from src.generator import LLMInferenceGenerator
from src.utils import DataTreeAttributes       
from src.dataloader import PromptDataLoader, DataLoaderAttributes
from src.generator import PeftModelWrapper
from src.huggingface_utils import AutoPeftModelAttributes, AutoTokenizerAttributes 
import pytest


DATA_DIR = 'tests/test_model_generation/data'
MODEL_REPO = "ybelkada/opt-350m-lora"
TOKENIZER_REPO = 'facebook/opt-350m'


@pytest.mark.model_generation
@pytest.mark.inference_generation
class TestInferenceGenerstor:
    def test_inf_gen_no_quant(self):
        dataloader_attrs = DataLoaderAttributes(DATA_DIR, model_folder='modelx')
        dataloader = PromptDataLoader(dataloader_attrs)
        
        model_wrapper = PeftModelWrapper(
            automodel_attributes=AutoPeftModelAttributes(MODEL_REPO),
            autotokenizer_attributes=AutoTokenizerAttributes(TOKENIZER_REPO))
        
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