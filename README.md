# 🚀 GitOps-Driven AI Inference Platform

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Jenkins-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![GitOps](https://img.shields.io/badge/GitOps-Argo%20CD-EF7B4D?logo=argo&logoColor=white)](https://argoproj.github.io/cd/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

A production-ready **GitOps-Driven AI Inference Platform** that demonstrates modern cloud-native application deployment practices. This platform provides real-time sentiment analysis using a FastAPI-based microservice, deployed to Kubernetes via GitOps principles using Argo CD.

### ✨ Key Features

- 🤖 **AI-Powered Sentiment Analysis** - Real-time text classification with confidence scores
- 🔄 **GitOps Workflow** - Automated deployments via Argo CD
- 📦 **Container-Native** - Multi-stage Docker builds with security best practices
- 🏗️ **CI/CD Pipeline** - Jenkins-based build and deployment automation
- 📊 **Full Observability** - Prometheus metrics and Grafana dashboards
- 🎯 **Multi-Environment** - Dev, Staging, and Production configurations
- ⚡ **Auto-Scaling** - Horizontal Pod Autoscaler (HPA) support
- 🔐 **Security-First** - Non-root containers, health probes, resource limits

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          GitOps-Driven AI Inference Platform                        │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                     │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐ │
│   │   Developer  │───▶│  gitops-ai-  │───▶│   Jenkins    │───▶│  Docker Registry │ │
│   │  Code Push   │    │     app      │    │   CI/CD      │    │   (ECR/DockerHub)│ │
│   └──────────────┘    └──────────────┘    └──────────────┘    └────────┬─────────┘ │
│                                                   │                     │           │
│                                                   ▼                     │           │
│                                           ┌──────────────┐              │           │
│                                           │   gitops-    │◀─────────────┘           │
│                                           │  manifests   │  Update Image Tag        │
│                                           └──────┬───────┘                          │
│                                                  │                                  │
│                                                  ▼                                  │
│   ┌──────────────────────────────────────────────────────────────────────────────┐ │
│   │                             Kubernetes Cluster                               │ │
│   │  ┌─────────────┐     ┌─────────────────────────────────────────────────────┐│ │
│   │  │   Argo CD   │────▶│  ┌─────────┐  ┌─────────┐  ┌─────────┐             ││ │
│   │  │   GitOps    │     │  │   Dev   │  │ Staging │  │  Prod   │             ││ │
│   │  │  Operator   │     │  │ ns:dev  │  │ns:stage │  │ns:prod  │             ││ │
│   │  └─────────────┘     │  └─────────┘  └─────────┘  └─────────┘             ││ │
│   │                      │              AI Inference Pods                      ││ │
│   │  ┌─────────────┐     └─────────────────────────────────────────────────────┘│ │
│   │  │ Prometheus  │                                                            │ │
│   │  │  + Grafana  │◀──── Metrics Collection                                    │ │
│   │  └─────────────┘                                                            │ │
│   └──────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Structure

This project follows the **GitOps repository separation pattern** with two distinct repositories:

```
GitOps-Driven-AI-Inference-Platform/
│
├── gitops-ai-app/              # 📦 Application Source Code
│   ├── src/                    # Python FastAPI application
│   │   ├── main.py             # Application entry point
│   │   ├── config.py           # Configuration management
│   │   ├── api/                # REST API endpoints
│   │   │   └── predict.py      # Prediction endpoint
│   │   ├── models/             # ML model definitions
│   │   │   └── sentiment_model.py
│   │   ├── services/           # Business logic layer
│   │   │   └── inference_service.py
│   │   └── utils/              # Utility functions
│   │       └── preprocessing.py
│   ├── tests/                  # Unit tests
│   ├── Dockerfile              # Multi-stage production build
│   ├── Jenkinsfile             # Main CI pipeline
│   ├── Jenkinsfile.pr          # PR validation pipeline
│   ├── requirements.txt        # Python dependencies
│   └── README.md               # Application documentation
│
├── gitops-manifests/           # 🎯 Kubernetes Manifests (GitOps)
│   ├── argocd/                 # Argo CD configuration
│   │   ├── root-app.yaml       # App-of-Apps bootstrap
│   │   └── projects.yaml       # RBAC definitions
│   ├── apps/                   # Application manifests
│   │   └── ai-inference/
│   │       ├── base/           # Base Kustomize configs
│   │       │   ├── deployment.yaml
│   │       │   ├── service.yaml
│   │       │   ├── hpa.yaml
│   │       │   └── kustomization.yaml
│   │       └── overlays/       # Environment overlays
│   │           ├── dev/
│   │           ├── staging/
│   │           └── prod/
│   ├── monitoring/             # Observability stack
│   │   ├── prometheus/
│   │   └── grafana/
│   └── README.md               # Manifests documentation
│
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.11+ | Application runtime |
| Docker | 24+ | Containerization |
| kubectl | 1.28+ | Kubernetes CLI |
| Argo CD | 2.8+ | GitOps operator |
| Jenkins | 2.400+ | CI/CD pipeline |

### 1️⃣ Local Development

```bash
# Clone the repository
git clone https://github.com/your-org/GitOps-Driven-AI-Inference-Platform.git
cd GitOps-Driven-AI-Inference-Platform/gitops-ai-app

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2️⃣ Docker Build & Run

```bash
cd gitops-ai-app

# Build the Docker image
docker build -t ai-inference:latest .

# Run the container
docker run -p 8000:8000 --name ai-inference ai-inference:latest

# Test the API
curl http://localhost:8000/health
```

### 3️⃣ Deploy to Kubernetes with Argo CD

```bash
# Apply Argo CD projects and root application
kubectl apply -f gitops-manifests/argocd/projects.yaml
kubectl apply -f gitops-manifests/argocd/root-app.yaml

# Verify deployment
argocd app list
argocd app get ai-inference-dev
```

---

## 📡 API Reference

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message and API info |
| `/health` | GET | Liveness probe endpoint |
| `/ready` | GET | Readiness probe endpoint |
| `/metrics` | GET | Prometheus metrics |
| `/api/v1/predict` | POST | Single text prediction |
| `/api/v1/predict/batch` | POST | Batch text predictions |
| `/docs` | GET | Swagger UI (dev mode) |

### Example: Single Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing! I love it!"}'
```

**Response:**
```json
{
  "success": true,
  "result": {
    "text": "This product is amazing! I love it!",
    "label": "POSITIVE",
    "confidence": 0.95,
    "sentiment_score": 0.89,
    "processing_time_ms": 23.5
  },
  "model": "sentiment-v1",
  "timestamp": "2026-01-01T10:30:00Z",
  "request_id": "abc123-def456"
}
```

### Example: Batch Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great service!", "Terrible experience.", "It was okay."]}'
```

---

## 🔄 CI/CD Pipeline

### Pipeline Stages

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Checkout   │───▶│ Unit Tests  │───▶│ Build Image │───▶│ Push Image  │───▶│ Update GitOps│
│             │    │  + Lint     │    │  (Docker)   │    │ (Registry)  │    │  Manifests  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Automated Workflow

1. **Developer pushes code** to `gitops-ai-app` repository
2. **Jenkins triggers** CI pipeline automatically
3. **Tests run** including unit tests and linting
4. **Docker image built** using multi-stage Dockerfile
5. **Image pushed** to container registry with versioned tag
6. **GitOps manifests updated** with new image tag
7. **Argo CD detects** the change and syncs to cluster
8. **Rolling update** deploys new version with zero downtime

---

## 🌍 Environments

| Environment | Namespace | Replicas | Auto-Sync | HPA | Ingress |
|-------------|-----------|----------|-----------|-----|---------|
| **Dev** | `ai-inference-dev` | 1 | ✅ Yes | ❌ | ❌ |
| **Staging** | `ai-inference-staging` | 2 | ✅ Yes | ❌ | ❌ |
| **Production** | `ai-inference-prod` | 3 | ⚠️ Manual | ✅ | ✅ |

### Environment Promotion

```bash
# Promote from dev to staging
git checkout main
# Update staging overlay with new image tag
git commit -am "Promote v1.2.3 to staging"
git push

# Promote from staging to production (manual approval)
argocd app sync ai-inference-prod
```

---

## 📊 Monitoring & Observability

### Metrics Available

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests by method/endpoint/status |
| `http_request_duration_seconds` | Histogram | Request latency distribution |
| `predictions_total` | Counter | Total predictions by status |
| `prediction_duration_seconds` | Histogram | Inference latency |
| `model_load_time_seconds` | Gauge | Model loading time |

### Grafana Dashboards

Pre-configured dashboards are available in `gitops-manifests/monitoring/grafana/dashboards/`:

- **AI Inference Dashboard** - Request rates, latency, error rates
- **Resource Usage** - CPU, memory, pod counts
- **Model Performance** - Prediction accuracy, confidence distributions

---

## 🧪 Testing

```bash
cd gitops-ai-app

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py -v
```

---

## 🔐 Security Features

- ✅ **Non-root container** - Application runs as unprivileged user
- ✅ **Read-only filesystem** - Immutable container runtime
- ✅ **Resource limits** - CPU and memory constraints defined
- ✅ **Health probes** - Liveness and readiness checks
- ✅ **Network policies** - Namespace isolation (production)
- ✅ **Secrets management** - Kubernetes secrets for sensitive data
- ✅ **RBAC** - Role-based access control for Argo CD

---

## 📚 Documentation

| Document | Location | Description |
|----------|----------|-------------|
| Application README | [gitops-ai-app/README.md](gitops-ai-app/README.md) | Application development guide |
| Manifests README | [gitops-manifests/README.md](gitops-manifests/README.md) | Kubernetes deployment guide |
| API Documentation | `/docs` endpoint | Interactive Swagger UI |

---

## 🛠️ Technology Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.11 |
| **Framework** | FastAPI |
| **ML Library** | Transformers / scikit-learn |
| **Container** | Docker (multi-stage) |
| **Orchestration** | Kubernetes 1.28+ |
| **GitOps** | Argo CD |
| **CI/CD** | Jenkins |
| **Monitoring** | Prometheus + Grafana |
| **Config Management** | Kustomize |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **AI Platform Team** - *Initial work*

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Argo CD](https://argoproj.github.io/cd/) - Declarative GitOps CD
- [Kubernetes](https://kubernetes.io/) - Container orchestration
- [Prometheus](https://prometheus.io/) - Monitoring system

---

<p align="center">
  Made with ❤️ using GitOps principles
</p>
