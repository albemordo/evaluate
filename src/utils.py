from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Union, Any, Type, Tuple
from pathlib import Path
from simple_parsing import ArgumentParser
import sys


DEFAULT_DATA_FOLDER = 'data'
DEFAULT_MODEL_FOLDER = ''
DEFAULT_PROMPT_FILENAME = 'prompt.txt'
DEFAULT_GENERATED_FILES_PREFIX = 'output_'
DEFAULT_LOCAL_GENERATED_FOLDER_NAME = 'generated'
DEFAULT_TARGET_PLAN_FILENAME = 'plan.tfplan'
DEFAULT_TARGET_TF_FILENAME = 'main.tf'


@dataclass
class DataTreeAttributes:
    data_folder: str = DEFAULT_DATA_FOLDER                          # Root directory for data
    model_folder: str = DEFAULT_MODEL_FOLDER                        # Folder from which retrieve generated outputs
    providers_to_ignore: List[str] = field(
        default_factory = lambda: [])                               # List of providers to ignore
    tests_to_ignore: List[str] = field(
        default_factory = lambda: [])                               # List of tests to ignore
    #########
    prompt_filename: str = DEFAULT_PROMPT_FILENAME                  # Filename for the prompt
    generated_files_prefix: str = DEFAULT_GENERATED_FILES_PREFIX    # Standard prefix for model-generated output files
    local_generated_folder_name: str = DEFAULT_LOCAL_GENERATED_FOLDER_NAME  # Folder containing models' outputs
    target_plan_filename: str = DEFAULT_TARGET_PLAN_FILENAME                # Target (ground_truth) plan name
    target_tf_filename: str = DEFAULT_TARGET_TF_FILENAME                    # Target tf file name
    
    
@dataclass
class DataLoaderEntry:
    test_name_path: Path = None
    prompt_path: Path = None
    tf_file_path: Path = None
    plan_path: Path = None
    generated_files_path: List[Path] = field(default_factory=lambda: [])    
    
    
@dataclass
class Test:
    __test__ = False
    test_name: str = ''
    prompt: str = ''
    tf_file: str = ''
    plan: str = ''
    generated_files: List[str] = field(default_factory=lambda: [])
    meta_entry: DataLoaderEntry = None
    
    
def dict_to_arglist(input_dict: dict, first_argument='test') -> List[str]:
    argv = [f"--{k} {v if not isinstance(v, bool) else ''}".strip() for k, v in input_dict.items()]
    argv = ' '.join(argv).split(' ')
    argv.insert(0, first_argument)
    return argv


def check_dict_equality(input_dict: dict[str, Any], target_dict: dict[str, Any], strict_check=False) -> bool:
    '''Check equality between two dicts. If `strict_check=False` it only checks if any element inside target_dict is contained and equal to its input_dict counterpart, instead of full equality.'''
    if strict_check:    return input_dict == target_dict
    #equality = all([input_dict[key] == target_dict[key] for key in target_dict])
    for key in target_dict:
        if input_dict[key] != target_dict[key]:
            print(f"Key={key}, {input_dict[key]} != {target_dict[key]}")
            return False
    return True


def parse_argv(config: List[Tuple[Type, str]], argv: List[str] = sys.argv):
    parser = ArgumentParser()
    [parser.add_arguments(t, s) for t, s in config]
    print([w.dataclass for w in parser._wrappers])
    args, _ = parser.parse_known_args(argv)
    return args