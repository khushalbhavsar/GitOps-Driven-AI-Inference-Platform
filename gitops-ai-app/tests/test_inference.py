"""
Inference Tests - CI Test Layer
Unit tests for inference service and model
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestTextPreprocessor:
    """Test text preprocessing utilities"""
    
    @pytest.fixture
    def preprocessor(self):
        """Create preprocessor instance"""
        from utils.preprocessing import TextPreprocessor
        return TextPreprocessor(max_length=512)
    
    def test_basic_preprocessing(self, preprocessor):
        """Test basic text cleaning"""
        text = "Hello World!"
        result = preprocessor.preprocess(text)
        
        assert result == "Hello World!"
    
    def test_url_removal(self, preprocessor):
        """Test URL removal"""
        text = "Check out https://example.com for more info"
        result = preprocessor.preprocess(text)
        
        assert "https://example.com" not in result
        assert "Check out" in result
    
    def test_email_removal(self, preprocessor):
        """Test email removal"""
        text = "Contact us at test@example.com"
        result = preprocessor.preprocess(text)
        
        assert "test@example.com" not in result
    
    def test_mention_removal(self, preprocessor):
        """Test @mention removal"""
        text = "Hello @user123, how are you?"
        result = preprocessor.preprocess(text)
        
        assert "@user123" not in result
    
    def test_hashtag_handling(self, preprocessor):
        """Test hashtag handling (keeps word, removes #)"""
        text = "This is #awesome"
        result = preprocessor.preprocess(text)
        
        assert "#" not in result
        assert "awesome" in result
    
    def test_whitespace_normalization(self, preprocessor):
        """Test whitespace normalization"""
        text = "Hello    World\t\tTest"
        result = preprocessor.preprocess(text)
        
        assert "  " not in result
        assert "\t" not in result
    
    def test_html_decoding(self, preprocessor):
        """Test HTML entity decoding"""
        text = "Hello &amp; World"
        result = preprocessor.preprocess(text)
        
        assert "&amp;" not in result
        assert "&" in result or "and" in result.lower()
    
    def test_truncation(self, preprocessor):
        """Test text truncation"""
        text = "word " * 200  # Very long text
        result = preprocessor.preprocess(text)
        
        assert len(result) <= 512
    
    def test_empty_input(self, preprocessor):
        """Test empty input handling"""
        result = preprocessor.preprocess("")
        assert result == ""
    
    def test_unicode_normalization(self, preprocessor):
        """Test unicode normalization"""
        text = "café"
        result = preprocessor.preprocess(text)
        
        assert "caf" in result


class TestSentimentModel:
    """Test sentiment model wrapper"""
    
    @pytest.fixture
    def mock_model(self):
        """Create mock model (without transformers)"""
        from models.sentiment_model import SentimentModel
        
        with patch.object(SentimentModel, '_load_model'):
            model = SentimentModel(
                model_name="test-model",
                cache_dir="/tmp/models"
            )
            model._use_mock = True
            model._is_loaded = True
            return model
    
    def test_positive_prediction(self, mock_model):
        """Test positive sentiment detection"""
        result = mock_model.predict("This is great and amazing!")
        
        assert result['label'] == 'POSITIVE'
        assert result['confidence'] > 0.5
        assert result['score'] > 0
    
    def test_negative_prediction(self, mock_model):
        """Test negative sentiment detection"""
        result = mock_model.predict("This is terrible and awful!")
        
        assert result['label'] == 'NEGATIVE'
        assert result['confidence'] > 0.5
        assert result['score'] < 0
    
    def test_neutral_prediction(self, mock_model):
        """Test neutral sentiment detection"""
        result = mock_model.predict("The sky is blue")
        
        assert result['label'] == 'NEUTRAL'
        assert result['confidence'] == 0.5
    
    def test_batch_prediction(self, mock_model):
        """Test batch prediction"""
        texts = [
            "This is great!",
            "This is terrible!"
        ]
        
        results = mock_model.predict_batch(texts)
        
        assert len(results) == 2
        assert results[0]['label'] == 'POSITIVE'
        assert results[1]['label'] == 'NEGATIVE'
    
    def test_is_loaded(self, mock_model):
        """Test model loaded status"""
        assert mock_model.is_loaded() is True


class TestInferenceService:
    """Test inference service"""
    
    @pytest.fixture
    def mock_service(self):
        """Create mock inference service"""
        from services.inference_service import InferenceService
        
        with patch('services.inference_service.SentimentModel') as MockModel, \
             patch('services.inference_service.TextPreprocessor') as MockPreprocessor:
            
            # Setup mock model
            mock_model = MagicMock()
            mock_model.is_loaded.return_value = True
            mock_model.predict.return_value = {
                'label': 'POSITIVE',
                'confidence': 0.95,
                'score': 0.95
            }
            MockModel.return_value = mock_model
            
            # Setup mock preprocessor
            mock_preprocessor = MagicMock()
            mock_preprocessor.preprocess.return_value = "processed text"
            MockPreprocessor.return_value = mock_preprocessor
            
            service = InferenceService()
            service.model = mock_model
            service.preprocessor = mock_preprocessor
            service._is_ready = True
            
            return service
    
    @pytest.mark.asyncio
    async def test_run_inference(self, mock_service):
        """Test single inference run"""
        result = await mock_service.run("This is a test")
        
        assert 'label' in result
        assert 'confidence' in result
        assert 'sentiment_score' in result
    
    def test_is_ready(self, mock_service):
        """Test service readiness check"""
        assert mock_service.is_ready() is True
    
    def test_get_model_info(self, mock_service):
        """Test model info retrieval"""
        info = mock_service.get_model_info()
        
        assert 'model_name' in info
        assert 'is_ready' in info


class TestFeatureExtraction:
    """Test feature extraction utilities"""
    
    @pytest.fixture
    def preprocessor(self):
        from utils.preprocessing import TextPreprocessor
        return TextPreprocessor()
    
    def test_extract_features(self, preprocessor):
        """Test feature extraction"""
        text = "Hello world! Visit https://example.com @user #hashtag"
        features = preprocessor.extract_features(text)
        
        assert 'original_length' in features
        assert 'word_count' in features
        assert features['has_urls'] is True
        assert features['has_mentions'] is True
        assert features['has_hashtags'] is True
    
    def test_batch_preprocessing(self, preprocessor):
        """Test batch preprocessing"""
        texts = ["Hello world!", "Test text"]
        results = preprocessor.batch_preprocess(texts)
        
        assert len(results) == 2
        assert all(isinstance(r, str) for r in results)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
