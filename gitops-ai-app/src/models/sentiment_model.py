"""
Sentiment Model - Application Tier
ML model wrapper for sentiment analysis
"""
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class SentimentModel:
    """
    Wrapper for sentiment analysis model.
    Supports both HuggingFace transformers and fallback mock model.
    """
    
    def __init__(self, model_name: str, cache_dir: str = "/app/models"):
        self.model_name = model_name
        self.cache_dir = cache_dir
        self._model = None
        self._tokenizer = None
        self._pipeline = None
        self._is_loaded = False
        self._use_mock = False
        
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the sentiment analysis model"""
        try:
            # Try to load HuggingFace transformers pipeline
            from transformers import pipeline
            
            logger.info(f"Loading model: {self.model_name}")
            
            self._pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=-1  # CPU, use 0 for GPU
            )
            
            self._is_loaded = True
            logger.info(f"Model {self.model_name} loaded successfully")
            
        except ImportError:
            logger.warning("Transformers not available, using mock model")
            self._use_mock = True
            self._is_loaded = True
            
        except Exception as e:
            logger.warning(f"Failed to load model {self.model_name}: {str(e)}")
            logger.info("Falling back to mock model")
            self._use_mock = True
            self._is_loaded = True
    
    def is_loaded(self) -> bool:
        """Check if model is loaded and ready"""
        return self._is_loaded
    
    def predict(self, text: str) -> Dict[str, Any]:
        """
        Predict sentiment for a single text.
        
        Args:
            text: Preprocessed input text
            
        Returns:
            Dictionary with label, confidence, and score
        """
        if self._use_mock:
            return self._mock_predict(text)
        
        try:
            result = self._pipeline(text)[0]
            
            # Normalize to consistent format
            label = result['label']
            score = result['score']
            
            # Convert to sentiment score (-1 to 1)
            if label.upper() == 'POSITIVE':
                sentiment_score = score
            elif label.upper() == 'NEGATIVE':
                sentiment_score = -score
            else:
                sentiment_score = 0.0
            
            return {
                'label': label,
                'confidence': score,
                'score': sentiment_score
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise
    
    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Predict sentiment for a batch of texts.
        
        Args:
            texts: List of preprocessed texts
            
        Returns:
            List of prediction dictionaries
        """
        if self._use_mock:
            return [self._mock_predict(text) for text in texts]
        
        try:
            results = self._pipeline(texts)
            
            predictions = []
            for result in results:
                label = result['label']
                score = result['score']
                
                if label.upper() == 'POSITIVE':
                    sentiment_score = score
                elif label.upper() == 'NEGATIVE':
                    sentiment_score = -score
                else:
                    sentiment_score = 0.0
                
                predictions.append({
                    'label': label,
                    'confidence': score,
                    'score': sentiment_score
                })
            
            return predictions
            
        except Exception as e:
            logger.error(f"Batch prediction failed: {str(e)}")
            raise
    
    def _mock_predict(self, text: str) -> Dict[str, Any]:
        """
        Mock prediction for testing without transformers.
        Uses simple keyword-based sentiment analysis.
        """
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 
                         'fantastic', 'love', 'happy', 'best', 'awesome',
                         'beautiful', 'perfect', 'brilliant', 'outstanding']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate',
                         'worst', 'disappointing', 'poor', 'sad', 'angry',
                         'ugly', 'disgusting', 'pathetic', 'failure']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        total = pos_count + neg_count
        
        if total == 0:
            return {
                'label': 'NEUTRAL',
                'confidence': 0.5,
                'score': 0.0
            }
        
        pos_ratio = pos_count / total
        
        if pos_ratio > 0.5:
            confidence = 0.5 + (pos_ratio * 0.5)
            return {
                'label': 'POSITIVE',
                'confidence': confidence,
                'score': confidence
            }
        else:
            confidence = 0.5 + ((1 - pos_ratio) * 0.5)
            return {
                'label': 'NEGATIVE',
                'confidence': confidence,
                'score': -confidence
            }
