# AWS Terraform DevOps Lab

[![Build Status](https://github.com/Liquenson/aws-terraform-devops-lab/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Liquenson/aws-terraform-devops-lab/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Liquenson_aws-terraform-devops-lab&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Liquenson_aws-terraform-devops-lab)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=Liquenson_aws-terraform-devops-lab&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=Liquenson_aws-terraform-devops-lab)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Liquenson_aws-terraform-devops-lab&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Liquenson_aws-terraform-devops-lab)

## 📋 Descripción

Proyecto completo de infraestructura AWS como código (IaC) que demuestra las mejores prácticas de DevOps moderno. Este laboratorio implementa una aplicación web Python/Flask containerizada desplegada en Amazon EKS con un pipeline CI/CD completo, monitorización integrada y alta disponibilidad.

**Objetivo principal:** Demostrar competencias técnicas en infraestructura cloud, automatización, contenedores y prácticas DevOps para entornos de producción empresarial.

---

## 🏗️ Arquitectura AWS

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud (eu-west-1)                    │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ VPC (10.0.0.0/16)                                          │ │
│  │                                                             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │ │
│  │  │   Public     │  │   Public     │  │   Public     │    │ │
│  │  │   Subnet     │  │   Subnet     │  │   Subnet     │    │ │
│  │  │   AZ-1       │  │   AZ-2       │  │   AZ-3       │    │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │ │
│  │         │                  │                  │            │ │
│  │  ┌──────▼──────────────────▼──────────────────▼───────┐   │ │
│  │  │          Amazon EKS Cluster                        │   │ │
│  │  │  ┌─────────────────────────────────────────────┐  │   │ │
│  │  │  │  Worker Nodes (Auto Scaling Group)          │  │   │ │
│  │  │  │  - Flask App (Pods)                         │  │   │ │
│  │  │  │  - Prometheus                               │  │   │ │
│  │  │  │  - Grafana                                  │  │   │ │
│  │  │  └─────────────────────────────────────────────┘  │   │ │
│  │  └───────────────────────────────────────────────────┘   │ │
│  │         │                  │                  │            │ │
│  │  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────▼───────┐    │ │
│  │  │   Private    │  │   Private    │  │   Private    │    │ │
│  │  │   Subnet     │  │   Subnet     │  │   Subnet     │    │ │
│  │  │   AZ-1       │  │   AZ-2       │  │   AZ-3       │    │ │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │ │
│  │         │                  │                  │            │ │
│  │         └──────────────────┼──────────────────┘            │ │
│  │                            │                               │ │
│  │                     ┌──────▼───────┐                       │ │
│  │                     │   RDS MySQL  │                       │ │
│  │                     │   Multi-AZ   │                       │ │
│  │                     └──────────────┘                       │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │   Amazon ECR   │  │   Amazon S3    │  │  CloudWatch    │    │
│  │ (Docker Images)│  │ (Terraform     │  │  (Logs/Metrics)│    │
│  │                │  │  State)        │  │                │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Componentes principales:

- **VPC Multi-AZ**: Red privada con subnets públicas y privadas en 3 zonas de disponibilidad
- **Amazon EKS**: Cluster Kubernetes gestionado con nodos worker auto-escalables
- **Amazon RDS MySQL**: Base de datos relacional Multi-AZ con backups automáticos
- **Amazon ECR**: Registro privado de imágenes Docker
- **Amazon S3**: Almacenamiento del estado remoto de Terraform
- **CloudWatch**: Logs centralizados y métricas de monitorización

---

## 🚀 Stack Tecnológico

### Infraestructura como Código
- **Terraform 1.5+**: Módulos reutilizables para VPC, EKS, RDS, ECR, S3, IAM, CloudWatch
- **AWS Provider**: Gestión completa de recursos AWS
- **Remote State**: Backend S3 + DynamoDB para bloqueo de estado

### Contenedores y Orquestación
- **Docker**: Containerización de aplicación Python/Flask
- **Kubernetes**: Manifiestos para Deployment, Service, HPA, Namespace
- **Helm 3**: Charts para gestión de releases y configuración multi-entorno
- **Amazon EKS**: Cluster Kubernetes gestionado v1.28+

### CI/CD y Automatización
- **GitHub Actions**: Pipeline completo de integración y despliegue continuo
- **ArgoCD**: GitOps para despliegues declarativos en Kubernetes
- **Jenkins**: Pipeline alternativo (Jenkinsfile incluido)
- **Ansible**: Configuración post-despliegue de nodos EKS

### Calidad y Seguridad
- **SonarCloud**: Análisis estático de código, cobertura y vulnerabilidades
- **Pytest**: Testing unitario de aplicación Python (>80% coverage)
- **Security Rating A**: Código sin vulnerabilidades críticas ni medias
- **Quality Gate**: Aprobación automática en cada PR

### Monitorización y Observabilidad
- **Prometheus**: Métricas de cluster y aplicación
- **Grafana**: Dashboards personalizados de monitorización
- **CloudWatch**: Logs centralizados y alarmas
- **Horizontal Pod Autoscaler**: Auto-escalado basado en CPU/memoria

### Aplicación
- **Python 3.11+**: Backend con Flask framework
- **Flask**: API REST minimalista para demostración
- **MySQL**: Persistencia de datos vía Amazon RDS

---

## 📁 Estructura del Repositorio

```
aws-terraform-devops-lab/
│
├── terraform/                      # Infraestructura AWS
│   ├── main.tf                     # Orquestación de módulos
│   ├── variables.tf                # Variables de entrada
│   ├── outputs.tf                  # Salidas de recursos
│   ├── providers.tf                # Configuración de providers
│   └── backend.tf                  # Backend S3 para estado remoto
│
├── modules/                        # Módulos Terraform reutilizables
│   ├── vpc/                        # Red VPC multi-AZ
│   ├── eks/                        # Cluster EKS + Node Groups
│   ├── rds/                        # Base de datos RDS MySQL
│   ├── ecr/                        # Registro Docker privado
│   ├── s3_bucket/                  # Buckets S3 con cifrado
│   ├── iam/                        # Roles y políticas IAM
│   └── cloudwatch/                 # Log Groups y alarmas
│
├── environments/                   # Configuración por entorno
│   ├── dev/
│   │   └── terraform.tfvars        # Variables para desarrollo
│   └── prod/
│       └── terraform.tfvars        # Variables para producción
│
├── docker/                         # Aplicación containerizada
│   ├── Dockerfile                  # Multi-stage build
│   ├── requirements.txt            # Dependencias Python
│   └── src/
│       ├── app.py                  # Aplicación Flask
│       └── tests/                  # Tests unitarios (pytest)
│
├── kubernetes/                     # Manifiestos K8s nativos
│   ├── namespace.yaml              # Namespace aislado
│   ├── deployment.yaml             # Deployment de aplicación
│   ├── service.yaml                # Service tipo LoadBalancer
│   └── hpa.yaml                    # Horizontal Pod Autoscaler
│
├── helm/                           # Helm Charts
│   └── webapp/
│       ├── Chart.yaml              # Metadata del chart
│       ├── values.yaml             # Valores por defecto
│       ├── values-dev.yaml         # Override para dev
│       ├── values-prod.yaml        # Override para prod
│       └── templates/              # Plantillas Kubernetes
│
├── argocd/                         # GitOps con ArgoCD
│   └── apps/
│       └── webapp.yaml             # Definición de Application
│
├── ansible/                        # Automatización post-despliegue
│   ├── inventory/
│   │   └── hosts.ini               # Inventario dinámico
│   └── playbooks/
│       └── configure-eks-nodes.yml # Configuración de nodos
│
├── monitoring/                     # Stack de monitorización
│   ├── prometheus-values.yaml      # Configuración Prometheus
│   └── install.sh                  # Script de instalación
│
├── scripts/                        # Scripts de utilidad
│   ├── check_infra.py              # Validación de infraestructura
│   └── tests/                      # Tests de scripts
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # Pipeline GitHub Actions
│
├── Jenkinsfile                     # Pipeline alternativo Jenkins
├── sonar-project.properties        # Configuración SonarCloud
└── README.md                       # Este archivo
```

---

## 🔧 Requisitos Previos

### Herramientas necesarias:
- **Terraform** >= 1.5.0
- **AWS CLI** >= 2.0 configurado con credenciales
- **kubectl** >= 1.28
- **Helm** >= 3.0
- **Docker** >= 20.10
- **Python** >= 3.11
- **Git**

### Credenciales AWS:
```bash
aws configure
# AWS Access Key ID: [tu-access-key]
# AWS Secret Access Key: [tu-secret-key]
# Default region name: eu-west-1
# Default output format: json
```

### Variables de entorno requeridas:
```bash
export AWS_DEFAULT_REGION=eu-west-1
export TF_VAR_environment=dev
```

---

## 🚀 Despliegue de Infraestructura

### 1. Clonar el repositorio
```bash
git clone https://github.com/Liquenson/aws-terraform-devops-lab.git
cd aws-terraform-devops-lab
```

### 2. Configurar backend de Terraform
```bash
cd terraform

# Crear bucket S3 para estado remoto (primera vez)
aws s3 mb s3://tfstate-devops-lab-rliquenson-euw1 --region eu-west-1

# Habilitar versionado
aws s3api put-bucket-versioning \
  --bucket tfstate-devops-lab-rliquenson-euw1 \
  --versioning-configuration Status=Enabled

# Actualizar backend.tf con el nombre de tu bucket
```

### 3. Desplegar infraestructura base
```bash
# Inicializar Terraform
terraform init

# Seleccionar workspace (dev/prod)
terraform workspace new dev
terraform workspace select dev

# Planificar cambios
terraform plan -var-file=../environments/dev/terraform.tfvars

# Aplicar infraestructura
terraform apply -var-file=../environments/dev/terraform.tfvars -auto-approve
```

### 4. Configurar kubectl para EKS
```bash
# Actualizar kubeconfig
aws eks update-kubeconfig \
  --region eu-west-1 \
  --name devops-lab-eks-dev

# Verificar conectividad
kubectl get nodes
kubectl get namespaces
```

### 5. Desplegar aplicación con Helm
```bash
cd ../helm

# Instalar chart de aplicación
helm install webapp ./webapp \
  -f ./webapp/values-dev.yaml \
  --namespace webapp \
  --create-namespace

# Verificar deployment
kubectl get pods -n webapp
kubectl get svc -n webapp
```

### 6. Configurar monitorización
```bash
cd ../monitoring

# Instalar Prometheus + Grafana
chmod +x install.sh
./install.sh

# Obtener credenciales de Grafana
kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode
```

---

## 🔄 Pipeline CI/CD

El proyecto implementa un pipeline completo de CI/CD con **GitHub Actions**:

### Flujo de trabajo:

```
┌─────────────┐
│  git push   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  GitHub Actions Workflow (.github/)     │
├─────────────────────────────────────────┤
│                                         │
│  1️⃣  Checkout código                    │
│  2️⃣  Setup Python 3.11                  │
│  3️⃣  Instalar dependencias              │
│  4️⃣  Linting (flake8)                   │
│  5️⃣  Tests unitarios (pytest)           │
│  6️⃣  Cobertura de código                │
│  7️⃣  SonarCloud Analysis                │
│  8️⃣  Build Docker Image                 │
│  9️⃣  Push to Amazon ECR                 │
│  🔟  Deploy to EKS (solo en tags)       │
│                                         │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  SonarCloud Quality Gate                │
│  ✅ Security Rating: A                  │
│  ✅ No vulnerabilities                  │
│  ✅ Code Coverage > 80%                 │
└─────────────────────────────────────────┘
```

### Triggers del pipeline:
- **Push a main/develop**: Ejecuta CI completo (tests, análisis, build)
- **Pull Request**: CI + validación de Quality Gate
- **Tags (v\*.\*.\*)**: CI + CD completo (deploy a EKS)

### Secretos requeridos en GitHub:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
SONAR_TOKEN
```

---

## 📊 Monitorización

### Prometheus
- **Endpoint**: `http://<load-balancer>:9090`
- Métricas de cluster, nodos y pods
- Alertas configuradas para CPU/memoria/disco

### Grafana
- **Endpoint**: `http://<load-balancer>:3000`
- Usuario: `admin`
- Dashboards pre-configurados:
  - Cluster Overview
  - Node Metrics
  - Pod Metrics
  - Application Performance

### CloudWatch
- Logs centralizados de EKS
- Métricas de RDS (conexiones, CPU, storage)
- Alarmas configuradas para eventos críticos

---

## 🔒 Seguridad

### Prácticas implementadas:

✅ **SonarCloud Quality Gate**: Security Rating A sin vulnerabilidades  
✅ **IAM Least Privilege**: Roles específicos para cada servicio  
✅ **Secrets Management**: Variables sensibles en GitHub Secrets  
✅ **Network Isolation**: Subnets privadas para bases de datos  
✅ **Encryption at Rest**: RDS y S3 con cifrado habilitado  
✅ **Encryption in Transit**: TLS/SSL en todos los endpoints  
✅ **Security Groups**: Reglas de firewall restrictivas  
✅ **No hardcoded credentials**: Credenciales fuera del código fuente  

### Cumplimiento:
- ✅ Código limpio de credenciales (verificado con git-filter-repo)
- ✅ Sin vulnerabilidades críticas o altas
- ✅ Dependencias actualizadas y sin CVEs conocidos

---

## 🧪 Testing

### Tests unitarios (Python)
```bash
cd docker

# Ejecutar tests
pytest src/tests/ -v

# Con cobertura
pytest src/tests/ --cov=src --cov-report=html

# Abrir reporte
open htmlcov/index.html
```

### Validación de infraestructura
```bash
cd scripts

# Verificar recursos AWS
python check_infra.py --environment dev

# Ejecutar tests del script
pytest tests/ -v
```

### Linting de código
```bash
# Python
flake8 docker/src/ --max-line-length=120

# Terraform
terraform fmt -check -recursive terraform/
terraform validate
```

---

## 🌟 Características Destacadas

- ✅ **Infraestructura Multi-AZ**: Alta disponibilidad en 3 zonas
- ✅ **Auto-scaling**: HPA para pods + ASG para nodos EC2
- ✅ **GitOps Ready**: Integración con ArgoCD para despliegues declarativos
- ✅ **Multi-entorno**: Configuración separada para dev/prod
- ✅ **Modular**: Módulos Terraform reutilizables y versionados
- ✅ **Observabilidad**: Stack completo Prometheus + Grafana + CloudWatch
- ✅ **Security First**: Quality Gate A sin vulnerabilidades
- ✅ **Production Ready**: Backups, monitoring, logging, alerting

---

## 🔮 Mejoras Futuras

- [ ] **Service Mesh**: Implementar Istio para tráfico inter-servicios
- [ ] **Chaos Engineering**: Integrar AWS Fault Injection Simulator
- [ ] **Multi-región**: Despliegue activo-pasivo en us-east-1
- [ ] **CDN**: CloudFront para distribución de contenido estático
- [ ] **WAF**: AWS WAF para protección de aplicaciones web
- [ ] **Disaster Recovery**: Automatización de backups cross-region
- [ ] **Cost Optimization**: Spot instances + Fargate para cargas variables
- [ ] **Blue/Green Deployments**: Estrategia de despliegue sin downtime

---

## 📚 Documentación Adicional

- [AWS EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)
- [Terraform AWS Modules](https://registry.terraform.io/namespaces/terraform-aws-modules)
- [Kubernetes Production Best Practices](https://kubernetes.io/docs/setup/best-practices/)
- [Helm Chart Development](https://helm.sh/docs/chart_template_guide/)

---

## 👤 Autor

**Rubén Alexis Liquenson**  
DevOps Engineer | AWS & Kubernetes Specialist  

- GitHub: [@Liquenson](https://github.com/Liquenson)
- LinkedIn: [Liquenson Ruben](https://www.linkedin.com/in/liquenson-ruben)
- Email: liquenson.cloud@gmail.com

---

## 📄 Licencia

Este proyecto es de código abierto bajo la licencia MIT. Ver archivo `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

Este proyecto fue creado como demostración de competencias DevOps para procesos de selección profesional, implementando las mejores prácticas de la industria y siguiendo los estándares de AWS Well-Architected Framework.

**Stack tecnológico inspirado en**: AWS Solutions Architecture.

---

**⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub!**