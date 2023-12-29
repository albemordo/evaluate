from dataclasses import dataclass, asdict
from src.dataloader import PromptDataLoader, DataLoader
from src.utils import DataTreeAttributes, Test
from src.huggingface_utils import (
    AutoModelAttributes,
    AutoPeftModelAttributes, 
    AutoTokenizerAttributes, 
    QuantizationConfig)
from loguru import logger
from shutil import rmtree
from os import path
from tqdm import tqdm
from functools import reduce
from typing import Callable, List
from peft import AutoPeftModelForCausalLM, PeftModel
from transformers import PreTrainedModel, PreTrainedTokenizer, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch    
    
TextPreprocessor = Callable[[str], str]
    

class ModelWrapper:
    model: PreTrainedModel
    tokenizer: PreTrainedTokenizer
    AutoModelCLS = AutoModelForCausalLM
    AutoTokenizerCLS = AutoTokenizer
    
    
    def __init__(self,
                 automodel_attributes: AutoModelAttributes, 
                 autotokenizer_attributes: AutoTokenizerAttributes,
                 quantization_config: QuantizationConfig = None,
                 preprocessors: List[TextPreprocessor] = []):
        # Check for quantization options
        if (automodel_attributes.quantization_config is None 
            and quantization_config is not None):
            logger.info('Detected quantization config')
            automodel_attributes.quantization_config = BitsAndBytesConfig(**asdict(quantization_config))
            
        # Load model
        self.load_model(automodel_attributes)
        # Load tokenizer
        self.load_tokenizer(autotokenizer_attributes)
        
        self.preprocessors = preprocessors
        
        
    def load_tokenizer(self, attrs: AutoTokenizerAttributes):
        logger.info(f'Loading tokenizer from {attrs.pretrained_model_name_or_path} ({type(self.AutoTokenizerCLS).__name__})')
        self.tokenizer = self._load_tokenizer(attrs)
        
        
    def load_model(self, attrs: AutoModelAttributes):
        logger.info(f'Loading model from {attrs.pretrained_model_name_or_path} ({type(self.AutoModelCLS).__name__})')
        self.model = self._load_model(attrs)
        
        
    def _load_model(self, attrs: AutoModelAttributes) -> PreTrainedModel:
        model = self.AutoModelCLS.from_pretrained(**asdict(attrs))
        return model
    
    
    def _load_tokenizer(self, attrs: AutoTokenizerAttributes) -> PreTrainedTokenizer:
        tokenizer = self.AutoTokenizerCLS.from_pretrained(**asdict(attrs))
        return tokenizer
    
    
    def _generate(self, prompt: str, **kwargs):
        inputs = self.tokenizer(prompt, return_tensors='pt')
        inputs.to('cuda' if torch.cuda.is_available() else 'cpu')
        outputs = self.model.generate(**inputs, 
                                      eos_token_id=self.model.config.eos_token_id,
                                      **kwargs)
        return outputs
    
    def preprocess_prompt(self, prompt: str):
        if self.preprocessors:
            iterator = self.preprocessors.copy()
            iterator.insert(0, prompt)
            output = str(reduce(lambda agg, x: x(agg), iterator))   # First element 'agg' is the prompt
        else: output = prompt
        return output
    
    
    def postprocess_model_output(self, outputs):
        generated_texts = self.tokenizer.batch_decode(outputs.detach().cpu().numpy(), skip_special_tokens=True)
        return generated_texts
    
    
    def generate(self, prompt: str, **kwargs):
        logger.trace(f'Generating input for prompt\n{prompt}\n')
        prompt = self.preprocess_prompt(prompt) # Preprocess
        outputs = self._generate(prompt=prompt, **kwargs)
        text = self.postprocess_model_output(outputs)
        return text

    
class PeftModelWrapper(ModelWrapper):
    model: PeftModel
    AutoModelCLS = AutoPeftModelForCausalLM
    
    def __init__(self,
                automodel_attributes: AutoPeftModelAttributes, 
                autotokenizer_attributes: AutoTokenizerAttributes,
                quantization_config: QuantizationConfig = None):
        super().__init__(automodel_attributes, autotokenizer_attributes, quantization_config)
        
        
class LLMInferenceGenerator:
    def __init__(self, 
                 data_tree_attributes: DataTreeAttributes,
                 dataloader: DataLoader,
                 model_wrapper: ModelWrapper,
                 delete_duplicate_model_outputs_folder: bool = True):
        self.data_tree_attributes = data_tree_attributes
        self.dataloader = dataloader
        self.model_wrapper = model_wrapper
        self.delete_duplicate_model_outputs_folder = delete_duplicate_model_outputs_folder
        
    
    def process_item(self, item: Test):
        absolute_model_output_path = item.meta_entry.test_name_path.joinpath(
                self.data_tree_attributes.local_generated_folder_name, 
                self.data_tree_attributes.model_folder
            ).absolute()
        
        # Check if to eliminate directory
        if absolute_model_output_path.exists() and self.delete_duplicate_model_outputs_folder:
            logger.info(f"Eliminating directory {absolute_model_output_path}")
            rmtree(str(absolute_model_output_path))
        else:   absolute_model_output_path.mkdir(exist_ok=True)
        
        # Model inference
        output_texts = self.model_wrapper.generate(item.prompt)
        
        # Output saving
        logger.info('Saving files')
        for i, text in tqdm(enumerate(output_texts)):
            file_name = str(self.data_tree_attributes.generated_files_prefix)+str(i)    # output_x
            output_file_path = absolute_model_output_path.joinpath(file_name).absolute()
            logger.trace(f'Saving file {output_file_path}')
            output_file_path.touch()            # create file
            output_file_path.write_text(text)   # write to file
    
    
    def run(self):
        for item in tqdm(self.dataloader):
            logger.info(f'Processing test {item.test_name}')
            self.process_item(item)