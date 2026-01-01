"""
Prediction API Endpoint - Presentation Tier
Handles /predict endpoint for inference requests
"""
import logging
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field, validator
from prometheus_client import Counter, Histogram

from services.inference_service import InferenceService

logger = logging.getLogger(__name__)

router = APIRouter()

# Metrics
PREDICTION_COUNT = Counter(
    'predictions_total',
    'Total prediction requests',
    ['status', 'model']
)
PREDICTION_LATENCY = Histogram(
    'prediction_duration_seconds',
    'Prediction latency in seconds',
    ['model']
)


# Request/Response Models
class TextInput(BaseModel):
    """Single text input for prediction"""
    text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze")
    
    @validator('text')
    def text_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()


class BatchTextInput(BaseModel):
    """Batch text input for multiple predictions"""
    texts: List[str] = Field(..., min_items=1, max_items=100, description="List of texts to analyze")
    

class PredictionResult(BaseModel):
    """Single prediction result"""
    text: str
    label: str
    confidence: float
    sentiment_score: float
    processing_time_ms: float


class PredictionResponse(BaseModel):
    """API response for single prediction"""
    success: bool
    result: PredictionResult
    model: str
    timestamp: str
    request_id: str


class BatchPredictionResponse(BaseModel):
    """API response for batch predictions"""
    success: bool
    results: List[PredictionResult]
    model: str
    total_processing_time_ms: float
    timestamp: str
    request_id: str


# Dependency to get inference service
def get_inference_service():
    from main import get_inference_service as get_svc
    return get_svc()


@router.post("/predict", response_model=PredictionResponse)
async def predict(
    payload: TextInput,
    background_tasks: BackgroundTasks,
    inference_service: InferenceService = Depends(get_inference_service)
) -> PredictionResponse:
    """
    Perform sentiment analysis on input text.
    
    - **text**: The text to analyze (1-10000 characters)
    
    Returns prediction with label, confidence, and sentiment score.
    """
    import time
    import uuid
    
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        logger.info(f"Processing prediction request {request_id}")
        
        # Call inference service
        result = await inference_service.run(payload.text)
        
        processing_time = (time.time() - start_time) * 1000
        
        # Record metrics
        PREDICTION_COUNT.labels(
            status='success',
            model=inference_service.model_name
        ).inc()
        PREDICTION_LATENCY.labels(
            model=inference_service.model_name
        ).observe(processing_time / 1000)
        
        prediction_result = PredictionResult(
            text=payload.text[:100] + "..." if len(payload.text) > 100 else payload.text,
            label=result['label'],
            confidence=result['confidence'],
            sentiment_score=result['sentiment_score'],
            processing_time_ms=processing_time
        )
        
        return PredictionResponse(
            success=True,
            result=prediction_result,
            model=inference_service.model_name,
            timestamp=datetime.utcnow().isoformat(),
            request_id=request_id
        )
        
    except Exception as e:
        logger.error(f"Prediction failed for request {request_id}: {str(e)}")
        PREDICTION_COUNT.labels(
            status='error',
            model=inference_service.model_name if inference_service else 'unknown'
        ).inc()
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(
    payload: BatchTextInput,
    inference_service: InferenceService = Depends(get_inference_service)
) -> BatchPredictionResponse:
    """
    Perform batch sentiment analysis on multiple texts.
    
    - **texts**: List of texts to analyze (1-100 items)
    
    Returns predictions for all texts with processing times.
    """
    import time
    import uuid
    
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    try:
        logger.info(f"Processing batch prediction request {request_id} with {len(payload.texts)} texts")
        
        # Call batch inference
        results = await inference_service.run_batch(payload.texts)
        
        total_processing_time = (time.time() - start_time) * 1000
        
        prediction_results = [
            PredictionResult(
                text=text[:100] + "..." if len(text) > 100 else text,
                label=result['label'],
                confidence=result['confidence'],
                sentiment_score=result['sentiment_score'],
                processing_time_ms=result.get('processing_time_ms', 0)
            )
            for text, result in zip(payload.texts, results)
        ]
        
        PREDICTION_COUNT.labels(
            status='success',
            model=inference_service.model_name
        ).inc(len(payload.texts))
        
        return BatchPredictionResponse(
            success=True,
            results=prediction_results,
            model=inference_service.model_name,
            total_processing_time_ms=total_processing_time,
            timestamp=datetime.utcnow().isoformat(),
            request_id=request_id
        )
        
    except Exception as e:
        logger.error(f"Batch prediction failed for request {request_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )


@router.get("/models")
async def list_models(
    inference_service: InferenceService = Depends(get_inference_service)
):
    """List available models and their status"""
    return {
        "models": [
            {
                "name": inference_service.model_name,
                "status": "loaded" if inference_service.is_ready() else "loading",
                "type": "sentiment-analysis"
            }
        ]
    }
