# 🚀 GitOps-Driven AI Inference Platform

<p align="center">
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white" alt="Jenkins"/>
  <img src="https://img.shields.io/badge/OWASP-000000?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP"/>
  <img src="https://img.shields.io/badge/SonarQube-4E9BCD?style=for-the-badge&logo=sonarqube&logoColor=white" alt="SonarQube"/>
  <img src="https://img.shields.io/badge/Trivy-1904DA?style=for-the-badge&logo=aquasecurity&logoColor=white" alt="Trivy"/>
  <img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white" alt="ArgoCD"/>
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis"/>
  <img src="https://img.shields.io/badge/AWS_EKS-FF9900?style=for-the-badge&logo=amazoneks&logoColor=white" alt="AWS EKS"/>
  <img src="https://img.shields.io/badge/Helm-0F1689?style=for-the-badge&logo=helm&logoColor=white" alt="Helm"/>
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Tech Stack](#️-tech-stack)
- [Pipeline Architecture](#-pipeline-architecture)
- [Quick Start](#-quick-start)
- [Application Setup](#-application-setup)
- [Jenkins Configuration](#️-jenkins-configuration)
- [ArgoCD Deployment](#-argocd-deployment)
- [API Reference](#-api-reference)
- [Project Structure](#-project-structure)
- [Environments](#-environments)
- [Documentation](#-documentation)

---

## 📖 Overview

A production-ready **GitOps-Driven AI Inference Platform** for real-time sentiment analysis. Built with **FastAPI** and **Python 3.11**, deployed to **AWS EKS** using GitOps principles with **Argo CD**, featuring comprehensive CI/CD pipelines with security scanning.

### Key Features

- 🤖 **AI Sentiment Analysis** - Real-time text classification using DistilBERT
- 🔄 **GitOps Workflow** - Automated deployments via Argo CD
- 🔒 **Security Scanning** - OWASP, Trivy, Bandit, Safety
- 📊 **Code Quality** - SonarQube, Flake8, Black, MyPy
- 📈 **Monitoring** - Prometheus metrics & Grafana dashboards
- 🐳 **Multi-stage Docker** - Production-optimized container builds

---

## 🛠️ Tech Stack

| Technology | Purpose |
|:----------:|---------|
| **GitHub** | Source Code Management |
| **Docker** | Containerization (Python 3.11-slim) |
| **Jenkins** | CI Pipeline (Build, Test, Push) |
| **OWASP** | Dependency Vulnerability Check |
| **SonarQube** | Code Quality Analysis |
| **Trivy** | Container & Filesystem Scanning |
| **ArgoCD** | GitOps Continuous Deployment |
| **Redis** | Caching Layer |
| **AWS EKS** | Kubernetes Cluster (v1.30) |
| **Helm** | Prometheus & Grafana Deployment |

---

## 🔄 Pipeline Architecture

### CI Pipeline (Jenkinsfile)

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Checkout │──▶│  Unit    │──▶│  Code    │──▶│ Security │──▶│  Docker  │──▶│  Push    │
│   Code   │   │  Tests   │   │ Quality  │   │   Scan   │   │  Build   │   │  Image   │
└──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘
                    │              │              │
                    ▼              ▼              ▼
               pytest +      Flake8 +       Bandit +
               coverage      Black +        Safety +
                             MyPy          Trivy
```

### CD Pipeline (GitOps Update)

```
┌──────────┐   ┌──────────────────┐   ┌──────────┐
│   CI     │──▶│ Update Image Tag │──▶│   Git    │
│ Success  │   │ in Kustomization │   │   Push   │
└──────────┘   └──────────────────┘   └──────────┘
```

### ArgoCD Sync

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────────────┐
│  GitOps  │──▶│  ArgoCD  │──▶│  Sync    │──▶│  EKS Cluster   │
│   Repo   │   │  Detect  │   │  Apply   │   │  (3 Envs)      │
└──────────┘   └──────────┘   └──────────┘   └────────────────┘
```

---

## 🚀 Quick Start

### Infrastructure Setup

> **📘 Complete EC2 & Infrastructure Setup Guide:** [docs/EC2_SETUP_GUIDE.md](docs/EC2_SETUP_GUIDE.md)

The infrastructure setup guide includes step-by-step instructions for:

| Step | Component | Description |
|:----:|-----------|-------------|
| 1 | EC2 Instances | Create Master & Worker machines |
| 2 | Docker | Install container runtime |
| 3 | Jenkins | CI/CD server installation |
| 4-7 | AWS Tools | AWS CLI, kubectl, eksctl |
| 8 | EKS Cluster | Create Kubernetes cluster |
| 9 | Jenkins Worker | Configure build agent |
| 10 | SonarQube | Code quality server |
| 11 | Trivy | Security scanner |
| 12 | ArgoCD | GitOps deployment tool |
| 13 | Monitoring | Prometheus & Grafana |

👉 **[Start Infrastructure Setup](docs/EC2_SETUP_GUIDE.md)**

---

## 🐍 Application Setup

### Clone Repository

```bash
git clone https://github.com/your-org/GitOps-Driven-AI-Inference-Platform.git
cd GitOps-Driven-AI-Inference-Platform/gitops-ai-app
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
cd gitops-ai-app

# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ \
    --cov=src \
    --cov-report=xml \
    --cov-report=html \
    -v
```

### Code Quality Checks

```bash
# Install tools
pip install flake8 black mypy bandit safety

# Linting
flake8 src/ --max-line-length=100 --ignore=E501,W503
black --check src/ --line-length=100
mypy src/ --ignore-missing-imports

# Security scan
bandit -r src/ -f json -o bandit-report.json
safety check -r requirements.txt
```

### Docker Build

```bash
cd gitops-ai-app

# Build production image
docker build --target production -t ai-inference:latest .

# Build development image
docker build --target development -t ai-inference:dev .

# Run container
docker run -p 8000:8000 \
    -e LOG_LEVEL=INFO \
    -e WORKERS=4 \
    --name ai-inference \
    ai-inference:latest

# Test health endpoint
curl http://localhost:8000/health
```

---

## ⚙️ Jenkins Configuration

### Required Plugins

- ✅ OWASP Dependency-Check
- ✅ SonarQube Scanner
- ✅ Docker Pipeline
- ✅ Pipeline: Stage View
- ✅ Git

### Add Credentials

| ID | Type | Description |
|----|------|-------------|
| `docker-registry-url` | Secret text | Docker registry URL |
| `docker-registry-credentials` | Username/Password | Docker Hub login |
| `gitops-repo-credentials` | Username/Password | GitHub PAT |
| `sonarqube-token` | Secret text | SonarQube token |

### Configure Tools

**Manage Jenkins** → **Tools**:

| Tool | Name | Install |
|------|------|---------|
| Dependency-Check | `DP-Check` | Auto |
| SonarQube Scanner | `SonarScanner` | Auto |

### SonarQube Webhook

**SonarQube** → **Administration** → **Webhooks** → **Create**
- URL: `http://<jenkins-ip>:8080/sonarqube-webhook/`

### Create Pipeline Jobs

#### CI Pipeline (ai-inference-ci)

| Setting | Value |
|---------|-------|
| Pipeline | Pipeline script from SCM |
| SCM | Git |
| Repository | `https://github.com/your-org/gitops-ai-app.git` |
| Script Path | `Jenkinsfile` |

### Email Notification Setup

#### Gmail App Password

1. Enable **2-Step Verification**
2. Gmail → **Manage Account** → **Security** → **App passwords**
3. Create password for Jenkins

#### Jenkins Configuration

**Manage Jenkins** → **System** → **Extended E-mail Notification**

| Setting | Value |
|---------|-------|
| SMTP Server | smtp.gmail.com |
| SMTP Port | 465 |
| Use SSL | ✅ |

---

## 🎯 ArgoCD Deployment

### Deploy Applications

```bash
# Apply ArgoCD projects
kubectl apply -f gitops-manifests/argocd/projects.yaml

# Apply root application (App of Apps)
kubectl apply -f gitops-manifests/argocd/root-app.yaml
```

### ArgoCD Applications

| Application | Namespace | Path | Sync |
|-------------|-----------|------|------|
| `ai-inference-dev` | ai-inference-dev | `apps/ai-inference/overlays/dev` | Auto |
| `ai-inference-staging` | ai-inference-staging | `apps/ai-inference/overlays/staging` | Auto |
| `ai-inference-prod` | ai-inference-prod | `apps/ai-inference/overlays/prod` | Manual |
| `monitoring` | monitoring | `monitoring` | Auto |

### Verify Deployment

```bash
# Check ArgoCD apps
argocd app list

# Check pods
kubectl get pods -n ai-inference-dev
kubectl get pods -n ai-inference-staging
kubectl get pods -n ai-inference-prod

# Check services
kubectl get svc -n ai-inference-dev
```

---

## 📡 API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Liveness probe |
| GET | `/ready` | Readiness probe |
| GET | `/metrics` | Prometheus metrics |
| POST | `/api/v1/predict` | Single prediction |
| POST | `/api/v1/predict/batch` | Batch predictions |

### Example: Single Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "This product is amazing!"}'
```

**Response:**
```json
{
  "success": true,
  "result": {
    "text": "This product is amazing!",
    "label": "POSITIVE",
    "confidence": 0.95,
    "sentiment_score": 0.89,
    "processing_time_ms": 23.5
  },
  "model": "distilbert-base-uncased-finetuned-sst-2-english",
  "timestamp": "2026-01-01T10:30:00Z",
  "request_id": "abc123"
}
```

### Example: Batch Prediction

```bash
curl -X POST http://localhost:8000/api/v1/predict/batch \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Great!", "Terrible!", "Okay"]}'
```

### Prometheus Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | Request latency |
| `predictions_total` | Counter | Total predictions |
| `prediction_duration_seconds` | Histogram | Inference time |

---

## 📁 Project Structure

```
GitOps-Driven-AI-Inference-Platform/
│
├── gitops-ai-app/                      # Application Repository
│   ├── src/
│   │   ├── main.py                     # FastAPI app (uvicorn)
│   │   ├── config.py                   # Environment config
│   │   ├── api/
│   │   │   └── predict.py              # /api/v1/predict endpoint
│   │   ├── models/
│   │   │   └── sentiment_model.py      # DistilBERT model
│   │   ├── services/
│   │   │   └── inference_service.py    # ML inference logic
│   │   └── utils/
│   │       └── preprocessing.py        # Text preprocessing
│   ├── tests/
│   │   ├── test_api.py                 # API tests
│   │   └── test_inference.py           # Inference tests
│   ├── Dockerfile                      # Multi-stage build
│   ├── Jenkinsfile                     # CI pipeline
│   ├── Jenkinsfile.pr                  # PR validation
│   ├── requirements.txt                # Python deps
│   └── pyproject.toml                  # Project config
│
├── gitops-manifests/                   # GitOps Repository
│   ├── argocd/
│   │   ├── root-app.yaml               # App of Apps
│   │   └── projects.yaml               # RBAC & projects
│   ├── apps/
│   │   └── ai-inference/
│   │       ├── base/
│   │       │   ├── deployment.yaml
│   │       │   ├── service.yaml
│   │       │   ├── hpa.yaml
│   │       │   └── kustomization.yaml
│   │       └── overlays/
│   │           ├── dev/
│   │           ├── staging/
│   │           └── prod/
│   └── monitoring/
│       ├── prometheus/
│       └── grafana/
│
├── docs/
│   └── EC2_SETUP_GUIDE.md              # Infrastructure setup guide
│
└── README.md
```

---

## 🌍 Environments

| Environment | Namespace | Replicas | Resources | Sync |
|-------------|-----------|----------|-----------|------|
| **Dev** | ai-inference-dev | 1 | 256m/512Mi | Auto |
| **Staging** | ai-inference-staging | 2 | 500m/1Gi | Auto |
| **Production** | ai-inference-prod | 3 | 1000m/2Gi | Manual |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [EC2 Setup Guide](docs/EC2_SETUP_GUIDE.md) | Complete infrastructure setup (EC2, Docker, Jenkins, EKS, ArgoCD, Monitoring) |
| [gitops-ai-app/README.md](gitops-ai-app/README.md) | Application documentation |
| [gitops-manifests/README.md](gitops-manifests/README.md) | Kubernetes manifests guide |

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <b>🚀 GitOps-Driven AI Inference Platform</b><br>
  Built with FastAPI • Deployed with ArgoCD • Secured with DevSecOps
</p>
