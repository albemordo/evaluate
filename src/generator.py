from dataclasses import dataclass, asdict
from src.dataloader import DataLoader
from src.utils import DataTreeAttributes, Test
from src.huggingface_utils import (
    AutoModelAttributes,
    AutoPeftModelAttributes, 
    AutoTokenizerAttributes, 
    QuantizationConfig,
    GenerationConfig)
from loguru import logger
from shutil import rmtree
from os import path
from tqdm.notebook import tqdm
from functools import reduce
from typing import Callable, List
from peft import AutoPeftModelForCausalLM, PeftModel
from pathlib import Path
from transformers import PreTrainedModel, PreTrainedTokenizer, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch    
import sys
    
    
TextPreprocessor = Callable[[str], str]
PROMPT_TEMPLATE_PROMPT_KEYWORD = 'prompt'


def to_cuda_or_cpu(x):
    x.to('cuda' if torch.cuda.is_available() else 'cpu')


class ModelWrapper:
    model: PreTrainedModel
    tokenizer: PreTrainedTokenizer
    generation_config: GenerationConfig
    AutoModelCLS = AutoModelForCausalLM
    AutoTokenizerCLS = AutoTokenizer
    
    
    def __init__(self,
                 automodel_attributes: AutoModelAttributes, 
                 autotokenizer_attributes: AutoTokenizerAttributes,
                 generation_config: GenerationConfig,
                 quantization_config: QuantizationConfig = None,
                 preprocessors: List[TextPreprocessor] = []):
        # Check for quantization options
        if (quantization_config is not None):   logger.info('Detected quantization config')
            
        # Load model
        bnb_conf = BitsAndBytesConfig(**asdict(quantization_config)) if quantization_config else None
        self.load_model(automodel_attributes, quantization_config = bnb_conf)
        
        # Load tokenizer
        self.load_tokenizer(autotokenizer_attributes)
        
        self.generation_config = generation_config
        self.preprocessors = preprocessors
        
        # Prompt template formatting
        if self.generation_config.prompt_template_path:
            template = Path(self.generation_config.prompt_template_path).read_text()
            del self.generation_config.prompt_template_path
            format_fn = lambda prompt: template.format(prompt=prompt)
            self.preprocessors.append(format_fn)
            
        
    def load_tokenizer(self, attrs: AutoTokenizerAttributes):
        logger.info(f'Loading tokenizer from {attrs.pretrained_model_name_or_path} ({type(self.AutoTokenizerCLS).__name__})')
        self.tokenizer = self._load_tokenizer(attrs)
        
        
    def load_model(self, attrs: AutoModelAttributes, **kwargs):
        logger.info(f'Loading model from {attrs.pretrained_model_name_or_path} ({type(self.AutoModelCLS).__name__})')
        self.model = self._load_model(attrs, **kwargs)
        to_cuda_or_cpu(self.model)
        
        
    def _load_model(self, attrs: AutoModelAttributes, **kwargs) -> PreTrainedModel:
        model = self.AutoModelCLS.from_pretrained(**asdict(attrs), **kwargs)
        return model
    
    
    def _load_tokenizer(self, attrs: AutoTokenizerAttributes) -> PreTrainedTokenizer:
        tokenizer = self.AutoTokenizerCLS.from_pretrained(**asdict(attrs))
        return tokenizer
    
    
    def _generate(self, prompt: str, **kwargs):
        inputs = self.tokenizer(prompt, return_tensors='pt')
        to_cuda_or_cpu(inputs)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, 
                                      eos_token_id=self.model.config.eos_token_id,
                                      **asdict(self.generation_config),
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
                generation_config: GenerationConfig,
                quantization_config: QuantizationConfig = None):
        super().__init__(automodel_attributes, autotokenizer_attributes, generation_config, quantization_config)
        
        
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
            logger.trace(f"Eliminating directory {absolute_model_output_path}")
            rmtree(str(absolute_model_output_path))
        # Create if not exists
        absolute_model_output_path.mkdir(exist_ok=True, parents=True)
        
        # Model inference
        # Generating N sequences in parallel may be hardware intense
        # so we do it sequentially
        num_sequences = self.model_wrapper.generation_config.num_return_sequences
        if num_sequences > 1:   self.model_wrapper.generation_config.num_return_sequences = 1
        output_texts = [self.model_wrapper.generate(item.prompt) for _ in range(num_sequences)]
        
        # Output saving
        with tqdm(total=len(output_texts), position=0, leave=False) as pbar:
            for i, text in enumerate(output_texts):
                file_name = str(self.data_tree_attributes.generated_files_prefix)+str(i)    # output_x
                output_file_path = absolute_model_output_path.joinpath(file_name).absolute()
                logger.trace(f'Saving file {output_file_path}')
                output_file_path.touch()            # create file
                output_file_path.write_text(text)   # write to file
                
                pbar.update()
                pbar.refresh()
    
    
    def run(self):
        with tqdm(total=len(self.dataloader), leave=False, position=0) as pbar:
            for item in self.dataloader:
                pbar.set_description(item.test_name)
                logger.trace(f'Processing test {item.test_name}')
                # Inference
                self.process_item(item)
                
                # Update bar
                pbar.update()
                pbar.refresh()