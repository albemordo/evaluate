from dataloader import PromptDataLoader, DataLoaderAttributes
from dataclasses import dataclass, field
from utils import DataTreeAttributes
from src.huggingface_utils import AutoPeftModelAttributes, AutoTokenizerAttributes, QuantizationConfig
from loguru import logger
from peft import PeftModelForCausalLM
    
    
@dataclass
class LLMInferenceGeneratorAttributes(DataTreeAttributes):
    delete_already_present_model_folder: bool = True
    
    
class PeftModelWrapper:
    def __init__(self,
                 autopeftmodel_attributes: AutoPeftModelAttributes, 
                 autotokenizer_attributes: AutoTokenizerAttributes,
                 quantization_config: QuantizationConfig = None):
        self.autopeftmodel_attributes = autopeftmodel_attributes
        self.autotokenizer_attributes = autotokenizer_attributes
        self.quantization_config = quantization_config
        
        
    def load_tokenizer(self):
        logger.info(f'Loading tokenizer from {self.autotokenizer_attributes.pretrained_model_name_or_path}')
        self.tokenizer = self.do_load_tokenizer()
        
    
    def load_model(self):
        logger.info(f'Loading model from {self.autopeftmodel_attributes.pretrained_model_name_or_path}')
        self.model = self.do_load_model()
        
        
    def do_load_model(self):
        return None
    
    def do_load_tokenizer(self):
        return None