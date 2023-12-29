from simple_parsing import ArgumentParser
from peft import AutoPeftModelForCausalLM
from transformers import BitsAndBytesConfig
from typing import List
from dataclasses import dataclass, asdict
from src.utils import dict_to_arglist, check_dict_equality
from src.huggingface_utils import AutoPeftModelAttributes
from dotenv import find_dotenv, load_dotenv
from loguru import logger
import pytest
import torch


load_dotenv(find_dotenv())

MODEL = "ybelkada/opt-350m-lora"
# Copied from https://huggingface.co/ybelkada/opt-350m-lora. 
# Note that "target_modules" should be a List. 
# It's a Set because the `asdict` function used below, before checking for equality, converts that kind of attribute into a set.
MODEL_CONFIG = {
    "base_model_name_or_path": "facebook/opt-350m",
    "bias": "none",
    "fan_in_fan_out": False,
    "inference_mode": True,
    "init_lora_weights": True,
    "layers_pattern": None,
    "layers_to_transform": None,
    "lora_alpha": 32,
    "lora_dropout": 0.05,
    "modules_to_save": None,
    "peft_type": "LORA",
    "r": 16,
    "revision": None,
    "target_modules": {
        "q_proj",
        "v_proj"
    },
    "task_type": "CAUSAL_LM"
}
   

parser = ArgumentParser()
parser.add_arguments(AutoPeftModelAttributes, 'autopeftmodel_attributes')


@pytest.mark.argparse
@pytest.mark.autopeftmodel
@pytest.mark.filterwarnings("ignore: The installed")
class TestAutoPeftModelArgparse:
    def test_load_model_from_hub(self):
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type='nf4'
        )
        pars = dict(
            pretrained_model_name_or_path = MODEL,
            #quantization_config=quant_config
        )
        
        argv = dict_to_arglist(pars)
        args = parser.parse_known_args(argv)[0]
        autopeftmodel_attr: AutoPeftModelAttributes = args.autopeftmodel_attributes
        try:
            model = AutoPeftModelForCausalLM.from_pretrained(**asdict(autopeftmodel_attr))
        except Exception as e:
            print(e)
            assert False
        
        # Check model Loading
        assert model is not None
        # Check LoRa Config correctness
        model_peft_config = asdict(model.peft_config.get(autopeftmodel_attr.adapter_name))
        assert check_dict_equality(model_peft_config, MODEL_CONFIG)
        
        
    # Should be run on GPU environment, because quantization needs it.
    def test_load_model_from_hub_and_quantize(self):
        if torch.cuda_is_available():
            quant_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type='nf4'
            )
            pars = dict(
                pretrained_model_name_or_path = MODEL,
                quantization_config=quant_config
            )
            
            argv = dict_to_arglist(pars)
            args = parser.parse_known_args(argv)[0]
            autopeftmodel_attr: AutoPeftModelAttributes = args.autopeftmodel_attributes
            try:
                model = AutoPeftModelForCausalLM.from_pretrained(**asdict(autopeftmodel_attr))
            except Exception as e:
                print(e)
                assert False
            
            # Check model Loading
            assert model is not None
            # Check LoRa Config correctness
            model_peft_config = asdict(model.peft_config.get(autopeftmodel_attr.adapter_name))
            assert check_dict_equality(model_peft_config, MODEL_CONFIG)
            
            
class TestAutoPeftModelGeneration:
    pass