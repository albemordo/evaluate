from typing import List, Union
from dataclasses import dataclass, field
from src.utils import BaseEvaluationAttributes, Test
from loguru import logger
from os import path


DEFAULT_EVALUATION_RESULTS_FOLDER_NAME = 'results'
DEFAULT_OVERWRITE_DUPLICATE_EVALUATION_RESULTS = False

@dataclass
class ValidatorAttributes(BaseEvaluationAttributes):
    evaluation_results_folder_name = DEFAULT_EVALUATION_RESULTS_FOLDER_NAME   # Folder in which output the evaluation results.
    overwrite_duplicate_evaluation_results = DEFAULT_OVERWRITE_DUPLICATE_EVALUATION_RESULTS


class Validator:
    attrs: ValidatorAttributes
    
    def __init__(self, attrs: ValidatorAttributes, logger):
        self.attrs = attrs
        self.logger = logger
        
        
    def validate(self, test: Test):
        complete_test_name = path.join(test.test_name, test.meta_entry.test_name_path.parent.name)
        self.logger.info(f"Validating test {complete_test_name}")
    
    
