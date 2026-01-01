# 🚀 GitOps-Driven AI Inference Platform

[![GitHub](https://img.shields.io/badge/GitHub-Code-181717?logo=github&logoColor=white)](https://github.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerization-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Jenkins](https://img.shields.io/badge/Jenkins-CI-D24939?logo=jenkins&logoColor=white)](https://www.jenkins.io/)
[![OWASP](https://img.shields.io/badge/OWASP-Security-000000?logo=owasp&logoColor=white)](https://owasp.org/)
[![SonarQube](https://img.shields.io/badge/SonarQube-Quality-4E9BCD?logo=sonarqube&logoColor=white)](https://www.sonarqube.org/)
[![Trivy](https://img.shields.io/badge/Trivy-Scanner-1904DA?logo=aqua&logoColor=white)](https://trivy.dev/)
[![ArgoCD](https://img.shields.io/badge/ArgoCD-CD-EF7B4D?logo=argo&logoColor=white)](https://argoproj.github.io/cd/)
[![Redis](https://img.shields.io/badge/Redis-Caching-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![AWS EKS](https://img.shields.io/badge/AWS%20EKS-Kubernetes-FF9900?logo=amazoneks&logoColor=white)](https://aws.amazon.com/eks/)
[![Helm](https://img.shields.io/badge/Helm-Monitoring-0F1689?logo=helm&logoColor=white)](https://helm.sh/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

A production-ready **GitOps-Driven AI Inference Platform** that demonstrates modern cloud-native DevSecOps practices. This platform provides real-time sentiment analysis using a FastAPI-based microservice, deployed to AWS EKS via GitOps principles using Argo CD, with comprehensive CI/CD pipelines, security scanning, and monitoring.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| ![GitHub](https://img.shields.io/badge/-GitHub-181717?logo=github&logoColor=white) | Source Code Management |
| ![Docker](https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white) | Containerization |
| ![Jenkins](https://img.shields.io/badge/-Jenkins-D24939?logo=jenkins&logoColor=white) | Continuous Integration |
| ![OWASP](https://img.shields.io/badge/-OWASP-000000?logo=owasp&logoColor=white) | Dependency Check |
| ![SonarQube](https://img.shields.io/badge/-SonarQube-4E9BCD?logo=sonarqube&logoColor=white) | Code Quality Analysis |
| ![Trivy](https://img.shields.io/badge/-Trivy-1904DA?logo=aqua&logoColor=white) | Filesystem & Image Scanning |
| ![ArgoCD](https://img.shields.io/badge/-ArgoCD-EF7B4D?logo=argo&logoColor=white) | Continuous Deployment (GitOps) |
| ![Redis](https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white) | Caching Layer |
| ![AWS EKS](https://img.shields.io/badge/-AWS%20EKS-FF9900?logo=amazoneks&logoColor=white) | Kubernetes Cluster |
| ![Helm](https://img.shields.io/badge/-Helm-0F1689?logo=helm&logoColor=white) | Monitoring (Prometheus & Grafana) |

---

## 🔄 Pipeline Architecture

### CI Pipeline - Build and Push Image

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Checkout   │───▶│  SonarQube   │───▶│    OWASP     │───▶│    Trivy     │───▶│ Docker Build │
│    Code      │    │   Analysis   │    │  Dep Check   │    │  FS Scan     │    │   & Push     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### CD Pipeline - Update Application Version

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Trigger    │───▶│ Update Image │───▶│  Git Commit  │
│  from CI     │    │    Tag       │    │   & Push     │
└──────────────┘    └──────────────┘    └──────────────┘
```

### ArgoCD - Deployment on EKS

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  Git Repo    │───▶│   ArgoCD     │───▶│   Sync to    │───▶│  AWS EKS     │
│   Change     │    │   Detect     │    │   Cluster    │    │  Deployment  │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

---

## 📚 Quick Navigation

> **Important:** Below table helps you navigate to the particular tool installation section fast.

| Tech Stack | Installation Guide |
|------------|-------------------|
| Jenkins Master | [Install and configure Jenkins](#-install-and-configure-jenkins-master-machine) |
| eksctl | [Install eksctl](#-install-eksctl-master-machine) |
| ArgoCD | [Install and configure ArgoCD](#-install-and-configure-argocd-master-machine) |
| Jenkins Worker Setup | [Install and configure Jenkins Worker Node](#-setting-up-jenkins-worker-node) |
| OWASP Setup | [Install and configure OWASP](#-configure-owasp) |
| SonarQube | [Install and configure SonarQube](#-install-and-configure-sonarqube-master-machine) |
| Email Notification Setup | [Email notification setup](#-email-notification-setup) |
| Monitoring | [Prometheus and Grafana setup using Helm](#-monitoring-with-prometheus-and-grafana-master-machine) |
| Clean Up | [Clean up resources](#-clean-up) |

---

## 📋 Pre-requisites

> **Note:** This project will be implemented on **N. California region (us-west-1)**.

### Master Machine Setup

Create 1 Master machine on AWS with the following specifications:

| Resource | Specification |
|----------|--------------|
| **CPU** | 2 vCPU |
| **RAM** | 8 GB |
| **Instance Type** | t2.large |
| **Storage** | 29 GB |
| **OS** | Ubuntu |

### Required Security Group Ports

Open the following ports in the security group of the master machine (also attach the same security group to Jenkins worker node):

| Port | Service |
|------|---------|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 465 | SMTPS |
| 6443 | Kubernetes API |
| 8080 | Jenkins |
| 9000 | SonarQube |
| 30000-32767 | NodePort Services |

> **Note:** We are creating this master machine because we will configure Jenkins master, eksctl, and EKS cluster creation from here.

---

## 🐳 Install Docker (Master Machine)

```bash
sudo apt-get update
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu && newgrp docker
```

> **Note:** `newgrp docker` will refresh the group config, hence no need to restart the EC2 machine.

---

## 🔧 Install and Configure Jenkins (Master Machine)

```bash
# Update system and install Java
sudo apt update -y
sudo apt install fontconfig openjdk-17-jre -y

# Add Jenkins repository key
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

# Add Jenkins repository
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt-get update -y
sudo apt-get install jenkins -y
```

Now, access Jenkins Master on the browser on port **8080** and configure it.

---

## ☁️ Create EKS Cluster on AWS (Master Machine)

### Prerequisites
- IAM user with access keys and secret access keys
- AWS CLI configured

### Install AWS CLI

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
aws configure
```

### Install kubectl (Master Machine)

```bash
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin
kubectl version --short --client
```

### Install eksctl (Master Machine)

```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

### Create EKS Cluster (Master Machine)

```bash
eksctl create cluster --name=wanderlust \
                      --region=us-west-1 \
                      --version=1.30 \
                      --without-nodegroup
```

### Associate IAM OIDC Provider (Master Machine)

```bash
eksctl utils associate-iam-oidc-provider \
  --region us-west-1 \
  --cluster wanderlust \
  --approve
```

### Create Nodegroup (Master Machine)

```bash
eksctl create nodegroup --cluster=wanderlust \
                        --region=us-west-1 \
                        --name=wanderlust \
                        --node-type=t2.large \
                        --nodes=2 \
                        --nodes-min=2 \
                        --nodes-max=2 \
                        --node-volume-size=29 \
                        --ssh-access \
                        --ssh-public-key=eks-nodegroup-key
```

> **Note:** Make sure the ssh-public-key `eks-nodegroup-key` is available in your AWS account.

---

## 👷 Setting up Jenkins Worker Node

### Create Jenkins Worker EC2 Instance

Create a new EC2 instance with:
- **CPU:** 2 vCPU
- **RAM:** 8 GB (t2.large)
- **Storage:** 29 GB

### Install Java on Worker Node

```bash
sudo apt update -y
sudo apt install fontconfig openjdk-17-jre -y
```

### Attach IAM Role

1. Create an IAM role with **Administrator Access**
2. Attach it to the Jenkins worker node:
   - Select Jenkins worker node EC2 instance → **Actions** → **Security** → **Modify IAM role**

### Configure AWS CLI (Worker Node)

```bash
sudo su
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
aws configure
```

### Generate SSH Keys (Master Machine)

```bash
ssh-keygen
```

Copy the content of the public key (`~/.ssh/id_rsa.pub`) and paste it into the `~/.ssh/authorized_keys` file of the Jenkins worker node.

### Add Worker Node in Jenkins

1. Go to Jenkins Master → **Manage Jenkins** → **Nodes** → **Add node**
2. Configure the node:

| Setting | Value |
|---------|-------|
| **Name** | Node |
| **Type** | Permanent Agent |
| **Number of executors** | 2 |
| **Remote root directory** | /home/ubuntu |
| **Labels** | Node |
| **Usage** | Only build jobs with label expressions matching this node |
| **Launch method** | Via SSH |
| **Host** | `<public-ip-worker-jenkins>` |
| **Credentials** | Add SSH credentials with private key |
| **Host Key Verification** | Non verifying Verification Strategy |
| **Availability** | Keep this agent online as much as possible |

### Install Docker (Jenkins Worker)

```bash
sudo apt install docker.io -y
sudo usermod -aG docker ubuntu && newgrp docker
```

---

## 📊 Install and Configure SonarQube (Master Machine)

```bash
docker run -itd --name SonarQube-Server -p 9000:9000 sonarqube:lts-community
```

Access SonarQube on `http://<master-ip>:9000`
- **Default Username:** admin
- **Default Password:** admin

---

## 🔍 Install Trivy (Jenkins Worker)

```bash
sudo apt-get install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update -y
sudo apt-get install trivy -y
```

---

## 🎯 Install and Configure ArgoCD (Master Machine)

### Create ArgoCD Namespace

```bash
kubectl create namespace argocd
```

### Apply ArgoCD Manifest

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Verify Pods are Running

```bash
watch kubectl get pods -n argocd
```

### Install ArgoCD CLI

```bash
sudo curl --silent --location -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.4.7/argocd-linux-amd64
sudo chmod +x /usr/local/bin/argocd
```

### Expose ArgoCD Server

```bash
# Check ArgoCD services
kubectl get svc -n argocd

# Change service from ClusterIP to NodePort
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'

# Confirm service is patched
kubectl get svc -n argocd
```

### Get ArgoCD Initial Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

Access ArgoCD on `https://<worker-public-ip>:<nodeport>`
- **Username:** admin
- **Password:** (from above command)

> **Tip:** Go to **User Info** and update your ArgoCD password after first login.

---

## 📧 Email Notification Setup

### Allow SMTP Port

Go to your Jenkins Master EC2 instance and allow port **465** for SMTPS.

### Generate Gmail App Password

> **Important:** Make sure 2-step verification is enabled on your Gmail account.

1. Open Gmail → **Manage your Google Account** → **Security**
2. Search for **App passwords**
3. Create an app password for Jenkins

### Configure Email in Jenkins

1. Go to **Manage Jenkins** → **Credentials** → Add username and password for email notification
2. Go to **Manage Jenkins** → **System** → Search for **Extended E-mail Notification**

Configure the following:
| Setting | Value |
|---------|-------|
| **SMTP Server** | smtp.gmail.com |
| **SMTP Port** | 465 |
| **Credentials** | Your Gmail credentials |
| **Use SSL** | ✅ Enabled |

3. Scroll down and configure **E-mail Notification** section similarly

---

## 🔌 Jenkins Plugins Installation

Go to **Manage Jenkins** → **Plugins** → **Available plugins** and install:

- OWASP Dependency-Check
- SonarQube Scanner
- Docker
- Pipeline: Stage View

### Configure OWASP

1. Go to **Manage Jenkins** → **Tools**
2. Add OWASP Dependency-Check installation
3. Name: `DP-Check`
4. Install automatically: ✅

### Configure SonarQube

#### Create SonarQube Token

1. Login to SonarQube
2. Navigate to **Administration** → **Security** → **Users** → **Token**
3. Generate a new token for Jenkins

#### Add SonarQube Credentials in Jenkins

1. Go to **Manage Jenkins** → **Credentials**
2. Add SonarQube token as **Secret text**

#### Configure SonarQube Scanner

1. Go to **Manage Jenkins** → **Tools**
2. Add SonarQube Scanner installation

#### Configure SonarQube Server

1. Go to **Manage Jenkins** → **System**
2. Search for **SonarQube installations**
3. Add your SonarQube server URL

### Configure SonarQube Webhook

1. Login to SonarQube
2. Go to **Administration** → **Webhooks** → **Create**
3. URL: `http://<jenkins-ip>:8080/sonarqube-webhook/`

### Add GitHub Credentials

1. Go to **Manage Jenkins** → **Credentials**
2. Add GitHub credentials with Personal Access Token as password

### Add Docker Hub Credentials

1. Go to **Manage Jenkins** → **Credentials**
2. Add Docker Hub username and password/token

---

## 🏗️ Pipeline Setup

### Create CI Pipeline

1. Create a new Pipeline job named `AI-Inference-CI`
2. Configure pipeline from SCM (Git)
3. Script path: `Jenkinsfile`

### Create CD Pipeline

1. Create a new Pipeline job named `AI-Inference-CD`
2. Configure pipeline from SCM (Git)
3. Script path: `Jenkinsfile.cd`
4. Enable: **Build after other projects are built** → `AI-Inference-CI`

### Fix Docker Socket Permission (Jenkins Worker)

```bash
chmod 777 /var/run/docker.sock
```

---

## 🔗 Connect EKS Cluster to ArgoCD

### Login to ArgoCD from CLI

```bash
argocd login <argocd-url>:<port> --username admin
```

### Check Available Clusters

```bash
argocd cluster list
```

### Get Cluster Context Name

```bash
kubectl config get-contexts
```

### Add Cluster to ArgoCD

```bash
argocd cluster add <cluster-context-name> --name wanderlust-eks-cluster
```

### Verify in ArgoCD Console

Go to **Settings** → **Clusters** and verify your cluster is added.

### Connect Git Repository

1. Go to **Settings** → **Repositories** → **Connect Repo**
2. Add your GitOps manifests repository

### Create ArgoCD Application

1. Go to **Applications** → **New App**
2. Configure:

| Setting | Value |
|---------|-------|
| **Application Name** | ai-inference |
| **Project** | default |
| **Sync Policy** | Automatic |
| **Auto-Create Namespace** | ✅ |
| **Repository URL** | Your GitOps repo URL |
| **Path** | apps/ai-inference/overlays/dev |
| **Cluster URL** | Your EKS cluster |
| **Namespace** | ai-inference |

---

## 📊 Monitoring with Prometheus and Grafana (Master Machine)

### Install Helm

```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

### Add Helm Repositories

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

### Create Prometheus Namespace

```bash
kubectl create namespace prometheus
kubectl get ns
```

### Install Prometheus Stack

```bash
helm install stable prometheus-community/kube-prometheus-stack -n prometheus
```

### Verify Installation

```bash
kubectl get pods -n prometheus
kubectl get svc -n prometheus
```

### Expose Prometheus and Grafana

#### Expose Prometheus

```bash
kubectl edit svc stable-kube-prometheus-sta-prometheus -n prometheus
```

Change `type: ClusterIP` to `type: NodePort`

#### Expose Grafana

```bash
kubectl edit svc stable-grafana -n prometheus
```

Change `type: ClusterIP` to `type: NodePort`

### Verify Services

```bash
kubectl get svc -n prometheus
```

### Get Grafana Password

```bash
kubectl get secret --namespace prometheus stable-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

- **Username:** admin

### Access Dashboards

- **Prometheus:** `http://<worker-ip>:<prometheus-nodeport>`
- **Grafana:** `http://<worker-ip>:<grafana-nodeport>`

### Recommended Grafana Dashboards

Import these dashboard IDs:
- **3119** - Kubernetes Cluster Monitoring
- **6417** - Kubernetes Pod Monitoring
- **15757** - Kubernetes Views (Global)

---

## 🧹 Clean Up

### Delete EKS Cluster

```bash
eksctl delete cluster --name=wanderlust --region=us-west-1
```

### Delete EC2 Instances

1. Terminate Jenkins Master EC2 instance
2. Terminate Jenkins Worker EC2 instance

### Clean Up Docker Resources

```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
```

---

## 📁 Repository Structure

```
GitOps-Driven-AI-Inference-Platform/
│
├── gitops-ai-app/              # 📦 Application Source Code
│   ├── src/                    # Python FastAPI application
│   │   ├── main.py             # Application entry point
│   │   ├── config.py           # Configuration management
│   │   ├── api/                # REST API endpoints
│   │   ├── models/             # ML model definitions
│   │   ├── services/           # Business logic layer
│   │   └── utils/              # Utility functions
│   ├── tests/                  # Unit tests
│   ├── Dockerfile              # Multi-stage production build
│   ├── Jenkinsfile             # CI pipeline
│   ├── Jenkinsfile.pr          # PR validation pipeline
│   └── requirements.txt        # Python dependencies
│
├── gitops-manifests/           # 🎯 Kubernetes Manifests (GitOps)
│   ├── argocd/                 # Argo CD configuration
│   │   ├── root-app.yaml       # App-of-Apps bootstrap
│   │   └── projects.yaml       # RBAC definitions
│   ├── apps/                   # Application manifests
│   │   └── ai-inference/
│   │       ├── base/           # Base Kustomize configs
│   │       └── overlays/       # Environment overlays
│   │           ├── dev/
│   │           ├── staging/
│   │           └── prod/
│   └── monitoring/             # Observability stack
│
└── README.md                   # This file
```

---

## 🌍 Environments

| Environment | Namespace | Replicas | Auto-Sync | Purpose |
|-------------|-----------|----------|-----------|---------|
| **Dev** | ai-inference-dev | 1 | ✅ Yes | Development/Testing |
| **Staging** | ai-inference-staging | 2 | ✅ Yes | Pre-production |
| **Production** | ai-inference-prod | 3 | ⚠️ Manual | Live environment |

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/health` | GET | Liveness probe |
| `/ready` | GET | Readiness probe |
| `/metrics` | GET | Prometheus metrics |
| `/api/v1/predict` | POST | Single prediction |
| `/api/v1/predict/batch` | POST | Batch predictions |

---

## 🔐 Security Features

- ✅ **OWASP Dependency Check** - Vulnerability scanning for dependencies
- ✅ **Trivy Scanner** - Container and filesystem scanning
- ✅ **SonarQube** - Code quality and security analysis
- ✅ **Non-root containers** - Security best practices
- ✅ **Resource limits** - CPU and memory constraints
- ✅ **Network policies** - Namespace isolation
- ✅ **RBAC** - Role-based access control

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

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Argo CD](https://argoproj.github.io/cd/) - Declarative GitOps CD
- [Jenkins](https://www.jenkins.io/) - CI/CD automation
- [Prometheus](https://prometheus.io/) - Monitoring system
- [Grafana](https://grafana.com/) - Visualization platform
- [AWS EKS](https://aws.amazon.com/eks/) - Managed Kubernetes

---

<p align="center">
  Made with ❤️ using GitOps & DevSecOps principles
</p>
