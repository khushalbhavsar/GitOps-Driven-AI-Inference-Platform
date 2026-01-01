"""
API Tests - CI Test Layer
Unit tests for FastAPI endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client with mocked inference service"""
        with patch('main.InferenceService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.initialize = AsyncMock()
            mock_instance.cleanup = AsyncMock()
            mock_instance.is_ready.return_value = True
            mock_service.return_value = mock_instance
            
            from main import app
            return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test /health endpoint returns healthy status"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "service" in data
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestPredictEndpoint:
    """Test prediction endpoints"""
    
    @pytest.fixture
    def mock_inference_service(self):
        """Create mock inference service"""
        mock = MagicMock()
        mock.is_ready.return_value = True
        mock.model_name = "test-model"
        mock.run = AsyncMock(return_value={
            'label': 'POSITIVE',
            'confidence': 0.95,
            'sentiment_score': 0.95
        })
        mock.run_batch = AsyncMock(return_value=[
            {'label': 'POSITIVE', 'confidence': 0.95, 'score': 0.95},
            {'label': 'NEGATIVE', 'confidence': 0.85, 'score': -0.85}
        ])
        return mock
    
    @pytest.fixture
    def client(self, mock_inference_service):
        """Create test client with mocked service"""
        with patch('main.InferenceService') as mock_class:
            mock_class.return_value = mock_inference_service
            mock_inference_service.initialize = AsyncMock()
            mock_inference_service.cleanup = AsyncMock()
            
            from main import app
            with patch('main.inference_service', mock_inference_service):
                with patch('api.predict.get_inference_service', return_value=mock_inference_service):
                    return TestClient(app)
    
    def test_predict_valid_input(self, client):
        """Test prediction with valid input"""
        response = client.post(
            "/api/v1/predict",
            json={"text": "This is a great product!"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "result" in data
        assert data["result"]["label"] in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    
    def test_predict_empty_input(self, client):
        """Test prediction with empty input returns error"""
        response = client.post(
            "/api/v1/predict",
            json={"text": ""}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_predict_whitespace_only(self, client):
        """Test prediction with whitespace only returns error"""
        response = client.post(
            "/api/v1/predict",
            json={"text": "   "}
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_predict_long_text(self, client):
        """Test prediction with very long text"""
        long_text = "This is great! " * 500
        response = client.post(
            "/api/v1/predict",
            json={"text": long_text}
        )
        
        assert response.status_code == 200
    
    def test_batch_predict(self, client):
        """Test batch prediction endpoint"""
        response = client.post(
            "/api/v1/predict/batch",
            json={"texts": ["Great product!", "Terrible experience"]}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["results"]) == 2


class TestMetricsEndpoint:
    """Test Prometheus metrics endpoint"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        with patch('main.InferenceService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.initialize = AsyncMock()
            mock_instance.cleanup = AsyncMock()
            mock_instance.is_ready.return_value = True
            mock_service.return_value = mock_instance
            
            from main import app
            return TestClient(app)
    
    def test_metrics_endpoint(self, client):
        """Test /metrics endpoint returns Prometheus format"""
        response = client.get("/metrics")
        
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"] or \
               "text/plain" in response.headers.get("content-type", "")


class TestInputValidation:
    """Test input validation"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        with patch('main.InferenceService') as mock_service:
            mock_instance = MagicMock()
            mock_instance.initialize = AsyncMock()
            mock_instance.cleanup = AsyncMock()
            mock_instance.is_ready.return_value = True
            mock_service.return_value = mock_instance
            
            from main import app
            return TestClient(app)
    
    def test_missing_text_field(self, client):
        """Test request without text field"""
        response = client.post("/api/v1/predict", json={})
        
        assert response.status_code == 422
    
    def test_invalid_json(self, client):
        """Test request with invalid JSON"""
        response = client.post(
            "/api/v1/predict",
            content="not valid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422
    
    def test_batch_empty_list(self, client):
        """Test batch with empty list"""
        response = client.post(
            "/api/v1/predict/batch",
            json={"texts": []}
        )
        
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
