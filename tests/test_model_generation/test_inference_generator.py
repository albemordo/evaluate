from src.generator import LLMInferenceGenerator
from src.utils import DataTreeAttributes, dict_to_arglist 
from src.dataloader import PromptDataLoader, DataLoaderAttributes
from src.generator import PeftModelWrapper
from src.huggingface_utils import AutoPeftModelAttributes, AutoTokenizerAttributes, QuantizationConfig, GenerationConfig
from src.generate import run_generation
import pytest
import sys
import torch


DATA_DIR = 'tests/test_model_generation/data'
MODEL_REPO = "ybelkada/opt-350m-lora"
TOKENIZER_REPO = 'facebook/opt-350m'


@pytest.mark.inference_generation
@pytest.mark.model_generation
class TestInferenceGenerstor:
    def test_inf_gen(self):
        dataloader_attrs = DataLoaderAttributes(DATA_DIR, model_folder='model_fanto')
        dataloader = PromptDataLoader(dataloader_attrs)
        quant_config = QuantizationConfig() if torch.cuda.is_available() else None
        generation_config = GenerationConfig(
            num_return_sequences=2, 
            num_beams=10,
            prompt_template_path='prompts/llama_2.txt')
        model_wrapper = PeftModelWrapper(
            automodel_attributes=AutoPeftModelAttributes(MODEL_REPO),
            autotokenizer_attributes=AutoTokenizerAttributes(TOKENIZER_REPO),
            generation_config=generation_config,
            quantization_config=quant_config)
        
        generator = LLMInferenceGenerator(
            data_tree_attributes=DataTreeAttributes(
                data_folder=DATA_DIR,
                model_folder='model_fanto'
            ),
            dataloader=dataloader,
            model_wrapper=model_wrapper,
            delete_duplicate_model_outputs_folder=True
        )
        
        generator.run()
        
        
    def test_main_generate_command(self):
        args = dict(
            data_folder=DATA_DIR,
            model_folder='model_fanto2',
            pretrained_model_name_or_path=MODEL_REPO,
            tokenizer_name_or_path=TOKENIZER_REPO,
            num_return_sequences=2,
            num_beams=10,
            prompt_template_path='prompts/llama_2.txt',
        )
        sys.argv = dict_to_arglist(args)
        run_generation()