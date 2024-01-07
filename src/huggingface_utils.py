from transformers import BitsAndBytesConfig
from dataclasses import dataclass, field
from torch import dtype
from loguru import logger
import torch


@dataclass
class AutoModelAttributes:
    pretrained_model_name_or_path: str
    #quantization_config: BitsAndBytesConfig = None
    trust_remote_code: bool = True
    token: bool = True
    

@dataclass
class AutoPeftModelAttributes(AutoModelAttributes):
    adapter_name: str = 'default'
    
    
@dataclass
class QuantizationConfig:
    load_in_4bit: bool = True
    load_in_8bit: bool = False
    bnb_4bit_quant_type: str = 'nf4'
    bnb_4bit_compute_dtype: dtype = torch.float16
    
    def __post_init__(self):
        if self.load_in_4bit and self.load_in_8bit:
            logger.warning('Both `load_in_4bit` and `load_in_8bit` are set, unsetting `load_in_4bit`')
            self.load_in_4bit = False

    
@dataclass
class AutoTokenizerAttributes:
    tokenizer_name_or_path: str
    pretrained_model_name_or_path: str = field(default=None, init=False)
    trust_remote_code: bool = True
    use_fast: bool = True
    
    def __post_init__(self):
        self.pretrained_model_name_or_path = self.tokenizer_name_or_path
        
        
DEFAULT_PROMPT_TEMPLATE_PATH = 'prompts/no_template.txt'

@dataclass
class GenerationConfig:
    max_new_tokens: int = None
    early_stopping: bool = False
    max_time: float = None
    do_sample: bool = False
    num_beams: int = 1
    num_beam_groups: int = 1
    use_cache: bool = False
    temperature: float = 1.0
    top_k: int = 50
    top_p: float = 1.0
    num_return_sequences: int = 1
    prompt_template_path: str = None