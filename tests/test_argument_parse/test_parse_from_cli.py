from src.huggingface_utils import AutoPeftModelAttributes, AutoTokenizerAttributes, QuantizationConfig 
from src.utils import parse_argv, dict_to_arglist, DataTreeAttributes
from typing import List, Type, Tuple
import src.generate as generate
import pytest


cli_attributes = dict(
    data_folder='tests/test_model_generation/data',
    model_folder='lol',
    pretrained_model_name_or_path='dummy_path',
    tokenizer_name_or_path='duummy_path',
    adapter_name='fanto',
    load_in_4bit=True,
)


@pytest.mark.argparse
@pytest.mark.parse_from_cli
class TestParseCliArgs:
    def test_parse_generate_args(self):
        argparse_config: List[Tuple[Type, str]] = []
        argparse_config.append((DataTreeAttributes, generate.DATA_TREE_ATTRIBUTES_KEY))
        argparse_config.append((AutoPeftModelAttributes, generate.AUTOMODEL_ATTRIBUTES_KEY))
        argparse_config.append((AutoTokenizerAttributes, generate.AUTOTOKENIZER_ATTRIBUTES_KEY))
        argparse_config.append((QuantizationConfig, generate.QUANTIZATION_ATTRIBUTES_KEY))
        # Parsing
        args = parse_argv(argparse_config, dict_to_arglist(cli_attributes))
        automodel_attrs: AutoPeftModelAttributes = getattr(args, generate.AUTOMODEL_ATTRIBUTES_KEY)
        autotokenizer_attrs: AutoTokenizerAttributes = getattr(args, generate.AUTOTOKENIZER_ATTRIBUTES_KEY)
        dataloader_attrs: DataTreeAttributes = getattr(args, generate.DATA_TREE_ATTRIBUTES_KEY)
        quantization_attrs: QuantizationConfig = getattr(args, generate.QUANTIZATION_ATTRIBUTES_KEY, None)
        # Assertion
        assert dataloader_attrs.data_folder == cli_attributes.get('data_folder')
        assert dataloader_attrs.model_folder == cli_attributes.get('model_folder')
        assert automodel_attrs.pretrained_model_name_or_path == cli_attributes.get('pretrained_model_name_or_path')
        assert automodel_attrs.adapter_name == cli_attributes.get('adapter_name')
        assert quantization_attrs.load_in_4bit == cli_attributes.get('load_in_4bit')
        assert autotokenizer_attrs.pretrained_model_name_or_path == cli_attributes.get('tokenizer_name_or_path')