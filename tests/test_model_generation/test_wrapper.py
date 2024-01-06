from __future__ import annotations
from src.dataloader import PromptDataLoader, DataLoaderAttributes
from src.generator import PeftModelWrapper
from src.huggingface_utils import AutoPeftModelAttributes, AutoTokenizerAttributes, QuantizationConfig, GenerationConfig
import pytest
import torch


DATA_DIR = 'tests/test_model_generation/data'
MODEL_REPO = "ybelkada/opt-350m-lora"
TOKENIZER_REPO = 'facebook/opt-350m'


@pytest.mark.model_generation
@pytest.mark.model_wrapper
class TestModelWrapper:
    def test_model_generation(self):
        dataloader_attrs = DataLoaderAttributes(DATA_DIR, model_folder='modelx')
        dataloader = PromptDataLoader(dataloader_attrs)
        quant_config = QuantizationConfig() if torch.cuda.is_available() else None
        generation_config = GenerationConfig()
        model_wrapper = PeftModelWrapper(
            automodel_attributes=AutoPeftModelAttributes(MODEL_REPO),
            autotokenizer_attributes=AutoTokenizerAttributes(TOKENIZER_REPO),
            quantization_config=quant_config,
            generation_config=generation_config)
        
        for test in dataloader:
            assert test.prompt is not None
            model_wrapper.generate(test.prompt)