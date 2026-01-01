"""
Inference Service - Application Tier
Handles business logic for AI inference
"""
import logging
import asyncio
import time
from typing import Dict, Any, List, Optional
from concurrent.futures import ThreadPoolExecutor

from config import settings
from models.sentiment_model import SentimentModel
from utils.preprocessing import TextPreprocessor

logger = logging.getLogger(__name__)


class InferenceService:
    """
    Core inference service that orchestrates:
    - Text preprocessing
    - Model inference
    - Response formatting
    """
    
    def __init__(self):
        self.model: Optional[SentimentModel] = None
        self.preprocessor: Optional[TextPreprocessor] = None
        self._is_ready: bool = False
        self._executor = ThreadPoolExecutor(max_workers=settings.WORKERS)
        self.model_name = settings.MODEL_NAME
        
    async def initialize(self) -> None:
        """Initialize the inference service with model and preprocessor"""
        try:
            logger.info(f"Initializing inference service with model: {self.model_name}")
            
            # Initialize preprocessor
            self.preprocessor = TextPreprocessor(
                max_length=settings.MAX_SEQUENCE_LENGTH
            )
            
            # Initialize model (run in executor to avoid blocking)
            loop = asyncio.get_event_loop()
            self.model = await loop.run_in_executor(
                self._executor,
                self._load_model
            )
            
            self._is_ready = True
            logger.info("Inference service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize inference service: {str(e)}")
            self._is_ready = False
            raise
    
    def _load_model(self) -> SentimentModel:
        """Load the ML model (blocking operation)"""
        return SentimentModel(
            model_name=self.model_name,
            cache_dir=settings.MODEL_CACHE_DIR
        )
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        logger.info("Cleaning up inference service")
        self._is_ready = False
        self._executor.shutdown(wait=True)
        
    def is_ready(self) -> bool:
        """Check if service is ready to handle requests"""
        return self._is_ready and self.model is not None and self.model.is_loaded()
    
    async def run(self, text: str) -> Dict[str, Any]:
        """
        Run inference on a single text input.
        
        Args:
            text: Input text for sentiment analysis
            
        Returns:
            Dictionary with prediction results
        """
        if not self.is_ready():
            raise RuntimeError("Inference service is not ready")
        
        start_time = time.time()
        
        try:
            # Preprocess text
            processed_text = self.preprocessor.preprocess(text)
            
            # Run inference in executor to avoid blocking
            loop = asyncio.get_event_loop()
            result = await asyncio.wait_for(
                loop.run_in_executor(
                    self._executor,
                    self.model.predict,
                    processed_text
                ),
                timeout=settings.INFERENCE_TIMEOUT
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            return {
                'label': result['label'],
                'confidence': result['confidence'],
                'sentiment_score': result['score'],
                'processing_time_ms': processing_time
            }
            
        except asyncio.TimeoutError:
            logger.error(f"Inference timeout after {settings.INFERENCE_TIMEOUT}s")
            raise RuntimeError("Inference timeout")
        except Exception as e:
            logger.error(f"Inference failed: {str(e)}")
            raise
    
    async def run_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Run inference on a batch of texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of prediction results
        """
        if not self.is_ready():
            raise RuntimeError("Inference service is not ready")
        
        start_time = time.time()
        
        try:
            # Preprocess all texts
            processed_texts = [
                self.preprocessor.preprocess(text) 
                for text in texts
            ]
            
            # Run batch inference
            loop = asyncio.get_event_loop()
            results = await asyncio.wait_for(
                loop.run_in_executor(
                    self._executor,
                    self.model.predict_batch,
                    processed_texts
                ),
                timeout=settings.INFERENCE_TIMEOUT * 2  # Allow more time for batches
            )
            
            total_time = (time.time() - start_time) * 1000
            per_item_time = total_time / len(texts)
            
            return [
                {
                    'label': result['label'],
                    'confidence': result['confidence'],
                    'sentiment_score': result['score'],
                    'processing_time_ms': per_item_time
                }
                for result in results
            ]
            
        except asyncio.TimeoutError:
            logger.error("Batch inference timeout")
            raise RuntimeError("Batch inference timeout")
        except Exception as e:
            logger.error(f"Batch inference failed: {str(e)}")
            raise
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        return {
            'model_name': self.model_name,
            'is_ready': self.is_ready(),
            'max_sequence_length': settings.MAX_SEQUENCE_LENGTH,
            'batch_size': settings.BATCH_SIZE
        }
