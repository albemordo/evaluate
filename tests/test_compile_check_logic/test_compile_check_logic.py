from src.compile_check import validate_terraform
from pathlib import Path


def do_validate_terraform(directory: str, should_be_valid=True):
    abs_path = str(Path(directory).absolute())
    valid, output = validate_terraform(abs_path)
    assert not (valid ^ should_be_valid)


class TestCompileCheckLogicOfInvalidFiles:
    def do_validate_invalid_files(self, dir):
        do_validate_terraform(dir, should_be_valid=False)
        
    def test_random_content(self):
        self.do_validate_invalid_files('tests/test_compile_check_logic/invalid/random_content/')
        
        
class TestCompileCheckLogicOfValidFiles:
    def test_aws_provider_only(self):
        do_validate_terraform('tests/test_compile_check_logic/valid/aws_provider_only/')