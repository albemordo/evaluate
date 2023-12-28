from src.terraform_cli_utils import (
    TerraformInitCommandExecutor, 
    TerraformValidateCommandExecutor,
    TerraformPlanCommandExecutor,
    TerraformShowPlanCommandExecutor
)
from pathlib import Path
from os import path
from typing import Any
import json
import pytest


DATA_FOLDER = 'tests/test_terraform_cli_commands/'
VALID_DATA_FOLDER = 'tests/test_terraform_cli_commands/valid/'
INVALID_DATA_FOLDER = 'tests/test_terraform_cli_commands/invalid/'


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
        
        
def do_generate_plan(directory: str, expected_result=True, init=True, **plan_executor_args):
    abs_path = Path(directory).absolute()
    if init:    
        do_init_terraform(directory)
    executor = TerraformPlanCommandExecutor(abs_path, **plan_executor_args)
    exit_code, plan_command_output = executor.run()
    
    print(executor.cli_command)
    print(plan_command_output)
    assert (exit_code == 0) == expected_result
    
    if exit_code == 0:
        show_plan_executor = TerraformShowPlanCommandExecutor(abs_path)
        show_exit_code, plan_content = show_plan_executor.run()
        assert show_exit_code == 0
        plan_content_dict = json.loads(plan_content)
        succes = not plan_content_dict['errored']
        assert succes == expected_result
        
        
def do_show_plan(directory: str, expected_result=True, target_plan: dict[str, Any] = None, **show_executor_args):
    abs_path = Path(directory).absolute()
    executor = TerraformShowPlanCommandExecutor(abs_path, **show_executor_args)
    exit_code, show_command_output = executor.run()
    
    assert (exit_code == 0) == expected_result
    if exit_code == 0 and (target_plan is not None):
        plan_content_dict: dict[str, Any] = json.loads(show_command_output)
        success: bool = not plan_content_dict['errored']
        input_config: dict[str, Any] = plan_content_dict['configuration']
        target_config: dict[str, Any] = target_plan['configuration']
        assert success
        assert check_json_equality(input_config, target_config)
        
        
def check_json_equality(input_json: dict[str, Any], target_json: dict[str, Any], strict_check=False) -> bool:
    if strict_check:    return input_json == target_json
    equality = all([input_json[key] == target_json[key] for key in target_json])
    return equality


@pytest.mark.terraform_cli_commands
class TestInitCommand:
    def test_init_existing_directory(self):
        do_init_terraform(path.join(VALID_DATA_FOLDER, 'aws_provider_only/'))
        
        
@pytest.mark.terraform_cli_commands
class TestValidateCommand:
    def do_validate_invalid_files(self, dir):
        do_validate_terraform(dir, expected_result=False)
        
    def test_random_content(self):
        self.do_validate_invalid_files(path.join(INVALID_DATA_FOLDER, 'random_content/'))
    
    def test_aws_provider_only(self):
        do_validate_terraform(path.join(VALID_DATA_FOLDER, 'aws_provider_only/'))
        

@pytest.mark.terraform_cli_commands
class TestPlanCommand:
    def test_valid_configuration(self):
        do_generate_plan(path.join(VALID_DATA_FOLDER, 'aws_bucket'))
        do_generate_plan(path.join(VALID_DATA_FOLDER, 'generate_plan'))
        
    def test_invalid_configuration(self):
        do_generate_plan(path.join(INVALID_DATA_FOLDER, 'generate_plan'), expected_result=False)
        

@pytest.mark.terraform_cli_commands
class TestShowCommand:
    def test_valid_plan(self):
        folder = path.join(VALID_DATA_FOLDER, 'show_plan')
        target_plan_path = Path(path.join(folder, 'target_plan.json'))
        target_plan = json.loads(target_plan_path.read_text())
        do_show_plan(folder, target_plan=target_plan)