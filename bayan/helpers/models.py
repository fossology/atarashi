from enum import Enum

class Models(Enum):
    # GroQ Models
    LLAMA_3_8b = 'llama3-8b-8192'
    LLAMA_3_1_8b = 'llama-3.1-8b-instant'
    GEMMA_7b = 'gemma-7b-it'
    GEMMA_2_9b = 'gemma2-9b-it'

    # Together AI Models
    MISTRAL_7b = 'mistralai/Mistral-7B-Instruct-v0.3'
    TOGETHER_GEMMA_2_9b = 'google/gemma-2-9b-it'
    
    # NVIDIA Models
    PHI_3_MINI = 'microsoft/phi-3-mini-128k-instruct'
    PHI_3_SMALL = 'microsoft/phi-3-small-128k-instruct'
    PHI_3_MEDIUM = 'microsoft/phi-3-medium-128k-instruct'