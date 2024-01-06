from src.generator import LLMInferenceGenerator
from src.utils import dict_to_arglist, parse_argv, DataTreeAttributes      
from src.dataloader import PromptDataLoader, DataLoaderAttributes
from src.generator import PeftModelWrapper
from src.huggingface_utils import AutoPeftModelAttributes, AutoTokenizerAttributes, QuantizationConfig 
from typing import Type, Tuple, List
import sys


DATA_TREE_ATTRIBUTES_KEY = 'data_tree_attributes'
AUTOMODEL_ATTRIBUTES_KEY = 'automodel_attributes'
AUTOTOKENIZER_ATTRIBUTES_KEY = 'autotokenizer_attributes'
QUANTIZATION_ATTRIBUTES_KEY = 'quantization_attributes'


def get_parser_config():
    argparse_config: List[Tuple[Type, str]] = []
    argparse_config.append((DataTreeAttributes, DATA_TREE_ATTRIBUTES_KEY))
    argparse_config.append((AutoPeftModelAttributes, AUTOMODEL_ATTRIBUTES_KEY))
    argparse_config.append((AutoTokenizerAttributes, AUTOTOKENIZER_ATTRIBUTES_KEY))
    argparse_config.append((QuantizationConfig, QUANTIZATION_ATTRIBUTES_KEY))
    return argparse_config


def run_generation():
    # Argument parsing
    args = parse_argv(get_parser_config(), sys.argv[1:])
    automodel_attrs: AutoPeftModelAttributes = getattr(args, AUTOMODEL_ATTRIBUTES_KEY)
    autotokenizer_attrs = getattr(args, AUTOMODEL_ATTRIBUTES_KEY)
    data_tree_attrs: DataTreeAttributes = getattr(args, DATA_TREE_ATTRIBUTES_KEY)
    quantization_attrs: QuantizationConfig = getattr(args, QUANTIZATION_ATTRIBUTES_KEY, None)
    # Object building
    # Dataloader
    dataloader = PromptDataLoader(data_tree_attrs)
    # Model wrapper
    model_wrapper = PeftModelWrapper(
        automodel_attributes=automodel_attrs,
        autotokenizer_attributes=autotokenizer_attrs,
        quantization_config=quantization_attrs)
    # Generator
    generator = LLMInferenceGenerator(
        data_tree_attributes=data_tree_attrs,
        dataloader=dataloader,
        model_wrapper=model_wrapper,
        delete_duplicate_model_outputs_folder=True
    )
    # Run
    generator.run()


if __name__ == '__main__':
    run_generation()