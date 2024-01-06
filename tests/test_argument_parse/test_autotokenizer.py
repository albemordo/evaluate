from simple_parsing import ArgumentParser
from transformers import AutoTokenizer
from dataclasses import asdict
from src.utils import check_dict_equality, dict_to_arglist
from src.huggingface_utils import AutoTokenizerAttributes
from dotenv import find_dotenv, load_dotenv
import pytest


TOKENIZER_REPO = 'facebook/opt-350m'
# Config copied from https://huggingface.co/facebook/opt-350m/tokenizer_config.json
TOKENIZER_CONFIG = {
    "errors": "replace", 
    "unk_token": {
        "content": "</s>", 
        "single_word": False, 
        "lstrip": False, 
        "rstrip": False, 
        "normalized": True, 
        "__type": "AddedToken"
    }, 
    "bos_token": {
        "content": "</s>", 
        "single_word": False, 
        "lstrip": False, 
        "rstrip": False, 
        "normalized": True, 
        "__type": "AddedToken"
    }, 
    "eos_token": {
        "content": "</s>", 
        "single_word": False, 
        "lstrip": False, 
        "rstrip": False, 
        "normalized": True, 
        "__type": "AddedToken"
    }, 
    "pad_token": {
        "content": "<pad>", 
        "single_word": False, 
        "lstrip": False, 
        "rstrip": False, 
        "normalized": True, 
        "__type": "AddedToken"
    }, 
    "add_prefix_space": False, 
    "add_bos_token": True, 
    "special_tokens_map_file": None, 
    "name_or_path": "patrickvonplaten/opt-30b"
}

# Dotenv
load_dotenv(find_dotenv())

parser = ArgumentParser()
parser.add_arguments(AutoTokenizerAttributes, 'autotokenizer_attributes')


@pytest.mark.argparse
@pytest.mark.autotokenizer
class TestAutoTokenizer:
    def test_load_tokenizer(self):
        attrs = dict(tokenizer_name_or_path=TOKENIZER_REPO)
        argv = dict_to_arglist(attrs)
        parsed_args = parser.parse_known_args(argv)[0]
        autotokenizer_attrs = parsed_args.autotokenizer_attributes
        try:
            tokenizer = AutoTokenizer.from_pretrained(**asdict(autotokenizer_attrs))
        except Exception as e:
            print(e)
            
        # Check Integrity    
        assert tokenizer.pad_token == TOKENIZER_CONFIG.get('pad_token').get('content')
        assert tokenizer.unk_token == TOKENIZER_CONFIG.get('unk_token').get('content')
        assert tokenizer.eos_token == TOKENIZER_CONFIG.get('eos_token').get('content')
        assert tokenizer.bos_token == TOKENIZER_CONFIG.get('bos_token').get('content')