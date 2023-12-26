import subprocess
import os
from pathlib import Path


DEFAULT_DIRECTORY = './'
DEFAULT_MAIN_TERRAFORM_COMMAND = 'terraform'
DEFAULT_SUBPROCESS_ARGS = dict(
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)


class CLICommand:
    def __init__(self, main_command: str, subprocess_args=None):
        self.main_command = main_command.strip()
        self.subprocess_args = subprocess_args or DEFAULT_SUBPROCESS_ARGS
        self.global_options = ''
        self.command = ''
        self.command_options = ''
        self.command_argument = ''

    def set_global_options(self, options: str):
        self.global_options = options.strip()

    def set_command(self, command: str, options: str = '', argument: str = ''):
        self.command = command.strip()
        self.command_options = options.strip()
        self.command_argument = argument.strip()

    def run(self):
        args = filter(None, [self.main_command, self.global_options, self.command, self.command_options, self.command_argument])
        process = subprocess.run(args=list(args), **self.subprocess_args)
        text_output = process.stdout if process.returncode == 0 else process.stderr
        return int(process.returncode), str(text_output)

    def __str__(self):
        return " ".join(filter(None, [self.main_command, self.global_options, self.command, self.command_options, self.command_argument]))


class TerraformCommandExecutor:
    def __init__(self, directory: Path):
        self.cli_command = CLICommand(main_command=DEFAULT_MAIN_TERRAFORM_COMMAND)
        self.directory = directory if directory.is_absolute() else directory.absolute()
        self.check_directory()

    def check_directory(self):
        if not self.directory.exists():
            raise ValueError(f"Directory {self.directory} does not exist.")

    def set_global_options(self):
        chdir_option = f"-chdir={self.directory}"
        self.cli_command.set_global_options(chdir_option)

    def run(self):
        self.set_global_options()
        return self.cli_command.run()


# Terraform Init Command Executor
class TerraformInitCommandExecutor(TerraformCommandExecutor):
    def __init__(self, directory: Path, backend=False):
        super().__init__(directory)
        options = ""

        if not backend:
            options += "-backend=false"

        self.cli_command.set_command('init', options)


# Terraform Validate Command Executor
class TerraformValidateCommandExecutor(TerraformCommandExecutor):
    def __init__(self, directory: Path, json=True):
        super().__init__(directory)
        options = "-json" if json else ""
        self.cli_command.set_command('validate', options)


# Terraform Plan Command Executor
class TerraformPlanCommandExecutor(TerraformCommandExecutor):
    def __init__(self, directory: Path, json=False, input=False):
        super().__init__(directory)
        options = ""

        if json:
            options += "-json "
        if not input:
            options += "-input=false"

        self.cli_command.set_command('plan', options.strip())


# Terraform Show Plan Command Executor
class TerraformShowPlanCommandExecutor(TerraformCommandExecutor):
    def __init__(self, directory: Path, json=True, plan_name='plan.tfplan'):
        super().__init__(directory)
        options = "-json" if json else ""
        self.cli_command.set_command('show', options, plan_name)