"""
Metaluminous Engine - Configuration Management
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "Metaluminous Engine"
    debug: bool = False
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "metaluminous"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    # Vector Store
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "philosophical_literature"
    
    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_primary_model: str = "qwen2.5:72b-instruct-q4_K_M"
    ollama_critic_model: str = "deepseek-r1:70b"
    ollama_creative_model: str = "mixtral:8x22b"
    
    # Cloud APIs
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    
    # OpenAI Models
    openai_model: str = "gpt-4o"
    openai_reasoning_model: str = "o1"
    
    # Anthropic Models
    anthropic_model: str = "claude-4.5-sonnet-20250514"
    
    # Google Models
    google_model: str = "gemini-2.5-pro"
    
    # Generation Settings
    max_iterations: int = 10
    temperature: float = 0.7
    novelty_threshold: float = 0.7
    min_testable_predictions: int = 2
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Logging
    log_level: str = "INFO"


settings = Settings()
