# 🚀 GitOps AI Application Repository

[![Build Status](https://img.shields.io/jenkins/build?jobUrl=https%3A%2F%2Fjenkins.example.com%2Fjob%2Fgitops-ai-app)](https://jenkins.example.com)
[![Coverage](https://img.shields.io/badge/coverage-85%25-green)](https://jenkins.example.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 Overview

This is the **Application Repository** for the GitOps-Driven AI Inference Platform. It contains:

- 🐍 **Python FastAPI application** for AI inference
- 🧪 **Unit tests** with pytest
- 🐳 **Multi-stage Dockerfile** for production builds
- 🔄 **Jenkins CI pipelines** for build automation

> ⚠️ This repository does NOT contain Kubernetes manifests. See [gitops-manifests](../gitops-manifests) for deployment configuration.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Tier                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   FastAPI   │  │   /predict  │  │      /metrics       │ │
│  │   main.py   │  │   endpoint  │  │   (Prometheus)      │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│                    Application Tier                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Inference  │  │  Sentiment  │  │   Text Preprocessor │ │
│  │   Service   │  │    Model    │  │                     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
gitops-ai-app/
├── src/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment configuration
│   ├── api/
│   │   └── predict.py       # /predict endpoint
│   ├── services/
│   │   └── inference_service.py
│   ├── models/
│   │   └── sentiment_model.py
│   └── utils/
│       └── preprocessing.py
├── tests/
│   ├── test_api.py
│   └── test_inference.py
├── Dockerfile
├── requirements.txt
├── Jenkinsfile              # Main CI pipeline
└── Jenkinsfile.pr           # PR validation pipeline
```

## 🚀 Quick Start

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Build image
docker build -t ai-inference:dev .

# Run container
docker run -p 8000:8000 ai-inference:dev
```

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Liveness probe |
| `/ready` | GET | Readiness probe |
| `/metrics` | GET | Prometheus metrics |
| `/api/v1/predict` | POST | Single text prediction |
| `/api/v1/predict/batch` | POST | Batch predictions |

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

### Example Response

```json
{
  "success": true,
  "result": {
    "text": "This product is amazing!",
    "label": "POSITIVE",
    "confidence": 0.95,
    "sentiment_score": 0.95,
    "processing_time_ms": 45.2
  },
  "model": "distilbert-base-uncased-finetuned-sst-2-english",
  "timestamp": "2025-01-01T12:00:00.000Z",
  "request_id": "abc-123-def"
}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

## 🔧 Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8000 | Server port |
| `HOST` | 0.0.0.0 | Server host |
| `WORKERS` | 4 | Uvicorn workers |
| `DEBUG` | false | Debug mode |
| `LOG_LEVEL` | INFO | Logging level |
| `MODEL_NAME` | distilbert-base-uncased... | HuggingFace model |
| `MAX_SEQUENCE_LENGTH` | 512 | Max input length |

## 🔄 CI/CD Pipeline

### Main Branch Pipeline (`Jenkinsfile`)

1. ✅ Code checkout
2. ✅ Unit tests with coverage
3. ✅ Code quality (Flake8, Black, MyPy)
4. ✅ Security scan (Bandit, Safety)
5. ✅ Docker image build
6. ✅ Container security scan (Trivy)
7. ✅ Push to registry
8. ✅ **Update GitOps repository**

### PR Pipeline (`Jenkinsfile.pr`)

1. ✅ Fast validation
2. ✅ Unit tests
3. ✅ Linting checks
4. ✅ Build verification

## 📊 Metrics

The application exposes Prometheus metrics at `/metrics`:

- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request latency
- `predictions_total` - Total predictions
- `prediction_duration_seconds` - Prediction latency

## 🔐 Security

- Non-root container user
- Multi-stage Docker build
- Dependency vulnerability scanning
- Container image scanning
- Input validation with Pydantic

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.
