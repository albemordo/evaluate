from __future__ import annotations
from dataclasses import dataclass, field
from os import path, walk
from pathlib import Path
from typing import List, Union
from src.utils import DataTreeAttributes, Test, DataLoaderEntry
from loguru import logger


@dataclass
class DataLoaderAttributes(DataTreeAttributes):
    pass


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
            if self.check_provider_path_validity(provider):
                for test_folder in provider.iterdir():
                    # Check if this is a test folder (and not the 'generated' folder)
                    if self.check_test_path_validity(test_folder):
                        test_folders.append(test_folder)
        return test_folders
        
        
    def check_provider_path_validity(self, provider_folder: Path) -> bool:
        return provider_folder.is_dir() and provider_folder.name not in self.attrs.providers_to_ignore
    
    
    def check_test_path_validity(self, test_path: Path) -> bool:
        return test_path.is_dir() and test_path.name not in self.attrs.tests_to_ignore
    
    def do_check_entry_validity(self, entry: DataLoaderEntry) -> bool:
        return True
    
    def check_entry_validity(self, entry: DataLoaderEntry) -> bool:
        '''Check if an entry is valid before pushing to the entries attributes. If this function returns false, the entry is not added'''
        validity = self.do_check_entry_validity(entry)
        logger.trace(f"[{self.__class__.__name__}] Entry {entry.test_name_path.absolute()} validity: {validity}")
        return validity
        
        
    def get_entries(self):
        entries: List[DataLoaderEntry] = []
        for test_folder in self.test_folders:
            dataloader_entry = DataLoaderEntry(test_name_path=test_folder)
            try:
                abs_test_folder = test_folder.absolute()
                dataloader_entry.prompt_path = Path(path.join(abs_test_folder, self.attrs.prompt_filename))
                dataloader_entry.tf_file_path = Path(path.join(abs_test_folder, self.attrs.target_tf_filename))
                dataloader_entry.plan_path = Path(path.join(abs_test_folder, self.attrs.target_plan_filename))
                if self.attrs.model_folder:
                    generated_files_path = Path(path.join(abs_test_folder, self.attrs.local_generated_folder_name))
                    generated_files_path = [
                        file for file in generated_files_path.glob(
                            self.attrs.model_folder+'/'+self.attrs.generated_files_prefix+'*'
                        ) if file.is_file()
                    ]
                    dataloader_entry.generated_files_path = generated_files_path
                else:
                    dataloader_entry.generated_files_path = []
                
                
                # Add to entries if it's valid
                if self.check_entry_validity(dataloader_entry):
                    entries.append(dataloader_entry)
            except Exception as e:
                logger.warning(e)
        
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
            logger.warning(e)

    
    def __getitem__(self, idx: int) -> Test:
        entry = self.entries[idx]
        test = self.entry_to_output(entry)
        return test
    
    def __len__(self) -> int:
        return len(self.entries)
    

class CompileCheckDataLoader(DataLoader):
    def do_check_entry_validity(self, entry: DataLoaderEntry) -> bool:
        '''Check if an entry contains valid generated files before pushing to the entries attributes. If this function returns false, the entry is not added'''
        gen_files_valid = all([file_path.exists() and file_path.is_file() for file_path in entry.generated_files_path])
        return gen_files_valid
    
    
class FunctionalCorrectnessDataLoader(CompileCheckDataLoader):
    def do_check_entry_validity(self, entry: DataLoaderEntry) -> bool:
        '''Check if an entry contains valid target plan and generated files before pushing to the entries attributes. If this function returns false, the entry is not added'''
        compile_check_valid = super().check_entry_validity(entry)
        target_plan_valid = entry.plan_path.exists() and entry.plan_path.is_file()
        
        return all([compile_check_valid, target_plan_valid])
    
    
class PromptDataLoader(DataLoader):
    '''This DataLoader is used for model inference'''
    def do_check_entry_validity(self, entry: DataLoaderEntry) -> bool:
        '''Check if an entry contains valid prompt before pushing to the entries attributes. If this function returns false, the entry is not added'''
        prompt_valid = entry.prompt_path.exists() and entry.prompt_path.is_file()
        
        return prompt_valid