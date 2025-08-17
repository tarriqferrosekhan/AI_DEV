from dataclasses import dataclass

@dataclass
class AppConfig:
    moderation_model:str
    data_source_file_name:str
    api_key_file_name:str
    base_llm:str
    similarity_top_k:int