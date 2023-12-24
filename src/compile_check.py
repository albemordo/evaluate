import subprocess
import os
from pathlib import Path


def validate_terraform(directory: str):
    # Run `terraform init` first to ensure modules, etc. are properly loaded
    # This might be necessary if you haven't initialized the directory or if you've made changes to the configuration
    init_process = subprocess.run(
        ['terraform', f'-chdir={directory}' ,'init'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Check that 'terraform init' was successful before proceeding
    if init_process.returncode != 0:
        return False, init_process.stderr
    
    # Run `terraform validate` and capture its output
    validate_process = subprocess.run(
        ['terraform', f'-chdir={directory}' ,'validate'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Check if `terraform validate` was successful
    if validate_process.returncode == 0:
        return True, validate_process.stdout
    else:
        return False, validate_process.stderr