from transformers import BitsAndBytesConfig
from dataclasses import dataclass, field
from torch import dtype
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

    
# TODO: cambia nome dell'attributo 'pretrained_model_name_or_path'
@dataclass
class AutoTokenizerAttributes:
    tokenizer_name_or_path: str
    pretrained_model_name_or_path: str = field(default=None, init=False)
    trust_remote_code: bool = True
    use_fast: bool = True
    
    def __post_init__(self):
        self.pretrained_model_name_or_path = self.tokenizer_name_or_path