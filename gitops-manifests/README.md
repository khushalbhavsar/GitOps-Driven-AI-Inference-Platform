# 🚀 GitOps Manifests Repository

[![Argo CD](https://img.shields.io/badge/Argo%20CD-Synced-green)](https://argocd.example.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-blue)](https://kubernetes.io)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 Overview

This is the **GitOps Repository** for the AI Inference Platform. It contains:

- 🎯 **Argo CD Applications** - App-of-Apps configuration
- ☸️ **Kubernetes Manifests** - Kustomize-based deployments
- 📊 **Monitoring Stack** - Prometheus & Grafana configuration

> ⚠️ This repository does NOT contain application code. See [gitops-ai-app](../gitops-ai-app) for the application source.

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              GitOps Flow                                     │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   Code Push → Jenkins CI → Docker Push → Git Commit → Argo CD → K8s Deploy │
│                                                                              │
│   ┌─────────┐     ┌─────────┐     ┌─────────────────┐     ┌──────────────┐  │
│   │ gitops- │     │ Jenkins │     │ gitops-manifests│     │  Kubernetes  │  │
│   │ ai-app  │────▶│   CI    │────▶│    (this repo)  │────▶│   Cluster    │  │
│   └─────────┘     └─────────┘     └─────────────────┘     └──────────────┘  │
│                                          │                        ▲         │
│                                          │    ┌───────────┐       │         │
│                                          └───▶│  Argo CD  │───────┘         │
│                                               └───────────┘                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

## 📁 Repository Structure

```
gitops-manifests/
├── argocd/
│   ├── root-app.yaml           # App-of-Apps bootstrap
│   └── projects.yaml           # RBAC & project definitions
│
├── apps/
│   └── ai-inference/
│       ├── base/               # Base Kubernetes manifests
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   ├── hpa.yaml
│       │   └── kustomization.yaml
│       │
│       └── overlays/           # Environment-specific configs
│           ├── dev/
│           ├── staging/
│           └── prod/
│
├── monitoring/
│   ├── prometheus/
│   │   └── values.yaml         # Prometheus Helm values
│   └── grafana/
│       └── dashboards/         # Custom dashboards
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Kubernetes cluster (1.28+)
- Argo CD installed
- kubectl configured

### Bootstrap Argo CD

```bash
# Apply the root application
kubectl apply -f argocd/projects.yaml
kubectl apply -f argocd/root-app.yaml

# Verify applications
argocd app list
```

### Manual Sync (if needed)

```bash
# Sync specific environment
argocd app sync ai-inference-dev
argocd app sync ai-inference-staging
argocd app sync ai-inference-prod
```

## 🌍 Environments

| Environment | Namespace | Auto-Sync | Replicas | Purpose |
|-------------|-----------|-----------|----------|---------|
| **dev** | ai-inference-dev | ✅ Yes | 1 | Development/testing |
| **staging** | ai-inference-staging | ✅ Yes | 2 | Pre-production |
| **prod** | ai-inference-prod | ❌ Manual | 3-20 | Production |

## 🔧 Kustomize Usage

### Preview manifests

```bash
# Development
kubectl kustomize apps/ai-inference/overlays/dev

# Production
kubectl kustomize apps/ai-inference/overlays/prod
```

### Apply locally (testing)

```bash
kubectl apply -k apps/ai-inference/overlays/dev --dry-run=client
```

## 📊 Monitoring

### Prometheus

Prometheus is deployed using the kube-prometheus-stack Helm chart:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm upgrade --install prometheus prometheus-community/kube-prometheus-stack \
  -n monitoring -f monitoring/prometheus/values.yaml
```

### Grafana Dashboards

Custom dashboards are automatically loaded from ConfigMaps with the label `grafana_dashboard: "1"`.

### Alerts

Pre-configured alerts for AI Inference service:
- 🔴 `AIInferenceHighErrorRate` - Error rate > 5%
- 🟡 `AIInferenceHighLatency` - P95 latency > 2s
- 🟡 `AIInferenceLowReplicas` - Available replicas < 2
- 🟡 `AIInferencePodNotReady` - Pod unhealthy

## 🔒 Security

### RBAC

Projects are configured with least-privilege access:

- **developers**: Can sync dev/staging, view all
- **admins**: Full control over all environments

### Network Policies

All applications have network policies that:
- Allow ingress from NGINX Ingress Controller
- Allow ingress from Prometheus for metrics
- Allow egress for DNS and HTTPS only

## 📝 Making Changes

### Update Image Tag

CI pipeline updates the image tag automatically. Manual update:

```bash
# Edit the kustomization.yaml
cd apps/ai-inference/base
sed -i 's/newTag:.*/newTag: v1.2.3/' kustomization.yaml

# Commit and push
git add .
git commit -m "chore: update ai-inference to v1.2.3"
git push
```

### Add New Environment

1. Create new overlay directory
2. Add kustomization.yaml with environment-specific patches
3. Add Argo CD Application in `argocd/root-app.yaml`

### Modify Resources

1. Edit appropriate files in `base/` or `overlays/`
2. Test with `kubectl kustomize`
3. Commit and push
4. Argo CD will auto-sync (or manual for prod)

## 🔄 Rollback

### Using Argo CD UI

1. Open Argo CD dashboard
2. Select the application
3. Click "History & Rollback"
4. Select previous revision

### Using CLI

```bash
# List revisions
argocd app history ai-inference-prod

# Rollback to specific revision
argocd app rollback ai-inference-prod 5
```

### Using Git

```bash
# Revert the commit
git revert HEAD
git push

# Argo CD will sync to previous state
```

## 📋 CI/CD Integration

The CI pipeline (Jenkins) updates this repository:

1. **Build** - Creates Docker image
2. **Push** - Pushes to container registry
3. **Update** - Commits new image tag to this repo
4. **Sync** - Argo CD detects change and deploys

### Commit Message Format

```
chore: update ai-inference image to <tag>

Build: <jenkins-build-url>
Commit: <app-repo-commit>
```

## 🛠️ Troubleshooting

### Application Not Syncing

```bash
# Check Argo CD application status
argocd app get ai-inference-dev

# Force refresh
argocd app refresh ai-inference-dev

# Check for drift
argocd app diff ai-inference-dev
```

### Sync Failed

```bash
# Get detailed sync status
argocd app sync ai-inference-dev --dry-run

# Check Kubernetes events
kubectl get events -n ai-inference-dev --sort-by='.lastTimestamp'
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.
