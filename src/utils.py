from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Union
from pathlib import Path


DEFAULT_DATA_FOLDER = 'data'
DEFAULT_MODEL_FOLDER = ''


@dataclass
class BaseEvaluationAttributes:
    data_folder: str = DEFAULT_DATA_FOLDER                          # Root directory for data
    model_folder: str = DEFAULT_MODEL_FOLDER                        # Folder from which retrieve generated outputs
    providers_to_ignore: List[str] = field(
        default_factory = lambda: [])                               # List of providers to ignore
    tests_to_ignore: List[str] = field(
        default_factory = lambda: [])                               # List of tests to ignore
    
    
    
@dataclass
class DataLoaderEntry:
    test_name_path: Path = None
    prompt_path: Path = None
    tf_file_path: Path = None
    plan_path: Path = None
    generated_files_path: List[Path] = field(default_factory=lambda: [])    
    
    
@dataclass
class Test:
    test_name: str
    prompt: str
    tf_file: str
    plan: str
    generated_files: List[str] = field(default_factory=lambda: [])
    meta_entry: DataLoaderEntry = None