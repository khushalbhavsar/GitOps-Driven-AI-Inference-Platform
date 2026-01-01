# 🖥️ EC2 Infrastructure Setup Guide

Complete step-by-step guide for setting up the GitOps-Driven AI Inference Platform infrastructure on AWS EC2.

---

## 📋 Table of Contents

- [Pre-requisites](#-pre-requisites)
- [Step 1: Create EC2 Instances](#-step-1-create-ec2-instances)
- [Step 2: Install Docker](#-step-2-install-docker-master-machine)
- [Step 3: Install Jenkins](#-step-3-install-jenkins-master-machine)
- [Step 4: Clone Project Repository](#-step-4-clone-project-repository)
- [Step 5: Install AWS CLI](#-step-5-install-aws-cli-master-machine)
- [Step 6: Install kubectl](#-step-6-install-kubectl-master-machine)
- [Step 7: Install eksctl](#-step-7-install-eksctl-master-machine)
- [Step 8: Create EKS Cluster](#-step-8-create-eks-cluster)
- [Step 9: Setup Jenkins Worker Node](#-step-9-setup-jenkins-worker-node)
- [Step 10: Install SonarQube](#-step-10-install-sonarqube-master-machine)
- [Step 11: Install Trivy](#-step-11-install-trivy-jenkins-worker)
- [Step 12: Install ArgoCD](#-step-12-install-argocd-master-machine)
- [Step 13: Install Helm & Monitoring](#-step-13-install-helm--monitoring-master-machine)
- [Verification Checklist](#-verification-checklist)
- [Troubleshooting](#-troubleshooting)
- [Clean Up](#-clean-up)

---

## 📋 Pre-requisites

### AWS Account Requirements

- AWS Account with administrative access
- IAM user with programmatic access (Access Key & Secret Key)
- SSH key pair created in AWS (for EC2 and EKS nodes)

### Region

> **Note:** This guide uses **us-west-1 (N. California)** region. Adjust commands if using a different region.

---

## 🖥️ Step 1: Create EC2 Instances

### Master Machine Specifications

| Setting | Value |
|---------|-------|
| **AMI** | Ubuntu 22.04 LTS |
| **Instance Type** | t2.large |
| **vCPU** | 2 |
| **RAM** | 8 GB |
| **Storage** | 29 GB (gp2) |
| **Key Pair** | Your SSH key |
| **Name** | `jenkins-master` |

### Worker Machine Specifications

| Setting | Value |
|---------|-------|
| **AMI** | Ubuntu 22.04 LTS |
| **Instance Type** | t2.large |
| **vCPU** | 2 |
| **RAM** | 8 GB |
| **Storage** | 29 GB (gp2) |
| **Key Pair** | Your SSH key |
| **Name** | `jenkins-worker` |

### Security Group Configuration

Create a security group with the following inbound rules:

| Port | Protocol | Source | Description |
|------|----------|--------|-------------|
| 22 | TCP | Your IP | SSH Access |
| 80 | TCP | 0.0.0.0/0 | HTTP |
| 443 | TCP | 0.0.0.0/0 | HTTPS |
| 465 | TCP | 0.0.0.0/0 | SMTPS (Email) |
| 6443 | TCP | 0.0.0.0/0 | Kubernetes API |
| 8000 | TCP | 0.0.0.0/0 | AI Inference App |
| 8080 | TCP | 0.0.0.0/0 | Jenkins |
| 9000 | TCP | 0.0.0.0/0 | SonarQube |
| 30000-32767 | TCP | 0.0.0.0/0 | NodePort Services |

> **Important:** Attach the same security group to both Master and Worker instances.

### Launch Instances

1. Go to **AWS Console** → **EC2** → **Launch Instance**
2. Configure as per specifications above
3. Launch both Master and Worker instances
4. Note down the Public IP addresses

### Connect to Instances

```bash
# Connect to Master
ssh -i "your-key.pem" ubuntu@<master-public-ip>

# Connect to Worker (in a new terminal)
ssh -i "your-key.pem" ubuntu@<worker-public-ip>
```

---

## 🐳 Step 2: Install Docker (Master Machine)

SSH into the Master machine and run:

```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install docker.io -y

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Apply group changes without logout
newgrp docker

# Verify installation
docker --version
docker run hello-world
```

**Expected Output:**
```
Docker version 24.x.x, build xxxxxxx
Hello from Docker!
```

---

## 🔧 Step 3: Install Jenkins (Master Machine)

```bash
# Update system
sudo apt update -y

# Install Java 17 (required for Jenkins)
sudo apt install fontconfig openjdk-17-jre -y

# Verify Java installation
java -version

# Add Jenkins GPG key
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key

# Add Jenkins repository
echo "deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Update and install Jenkins
sudo apt-get update -y
sudo apt-get install jenkins -y

# Start Jenkins service
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Check Jenkins status
sudo systemctl status jenkins
```

### Access Jenkins

1. Open browser: `http://<master-public-ip>:8080`
2. Get initial admin password:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
3. Complete setup wizard
4. Install suggested plugins
5. Create admin user

---

## 📦 Step 4: Clone Project Repository

```bash
# Navigate to home directory
cd ~

# Clone the repository
git clone https://github.com/your-org/GitOps-Driven-AI-Inference-Platform.git

# Navigate to project
cd GitOps-Driven-AI-Inference-Platform

# View project structure
ls -la
```

### Project Structure
```
GitOps-Driven-AI-Inference-Platform/
├── gitops-ai-app/          # Application source code
├── gitops-manifests/       # Kubernetes manifests
├── docs/                   # Documentation
└── README.md
```

---

## ☁️ Step 5: Install AWS CLI (Master Machine)

```bash
# Download AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

# Install unzip if not present
sudo apt install unzip -y

# Unzip and install
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version

# Configure AWS CLI
aws configure
```

### AWS Configure Prompts

```
AWS Access Key ID [None]: YOUR_ACCESS_KEY
AWS Secret Access Key [None]: YOUR_SECRET_KEY
Default region name [None]: us-west-1
Default output format [None]: json
```

### Verify Configuration

```bash
# Test AWS access
aws sts get-caller-identity
```

**Expected Output:**
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/your-user"
}
```

---

## ⚙️ Step 6: Install kubectl (Master Machine)

```bash
# Download kubectl
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/kubectl

# Make executable
chmod +x ./kubectl

# Move to PATH
sudo mv ./kubectl /usr/local/bin

# Verify installation
kubectl version --short --client
```

**Expected Output:**
```
Client Version: v1.19.6
```

---

## 🚀 Step 7: Install eksctl (Master Machine)

```bash
# Download and extract eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

# Move to PATH
sudo mv /tmp/eksctl /usr/local/bin

# Verify installation
eksctl version
```

**Expected Output:**
```
0.x.x
```

---

## ☸️ Step 8: Create EKS Cluster

### Create Cluster (Without Node Group)

```bash
eksctl create cluster \
  --name=ai-inference-cluster \
  --region=us-west-1 \
  --version=1.30 \
  --without-nodegroup
```

> **Note:** This takes approximately 15-20 minutes.

### Associate IAM OIDC Provider

```bash
eksctl utils associate-iam-oidc-provider \
  --region us-west-1 \
  --cluster ai-inference-cluster \
  --approve
```

### Create Node Group

> **Important:** Ensure `eks-nodegroup-key` SSH key exists in AWS EC2 Key Pairs.

```bash
eksctl create nodegroup \
  --cluster=ai-inference-cluster \
  --region=us-west-1 \
  --name=ai-inference-nodes \
  --node-type=t2.large \
  --nodes=2 \
  --nodes-min=2 \
  --nodes-max=2 \
  --node-volume-size=29 \
  --ssh-access \
  --ssh-public-key=eks-nodegroup-key
```

### Verify Cluster

```bash
# Update kubeconfig
aws eks update-kubeconfig --name ai-inference-cluster --region us-west-1

# Check nodes
kubectl get nodes

# Check cluster info
kubectl cluster-info
```

**Expected Output:**
```
NAME                                           STATUS   ROLES    AGE   VERSION
ip-192-168-xx-xx.us-west-1.compute.internal   Ready    <none>   5m    v1.30.x
ip-192-168-xx-xx.us-west-1.compute.internal   Ready    <none>   5m    v1.30.x
```

---

## 👷 Step 9: Setup Jenkins Worker Node

### 9.1 Install Java on Worker

SSH into Worker machine:

```bash
ssh -i "your-key.pem" ubuntu@<worker-public-ip>
```

```bash
# Update and install Java
sudo apt update -y
sudo apt install fontconfig openjdk-17-jre -y

# Verify
java -version
```

### 9.2 Attach IAM Role to Worker

1. Go to **AWS Console** → **EC2** → **Instances**
2. Select `jenkins-worker` instance
3. Click **Actions** → **Security** → **Modify IAM role**
4. Create and attach role with **AdministratorAccess** policy

### 9.3 Install AWS CLI on Worker

```bash
sudo su
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip -y
unzip awscliv2.zip
sudo ./aws/install
aws configure
exit
```

### 9.4 Generate SSH Keys on Master

On Master machine:

```bash
# Generate SSH key pair
ssh-keygen -t rsa -b 4096

# Press Enter for all prompts (default location, no passphrase)

# View public key
cat ~/.ssh/id_rsa.pub
```

Copy the output.

### 9.5 Add Public Key to Worker

On Worker machine:

```bash
# Open authorized_keys
nano ~/.ssh/authorized_keys

# Paste the public key from Master
# Save and exit (Ctrl+X, Y, Enter)

# Set permissions
chmod 600 ~/.ssh/authorized_keys
```

### 9.6 Add Worker Node in Jenkins

1. Go to Jenkins: `http://<master-ip>:8080`
2. Navigate to **Manage Jenkins** → **Nodes** → **New Node**

| Setting | Value |
|---------|-------|
| Node name | `Node` |
| Type | Permanent Agent |
| Number of executors | `2` |
| Remote root directory | `/home/ubuntu` |
| Labels | `Node` |
| Usage | Only build jobs with label expressions matching this node |
| Launch method | Launch agents via SSH |
| Host | `<worker-public-ip>` |
| Credentials | Add new SSH credentials |

#### Add SSH Credentials:
- **Kind:** SSH Username with private key
- **ID:** `jenkins-worker-ssh`
- **Username:** `ubuntu`
- **Private Key:** Enter directly → Paste content of `~/.ssh/id_rsa` from Master

| Setting | Value |
|---------|-------|
| Host Key Verification | Non verifying Verification Strategy |
| Availability | Keep this agent online as much as possible |

3. Click **Save**
4. Verify node is connected (green icon)

### 9.7 Install Docker on Worker

```bash
# Install Docker
sudo apt install docker.io -y

# Add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker

# Fix socket permissions (for Jenkins)
sudo chmod 777 /var/run/docker.sock

# Verify
docker --version
docker run hello-world
```

---

## 📊 Step 10: Install SonarQube (Master Machine)

```bash
# Run SonarQube container
docker run -itd \
  --name SonarQube-Server \
  -p 9000:9000 \
  sonarqube:lts-community

# Check container is running
docker ps

# View logs
docker logs SonarQube-Server
```

### Access SonarQube

1. Open browser: `http://<master-public-ip>:9000`
2. Wait for SonarQube to start (may take 1-2 minutes)
3. Login with default credentials:
   - **Username:** admin
   - **Password:** admin
4. Change password when prompted

### Create SonarQube Token

1. Go to **Administration** → **Security** → **Users**
2. Click on **Tokens** for admin user
3. Generate new token: `jenkins-token`
4. Copy and save the token

---

## 🔍 Step 11: Install Trivy (Jenkins Worker)

SSH into Worker machine:

```bash
# Install dependencies
sudo apt-get install wget apt-transport-https gnupg lsb-release -y

# Add Trivy GPG key
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -

# Add Trivy repository
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list

# Update and install
sudo apt-get update -y
sudo apt-get install trivy -y

# Verify installation
trivy --version
```

### Test Trivy

```bash
# Scan a test image
trivy image python:3.11-slim
```

---

## 🎯 Step 12: Install ArgoCD (Master Machine)

### Create Namespace

```bash
kubectl create namespace argocd
```

### Install ArgoCD

```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### Wait for Pods

```bash
# Watch pods until all are Running
watch kubectl get pods -n argocd

# Press Ctrl+C when all pods are Running/Completed
```

### Install ArgoCD CLI

```bash
# Download ArgoCD CLI
sudo curl --silent --location -o /usr/local/bin/argocd \
  https://github.com/argoproj/argo-cd/releases/download/v2.4.7/argocd-linux-amd64

# Make executable
sudo chmod +x /usr/local/bin/argocd

# Verify
argocd version --client
```

### Expose ArgoCD Server

```bash
# Patch service to NodePort
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'

# Get the NodePort
kubectl get svc argocd-server -n argocd
```

Note the NodePort (e.g., 32xxx).

### Get Initial Password

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

### Access ArgoCD

1. Open browser: `https://<worker-public-ip>:<nodeport>`
2. Accept security warning (self-signed certificate)
3. Login:
   - **Username:** admin
   - **Password:** (from above command)
4. Go to **User Info** → **Update Password**

### Connect Cluster to ArgoCD

```bash
# Login via CLI
argocd login <worker-public-ip>:<nodeport> --username admin --insecure

# Enter password when prompted

# List current clusters
argocd cluster list

# Get cluster context name
kubectl config get-contexts

# Add EKS cluster
argocd cluster add <context-name> --name ai-inference-cluster

# Confirm with 'y' when prompted
```

---

## 📈 Step 13: Install Helm & Monitoring (Master Machine)

### Install Helm

```bash
# Download Helm install script
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3

# Make executable
chmod 700 get_helm.sh

# Install
./get_helm.sh

# Verify
helm version
```

### Add Helm Repositories

```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### Create Prometheus Namespace

```bash
kubectl create namespace prometheus
```

### Install Prometheus Stack

```bash
helm install stable prometheus-community/kube-prometheus-stack -n prometheus

# Wait for pods
watch kubectl get pods -n prometheus
```

### Expose Prometheus & Grafana

```bash
# Expose Prometheus
kubectl patch svc stable-kube-prometheus-sta-prometheus -n prometheus \
  -p '{"spec": {"type": "NodePort"}}'

# Expose Grafana
kubectl patch svc stable-grafana -n prometheus \
  -p '{"spec": {"type": "NodePort"}}'

# Get service ports
kubectl get svc -n prometheus
```

### Get Grafana Password

```bash
kubectl get secret --namespace prometheus stable-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

- **Username:** admin

### Access Dashboards

- **Prometheus:** `http://<worker-public-ip>:<prometheus-nodeport>`
- **Grafana:** `http://<worker-public-ip>:<grafana-nodeport>`

---

## ✅ Verification Checklist

Run these commands to verify your setup:

```bash
# Docker
docker --version

# Java
java -version

# Jenkins (check service)
sudo systemctl status jenkins

# AWS CLI
aws --version
aws sts get-caller-identity

# kubectl
kubectl version --short --client
kubectl get nodes

# eksctl
eksctl version

# ArgoCD
argocd version --client
kubectl get pods -n argocd

# Helm
helm version

# Prometheus & Grafana
kubectl get pods -n prometheus
```

### Service URLs

| Service | URL |
|---------|-----|
| Jenkins | `http://<master-ip>:8080` |
| SonarQube | `http://<master-ip>:9000` |
| ArgoCD | `https://<worker-ip>:<nodeport>` |
| Prometheus | `http://<worker-ip>:<nodeport>` |
| Grafana | `http://<worker-ip>:<nodeport>` |

---

## 🔧 Troubleshooting

### Docker Permission Denied

```bash
sudo chmod 777 /var/run/docker.sock
# OR
sudo usermod -aG docker $USER && newgrp docker
```

### Jenkins Node Not Connecting

1. Verify SSH key is correct
2. Check security group allows SSH (port 22)
3. Verify Worker public IP is correct
4. Check Jenkins Worker logs in Jenkins UI

### EKS Cluster Not Creating

```bash
# Check CloudFormation stacks
aws cloudformation list-stacks --region us-west-1

# Check eksctl logs
eksctl create cluster ... --verbose 4
```

### ArgoCD Login Failed

```bash
# Reset password
kubectl -n argocd patch secret argocd-secret \
  -p '{"stringData": {"admin.password": "'$(htpasswd -bnBC 10 "" newpassword | tr -d ':\n')'"}}'
```

### Pods Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n <namespace>

# Check events
kubectl get events -n <namespace>
```

---

## 🧹 Clean Up

### Delete EKS Cluster

```bash
# Delete node group first
eksctl delete nodegroup \
  --cluster=ai-inference-cluster \
  --name=ai-inference-nodes \
  --region=us-west-1

# Delete cluster
eksctl delete cluster \
  --name=ai-inference-cluster \
  --region=us-west-1
```

### Stop SonarQube

```bash
docker stop SonarQube-Server
docker rm SonarQube-Server
```

### Terminate EC2 Instances

1. Go to **AWS Console** → **EC2** → **Instances**
2. Select `jenkins-master` and `jenkins-worker`
3. Click **Instance State** → **Terminate instance**

### Clean Docker Resources

```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q)
docker system prune -a -f
```

---

## 📚 Next Steps

After completing this setup:

1. **Configure Jenkins** - See [Jenkins Configuration](../README.md#️-jenkins-configuration)
2. **Setup Email Notifications** - See [Email Setup](../README.md#-email-notification-setup)
3. **Deploy Application** - See [ArgoCD Deployment](../README.md#-argocd-deployment)
4. **Run Pipeline** - Create and run CI/CD pipelines

---

<p align="center">
  <b>Infrastructure Setup Complete! 🎉</b>
</p>
