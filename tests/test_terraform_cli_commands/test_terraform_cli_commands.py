from src.terraform_cli_utils import (
    TerraformInitCommandExecutor, 
    TerraformValidateCommandExecutor,
    TerraformPlanCommandExecutor,
    TerraformShowPlanCommandExecutor
)
from pathlib import Path
import json


def do_validate_terraform(directory: str, expected_result=True, init=True):
    abs_path = Path(directory).absolute()
    if init:    
        do_init_terraform(directory, expected_result)
    executor = TerraformValidateCommandExecutor(abs_path)
    exit_code, output = executor.run()
    assert (exit_code == 0) == expected_result
    
    if exit_code == 0:
        output_dict = dict(json.loads(output))
        error_count = output_dict['error_count']
        valid = output_dict['valid']
        assert error_count == 0 and valid
        
    
def do_init_terraform(directory: str, expected_result=True):
    path = Path(directory)
    executor = TerraformInitCommandExecutor(path.absolute())
    exit_code, _ = executor.run()
    assert (exit_code == 0) == expected_result
        
        
def do_generate_plan(directory: str, expected_result=True, init=True):
    abs_path = Path(directory).absolute()
    if init:    
        do_init_terraform(directory, expected_result)
    executor = TerraformPlanCommandExecutor(abs_path)
    exit_code, _ = executor.run()
    assert (exit_code == 0) == expected_result
    
    if exit_code == 0:
        show_plan_executor = TerraformShowPlanCommandExecutor(abs_path)
        show_exit_code, plan_content = show_plan_executor.run()
        assert show_exit_code == 0
        plan_content_dict = json.loads(plan_content)
        succes = not plan_content_dict['errored']
        assert succes == expected_result
    

class TestInitCommand:
    def test_init_existing_directory(self):
        do_init_terraform('tests/test_terraform_cli_commands/valid/aws_provider_only/')
        

class TestValidateCommand:
    def do_validate_invalid_files(self, dir):
        do_validate_terraform(dir, expected_result=False)
        
    def test_random_content(self):
        self.do_validate_invalid_files('tests/test_terraform_cli_commands/invalid/random_content/')
    
    def test_aws_provider_only(self):
        do_validate_terraform('tests/test_terraform_cli_commands/valid/aws_provider_only/')
        

class TestPlanCommand:
    def test_aws_bucket(self):
        do_generate_plan('tests/test_terraform_cli_commands/valid/aws_bucket')