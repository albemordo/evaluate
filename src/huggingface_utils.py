from transformers import BitsAndBytesConfig
from dataclasses import dataclass
import torch


@dataclass
class AutoModelAttributes:
    pretrained_model_name_or_path: str
    quantization_config: BitsAndBytesConfig = None
    trust_remote_code: bool = True
    token: bool = True
    

@dataclass
class AutoPeftModelAttributes(AutoModelAttributes):
    adapter_name: str = 'default'
    
    
@dataclass
class QuantizationConfig:
    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = 'nf4'
    bnb_4bit_compute_dtype = torch.float16
    
    
@dataclass
class AutoTokenizerAttributes:
    pretrained_model_name_or_path: str
    trust_remote_code: bool = True
    use_fast: bool = True