"""
Application Configuration
Environment-based configuration management
"""
import os
from typing import Optional
from functools import lru_cache


class Settings:
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "AI Inference Service")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    WORKERS: int = int(os.getenv("WORKERS", "4"))
    
    # Model
    MODEL_NAME: str = os.getenv("MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "/app/models")
    MAX_SEQUENCE_LENGTH: int = int(os.getenv("MAX_SEQUENCE_LENGTH", "512"))
    
    # Inference
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "32"))
    INFERENCE_TIMEOUT: int = int(os.getenv("INFERENCE_TIMEOUT", "30"))
    
    # Metrics
    METRICS_ENABLED: bool = os.getenv("METRICS_ENABLED", "true").lower() == "true"
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "9090"))
    
    # Health Check
    HEALTH_CHECK_PATH: str = os.getenv("HEALTH_CHECK_PATH", "/health")
    READINESS_CHECK_PATH: str = os.getenv("READINESS_CHECK_PATH", "/ready")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
