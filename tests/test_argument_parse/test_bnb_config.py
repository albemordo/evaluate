from __future__ import annotations
from simple_parsing import ArgumentParser
from transformers import BitsAndBytesConfig
from typing import List
from dataclasses import asdict
from src.utils import dict_to_arglist
from src.huggingface_utils import QuantizationConfig
import pytest


parser = ArgumentParser()
parser.add_arguments(QuantizationConfig, "bnb_config")


@pytest.mark.argparse
@pytest.mark.bnb_config
class TestBitsAndBytesArgparse:
    def test_args(self):
        # Static target attributes
        args_dict = dict(
            load_in_4bit = True,
            bnb_4bit_quant_type = "nf4",
        )
        # Dict to argv list
        cli_args = dict_to_arglist(args_dict)
        args = parser.parse_known_args(cli_args)[0]
        bnb_args: QuantizationConfig = args.bnb_config
        
        # Assert no parsing errors
        assert bnb_args.load_in_4bit
        assert bnb_args.bnb_4bit_quant_type == "nf4"
        bnb_config = BitsAndBytesConfig(**asdict(bnb_args))
        # Assert no errors after the creation of BitsAndBytesClass
        assert bnb_config.load_in_4bit == args_dict.get('load_in_4bit')
        assert bnb_config.bnb_4bit_quant_type == args_dict.get('bnb_4bit_quant_type')
        

@pytest.mark.argparse
@pytest.mark.bnb_config
class TestBitsAndBytesConfig:
    def test_mandatory_parameters(self):
        try:
            config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4')
        except Exception as e:
            print(e)
            assert False # should never reach this point