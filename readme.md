# Placement Prediction Model - Deployment & Production Stage

![EC2](https://img.shields.io/badge/EC2-blue)
![FAST-API](https://img.shields.io/badge/FastAPI-orange)
![Docker](https://img.shields.io/badge/Docker-blue)
![ASG](https://img.shields.io/badge/ASG-Auto%20Scalling_group-purple)
![ELB](https://img.shields.io/badge/ELB-%20ELASTIC_LOAD_BALANCER-yellow)
![CI/CD](https://img.shields.io/badge/CI/CD_with_ACTION%20-red)
![Git](https://img.shields.io/badge/Git/Github-%20Code_Versioning-black)
![CodeDeploy](https://img.shields.io/badge/CodeDeploy-%20Update_deployment_Handling-black)
![Status](https://img.shields.io/badge/Project-Production--Ready-success)


This repository manages the **Production Lifecycle** of the Placement Prediction Model. It focuses on taking the "Production-Ready" model registered in the development phase and serving it as a highly available, scalable web service using **FastAPI**, **Docker**, and **AWS**.

---

## 🏗️ Deployment Architecture
The following diagram illustrates the production architecture, including the CI/CD containerization flow and the cloud infrastructure setup on AWS using a Blue-Green deployment strategy.

![Production & Deployment Workflow](images/production_image.png)

---

## 🚀 Production Workflow

### 1. Model Serving with FastAPI
* **Dynamic Fetching:** The application is built using **FastAPI**. Instead of hardcoding model files, the service dynamically fetches the latest version of the model tagged `Production` from the **MLflow Model Registry** (hosted on Dagshub).
* **Modular Wrapper:** The `src/` code from the development stage is reused here to ensure that the preprocessing logic used during inference exactly matches the logic used during training.

### 2. Containerization (CI/CD Phase 1)
* **Dockerization:** We use a lightweight Python base image to containerize the FastAPI application.
* **Automated CI Pipeline:** Upon a code push, GitHub Actions:
    * Executes **Route Testing** to ensure the API endpoints (`/predict`, `/health`) are responding correctly.
    * Builds a new **Docker Image**.
    * Authenticates and pushes the image to **Docker Hub** with a unique version tag.

### 3. Cloud Infrastructure (CD Phase 2)
The infrastructure is hosted on **AWS** to ensure high availability and scalability:
* **Computing:** Uses **EC2 Instances** organized within an **Auto Scaling Group (ASG)** to handle varying traffic loads.
* **Traffic Management:** An **AWS Elastic Load Balancer (ELB)** sits in front of the instances to distribute user requests evenly.

### 4. Blue-Green Deployment Strategy
To achieve zero-downtime updates, we utilize **AWS CodeDeploy** with a **Blue-Green** strategy:
* **Strategy:** `CodeDeployDefault.HalfAtATime`.
* **Process:** A new "Green" fleet of instances is launched with the latest Docker image. Once health checks pass, traffic is shifted from the "Blue" (old) fleet to the "Green" fleet.
* **Rollback:** If any issues are detected during the shift, traffic is immediately rerouted back to the stable Blue environment.

---

## 📂 Repository Structure
```text
.
├── .github/workflows/   <- Deployment CI/CD (Build, Test, Push to Docker)
├── app.py               <- FastAPI entrypoint and  Route definitions and schemas
├── scripts/             <- Deployment scripts for AWS CodeDeploy (AppSpec)
├── Dockerfile           <- Production container configuration
├── appspec.yml          <- AWS CodeDeploy configuration file
└── requirements.txt     <- Production-specific dependencies

```
## 🛠️ Tech Stack
Framework: FastAPI

* **Containerization**: Docker & Docker Hub

* **Registry**: MLflow (Model Registry)

* **Cloud Platform**: AWS (EC2, ASG, ELB)

* **Deployment Tool**: AWS CodeDeploy

* **CI/CD**: GitHub Actions

## 🔗 Development Source
This deployment repository relies on the models and modular pipelines produced in the development stage. For details on data versioning, training pipelines, and experiment tracking, visit the primary repository:

👉 Development & Training Repository
[![Development](https://img.shields.io/badge/View_Development_Code-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/umiii-786/placement-prediction-Model/)

Developed as part of the Final Year Project (FYP).