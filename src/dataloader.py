from __future__ import annotations
from dataclasses import dataclass, field
from loguru import logger
from os import path, walk
from pathlib import Path
from typing import List, Union

DEFAULT_DATA_FOLDER = 'data'
DEFAULT_PROMPT_FILENAME = 'prompt.txt'
DEFAULT_GENERATED_FILES_PREFIX = 'output_'
DEFAULT_LOCAL_GENERATED_FOLDER_NAME = 'generated'
DEFAULT_TARGET_PLAN_FILENAME = 'plan.json'
DEFAULT_TARGET_TF_FILENAME = 'main.tf'
DEFAULT_MODEL_FOLDER = None


@dataclass
class DataLoaderAttributes:
    data_folder: str = DEFAULT_DATA_FOLDER                          # Root directory for data
    model_folder: str = DEFAULT_MODEL_FOLDER                        # Folder from which retrieve generated outputs
    providers_to_ignore: List[str] = field(
        default_factory = lambda: [])                               # List of providers to ignore
    tests_to_ignore: List[str] = field(
        default_factory = lambda: [])                               # List of tests to ignore
    prompt_filename: str = DEFAULT_PROMPT_FILENAME                  # Filename for the prompt
    generated_files_prefix: str = DEFAULT_GENERATED_FILES_PREFIX    # Standard prefix for model-generated output files
    local_generated_folder_name: str = DEFAULT_LOCAL_GENERATED_FOLDER_NAME  # Folder containing models' outputs
    target_plan_filename: str = DEFAULT_TARGET_PLAN_FILENAME                # Target (ground_truth) plan name
    target_tf_filename: str = DEFAULT_TARGET_TF_FILENAME                    # Target tf file name
   
    
@dataclass
class FunctionalDataLoaderAttributes(DataLoaderAttributes):
    pass
    
@dataclass
class CompileCheckDataLoaderAttributes(DataLoaderAttributes):
    pass
    
    
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


def retrieve_path_content_if_exists(x: Path) -> Union[str, None]:
    '''Returns the content of a Path object if exists and is a file'''
    return (x.read_text() if (x.is_file and x.exists())
                         else None)


########## DATA LOADERS ##########

class DataLoader:
    test_folders: List[Path]
    entries: List[DataLoaderEntry]
    
    def __init__(self, attrs: DataLoaderAttributes):
        self.attrs = attrs
        self.test_folders = self.load_test_folders()
        self.entries = self.get_entries()

    def load_test_folders(self):
        data_path = Path(self.attrs.data_folder)
        test_folders = []
        
        # Iterating through the directory structure
        for provider in data_path.iterdir():
            if provider.is_dir() and provider.name not in self.attrs.providers_to_ignore:
                for test_folder in provider.iterdir():
                    # Check if this is a test folder (and not the 'generated' folder)
                    if test_folder.is_dir() and test_folder.name not in self.attrs.tests_to_ignore:
                        test_folders.append(test_folder)
        return test_folders
        
        
    def get_entries(self):
        entries: List[DataLoaderEntry] = []
        for test_folder in self.test_folders:
            dataloader_entry = DataLoaderEntry(test_name_path=test_folder)
            try:
                abs_test_folder = test_folder.absolute()
                dataloader_entry.prompt_path = Path(path.join(abs_test_folder, self.attrs.prompt_filename))
                dataloader_entry.tf_file_path = Path(path.join(abs_test_folder, self.attrs.target_tf_filename))
                dataloader_entry.plan_path = Path(path.join(abs_test_folder, self.attrs.target_plan_filename))
                generated_files_path = Path(path.join(abs_test_folder, self.attrs.local_generated_folder_name))
                generated_files_path = [
                    file for file in generated_files_path.glob(
                        self.attrs.model_folder+'/'+self.attrs.generated_files_prefix+'*'
                    ) if file.is_file()
                ]
                dataloader_entry.generated_files_path = generated_files_path
                
                '''
                # Add to entries if every path exists
                if all([
                    pth.exists()
                    for pth in [
                        dataloader_entry.prompt_path,
                        dataloader_entry.tf_file_path,
                        dataloader_entry.plan_path     
                    ]
                ]):
                    entries.append(dataloader_entry)
                '''
                entries.append(dataloader_entry)
            except Exception as e:
                print(e)
        
        return entries
    
    
    def entry_to_output(self, entry: DataLoaderEntry) -> Test:
        '''Convert DataLoaderEntry objects having Path attributes to Test objects having the content as attributes instead'''
        try:
            name = entry.test_name_path.name
            prompt = retrieve_path_content_if_exists(entry.prompt_path)
            tf_file = retrieve_path_content_if_exists(entry.tf_file_path)
            plan = retrieve_path_content_if_exists(entry.plan_path)
            generated_files_content = [retrieve_path_content_if_exists(x) for x in entry.generated_files_path]
            # Using filter to remove None elements
            generated_files_content = list(filter(lambda x: x is not None, generated_files_content))
            
            return Test(
                test_name=name,
                prompt=prompt,
                tf_file=tf_file,
                plan=plan,
                generated_files=generated_files_content,
                meta_entry=entry
            )
        except Exception as e:
            print(e)

    
    def __getitem__(self, idx: int) -> Test:
        entry = self.entries[idx]
        test = self.entry_to_output(entry)
        return test