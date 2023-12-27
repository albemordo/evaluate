from typing import Union, List
from pathlib import Path
from src.dataloader import DataLoader, DataLoaderAttributes, PromptDataLoader


DATA_FOLDER = 'tests/test_dataloader/data'


def Path_to_str(x: Union[List[str], List[Path]], relative_to_folder: str) -> List[str]:
    if len(x) > 0:
        if isinstance(x[0], Path):  return [str(i.relative_to(relative_to_folder)) for i in x]
        elif isinstance(x[0], str): return x
        else:   raise TypeError(f'Type {type(x[0])} not a string nor Path')
    else:
        return x
    

def match_folders(input_folders, target_folders, relative_to_folder, strict=True):
        input_folders = Path_to_str(input_folders, relative_to_folder)
        target_folders = Path_to_str(target_folders, relative_to_folder)
        
        if strict:  assert sorted(input_folders) == sorted(target_folders)
        else:
            for folder in target_folders:
                assert folder in input_folders
    

class TestTestFolder:
    '''Operations to retrieve and filter test folders'''
    def test_no_filters(self):
        attrs = DataLoaderAttributes(data_folder=DATA_FOLDER)
        dataloader = DataLoader(attrs)
        
        true_test_folders = [
            'aws/instance_simple',
            'aws/provider_block',
            'google/provider_block',
        ]
        
        match_folders(dataloader.test_folders, true_test_folders, relative_to_folder=dataloader.attrs.data_folder, strict=False)
        
        
    def test_provider_filters(self):
        attrs = DataLoaderAttributes(data_folder=DATA_FOLDER, providers_to_ignore=['aws'])
        dataloader = DataLoader(attrs)
        
        true_test_folders = [
            'google/provider_block'
        ]
        
        match_folders(dataloader.test_folders, true_test_folders, relative_to_folder=dataloader.attrs.data_folder, strict=False)
        

    def test_tests_filters(self):
        attrs = DataLoaderAttributes(data_folder=DATA_FOLDER, tests_to_ignore=['instance_simple'])
        dataloader = DataLoader(attrs)
        
        true_test_folders = [
            'aws/provider_block',
            'google/provider_block'
        ]
        
        match_folders(dataloader.test_folders, true_test_folders, relative_to_folder=dataloader.attrs.data_folder, strict=False)
        
        
class TestGeneratedFilesFolders:
    '''Operations on model-generated files: data/PROVDER/TEST/generated/MODEL/output_*'''
    def test_one_test_no_filters(self):
        attrs = DataLoaderAttributes(
            data_folder=DATA_FOLDER,
            model_folder='model_x')
        
        dataloader = DataLoader(attrs)
        
        for item in dataloader:
            provider = item.meta_entry.test_name_path.parent.name
            test_name = item.test_name
            if provider == 'aws' and test_name == 'provider_block':
                # Target values
                output_files_content = ['fanto',''] # model_x/output_1.txt, model_x/output_2.tf
                main_tf_target_content = '# data/aws/provider_block/main.tf'
                prompt_target_content = '# data/aws/provider_block/prompt.txt'
                plan_target_content = '{}'
                # Assertion
                assert sorted(item.generated_files) == sorted(output_files_content)
                assert item.plan == plan_target_content
                assert item.tf_file == main_tf_target_content
                assert item.prompt == prompt_target_content

        # Should not reach this point
        #assert False, "Test should not reach this point. The requested test is not found."
        
        
class TestPromptDataLoader:
    def test_with_folders_with_valid_and_invalid_prompt(self):
        attrs = DataLoaderAttributes(
            data_folder=DATA_FOLDER)
        
        dataloader = PromptDataLoader(attrs)
        expected_folders = ['prompt_only/test_1', 'prompt_only/test_2']
        
        # Match valid prompt folders
        match_folders(dataloader.test_folders, expected_folders, strict=False, relative_to_folder=dataloader.attrs.data_folder)
        # Assert no_prompt is not contained
        assert 'prompt_only/no_prompt' not in dataloader.test_folders