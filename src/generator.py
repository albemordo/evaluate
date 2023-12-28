from dataloader import PromptDataLoader, DataLoaderAttributes
from dataclasses import dataclass, field
from utils import DataTreeAttributes
from transformers import BitsAndBytesConfig
from peft import AutoPeftModelForCausalLM


@dataclass
class LLMInferenceGeneratorAttributes(DataTreeAttributes):
    delete_already_present_model_outputs: bool = True
    