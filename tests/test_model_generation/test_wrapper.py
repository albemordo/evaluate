from __future__ import annotations
from src.dataloader import PromptDataLoader, DataLoaderAttributes
from src.generator import PeftModelWrapper
from src.huggingface_utils import AutoPeftModelAttributes, AutoTokenizerAttributes, QuantizationConfig
import pytest

DATA_DIR = 'tests/test_model_generation/data'
MODEL_REPO = "ybelkada/opt-350m-lora"
TOKENIZER_REPO = 'facebook/opt-350m'


@pytest.mark.model_generation
class TestModelWrapper:
    def test_model_generation(self):
        dataloader_attrs = DataLoaderAttributes(DATA_DIR, model_folder='modelx')
        dataloader = PromptDataLoader(dataloader_attrs)
        
        model_wrapper = PeftModelWrapper(
            automodel_attributes=AutoPeftModelAttributes(MODEL_REPO),
            autotokenizer_attributes=AutoTokenizerAttributes(TOKENIZER_REPO))
        
        for test in dataloader:
            assert test.prompt is not None
            model_wrapper.generate(test.prompt)