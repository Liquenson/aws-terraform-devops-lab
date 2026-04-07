# AWS Terraform DevOps Lab

[![CI/CD Pipeline](https://github.com/Liquenson/aws-terraform-devops-lab/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Liquenson/aws-terraform-devops-lab/actions/workflows/ci-cd.yml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=aws-terraform-devops-lab&organization=liquensonruben&metric=alert_status)](https://sonarcloud.io/dashboard?id=aws-terraform-devops-lab)

[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=aws-terraform-devops-lab&organization=liquensonruben&metric=security_rating)](https://sonarcloud.io/dashboard?id=aws-terraform-devops-lab)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=aws-terraform-devops-lab&organization=liquensonruben&metric=coverage)](https://sonarcloud.io/dashboard?id=aws-terraform-devops-lab)

[![Terraform](https://img.shields.io/badge/Terraform-1.9.8-7B42BC?logo=terraform)](https://www.terraform.io/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.29-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![AWS](https://img.shields.io/badge/AWS-EKS%20%7C%20RDS%20%7C%20ECR%20%7C%20VPC-FF9900?logo=amazonaws)](https://aws.amazon.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Infraestructura de producción completa en AWS, desplegada mediante Terraform, con orquestación de contenedores en EKS, pipelines CI/CD automatizados y observabilidad de nivel empresarial.**

---

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Stack Tecnológico](#stack-tecnológico)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Módulos Terraform](#módulos-terraform)
- [Aplicación Flask](#aplicación-flask)
- [Contenedorización](#contenedorización)
- [Kubernetes y Orquestación](#kubernetes-y-orquestación)
- [Pipeline CI/CD](#pipeline-cicd)
- [Monitorización y Observabilidad](#monitorización-y-observabilidad)
- [Seguridad](#seguridad)
- [Gestión de Entornos](#gestión-de-entornos)
- [Variables de Configuración](#variables-de-configuración)
- [Outputs de Infraestructura](#outputs-de-infraestructura)
- [Requisitos Previos](#requisitos-previos)
- [Guía de Despliegue](#guía-de-despliegue)
- [Validación de Infraestructura](#validación-de-infraestructura)
- [Contribución](#contribución)

---

## Descripción General

Este repositorio implementa una infraestructura cloud completa de nivel productivo sobre **Amazon Web Services**, siguiendo las mejores prácticas de la industria en cuanto a infraestructura como código (IaC), seguridad, escalabilidad y observabilidad.

El proyecto despliega una aplicación web **Python/Flask** containerizada sobre **Amazon EKS**, con alta disponibilidad en múltiples zonas de disponibilidad, escalado automático, base de datos gestionada con failover automático, registro privado de imágenes Docker y pipelines de integración y despliegue continuo completamente automatizados.

**Características principales:**

- Infraestructura multi-AZ con alta disponibilidad y tolerancia a fallos
- Arquitectura modular en Terraform para máxima reutilización y mantenibilidad
- Pipeline CI/CD con análisis estático de código, cobertura de tests y validación de infraestructura
- Escalado automático tanto a nivel de pods (HPA) como de nodos (ASG)
- Seguridad por capas: red, identidad, datos en tránsito y en reposo
- Stack de monitorización completo con Prometheus y Grafana
- Gestión de estado remoto con bloqueo distribuido via DynamoDB

---

## Arquitectura del Sistema

```
                          ┌─────────────────────────────────────────────────────┐
                          │              AWS Cloud — eu-west-1 (Irlanda)         │
                          │                                                       │
                          │  ┌─────────────────────────────────────────────────┐ │
                          │  │            VPC — 10.0.0.0/16                    │ │
                          │  │                                                   │ │
                          │  │  ┌──────────────┐  ┌──────────────┐  ┌────────┐ │ │
                          │  │  │  AZ-1 (eu-w-1a) │  AZ-2 (eu-w-1b) │  AZ-3  │ │ │
                          │  │  │              │  │              │  │        │ │ │
                          │  │  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌────┐ │ │ │
                          │  │  │ │  Public  │ │  │ │  Public  │ │  │ │Pub │ │ │ │
                          │  │  │ │  Subnet  │ │  │ │  Subnet  │ │  │ │Sub │ │ │ │
                          │  │  │ └──────────┘ │  │ └──────────┘ │  │ └────┘ │ │ │
                          │  │  │ ┌──────────┐ │  │ ┌──────────┐ │  │ ┌────┐ │ │ │
                          │  │  │ │  Private │ │  │ │  Private │ │  │ │Priv│ │ │ │
                          │  │  │ │  Subnet  │ │  │ │  Subnet  │ │  │ │Sub │ │ │ │
                          │  │  │ │          │ │  │ │          │ │  │ │    │ │ │ │
                          │  │  │ │ [EKS    ]│ │  │ │ [EKS    ]│ │  │ │EKS │ │ │ │
                          │  │  │ │ [Worker ]│ │  │ │ [Worker ]│ │  │ │    │ │ │ │
                          │  │  │ │ [Nodes  ]│ │  │ │ [Nodes  ]│ │  │ │    │ │ │ │
                          │  │  │ └──────────┘ │  │ └──────────┘ │  │ └────┘ │ │ │
                          │  │  │ ┌──────────┐ │  │              │  │        │ │ │
                          │  │  │ │ RDS      │ │  │ ┌──────────┐ │  │        │ │ │
                          │  │  │ │ Primary  │ │  │ │ RDS      │ │  │        │ │ │
                          │  │  │ │ (MySQL)  │ │  │ │ Standby  │ │  │        │ │ │
                          │  │  │ └──────────┘ │  │ └──────────┘ │  │        │ │ │
                          │  │  └──────────────┘  └──────────────┘  └────────┘ │ │
                          │  │                                                   │ │
                          │  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │ │
                          │  │  │   ECR    │  │    S3    │  │  CloudWatch  │   │ │
                          │  │  │ (Images) │  │  (State) │  │   (Logs)     │   │ │
                          │  │  └──────────┘  └──────────┘  └──────────────┘   │ │
                          │  └─────────────────────────────────────────────────┘ │
                          └─────────────────────────────────────────────────────┘

  GitHub Actions ──► ECR Push ──► EKS Deploy ──► Prometheus ──► Grafana
       │                                              │
       └──► SonarCloud ──► Terraform Plan/Apply       └──► CloudWatch Alarms
```

### Flujo de Tráfico

```
Usuario / Internet
       │
       ▼
  [Load Balancer]  ←── Kubernetes Service (LoadBalancer)
       │
       ▼
  [EKS Node Group]  ←── Auto Scaling Group (1–4 nodos t3.medium)
       │
       ▼
  [Pod: webapp]  ←── HPA (2–10 réplicas) — CPU >70% / Memory >80%
       │
       ▼
  [RDS MySQL Multi-AZ]  ←── Subnets privadas (sin acceso público)
```

---

## Stack Tecnológico

### Infraestructura como Código

| Herramienta | Versión | Uso |
|---|---|---|
| Terraform | 1.9.8 | Provisión de toda la infraestructura AWS |
| HCL | — | Lenguaje de configuración de Terraform |
| AWS Provider | — | Interacción con servicios AWS |

### Servicios AWS

| Servicio | Uso |
|---|---|
| **VPC** | Red aislada con subnets públicas y privadas en 3 AZs |
| **EKS** | Cluster Kubernetes gestionado con worker nodes en ASG |
| **RDS MySQL** | Base de datos relacional con Multi-AZ y failover automático |
| **ECR** | Registro privado de imágenes Docker |
| **S3** | Almacenamiento de estado remoto de Terraform |
| **DynamoDB** | Bloqueo de estado distribuido para Terraform |
| **CloudWatch** | Logs centralizados y alarmas del cluster EKS |
| **IAM** | Roles y políticas con principio de mínimo privilegio |

### Contenedores y Orquestación

| Herramienta | Versión | Uso |
|---|---|---|
| Docker | — | Builds multi-stage optimizados |
| Kubernetes | 1.29 | Orquestación de contenedores |
| Helm | 3 | Gestión de charts para despliegue |
| ArgoCD | — | GitOps para despliegues declarativos |

### Aplicación

| Componente | Versión | Uso |
|---|---|---|
| Python | 3.11+ | Lenguaje de la aplicación |
| Flask | — | Framework web REST API |
| Gunicorn | — | Servidor WSGI de producción (2 workers, 2 threads) |

### CI/CD y Calidad

| Herramienta | Uso |
|---|---|
| GitHub Actions | Pipeline principal de CI/CD |
| SonarCloud | Análisis estático, cobertura, vulnerabilidades |
| pytest | Framework de tests unitarios |
| flake8 | Linting de código Python |
| `terraform fmt` | Formateo y validación de IaC |

### Monitorización

| Herramienta | Puerto | Uso |
|---|---|---|
| Prometheus | 9090 | Recolección de métricas |
| Grafana | 3000 | Dashboards y visualización |
| CloudWatch | — | Logs y alarmas en AWS |

---

## Estructura del Repositorio

```
aws-terraform-devops-lab/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # Pipeline principal de CI/CD
│
├── terraform/                      # Configuración raíz de Terraform
│   ├── main.tf                     # Orquestación de módulos (6 módulos)
│   ├── variables.tf                # Definición de 16 variables de entrada
│   ├── outputs.tf                  # 5 outputs de infraestructura
│   ├── providers.tf                # Configuración del proveedor AWS
│   └── backend.tf                  # Backend remoto S3 + DynamoDB
│
├── modules/                        # Módulos Terraform reutilizables
│   ├── vpc/                        # Red virtual: subnets, routing, IGW, NAT
│   ├── eks/                        # Cluster EKS + Node Group + ASG
│   ├── rds/                        # Base de datos MySQL Multi-AZ
│   ├── ecr/                        # Registro privado de imágenes Docker
│   ├── iam/                        # Roles y políticas IAM
│   ├── s3_bucket/                  # Bucket S3 con versionado
│   └── cloudwatch/                 # Logs y alarmas de monitorización
│
├── environments/
│   ├── dev/                        # Variables y configuración de desarrollo
│   └── prod/                       # Variables y configuración de producción
│
├── docker/
│   ├── Dockerfile                  # Build multi-stage Python 3.11
│   ├── requirements.txt            # Dependencias Python
│   └── src/
│       ├── app.py                  # Aplicación Flask (3 endpoints REST)
│       └── tests/                  # Tests unitarios de la aplicación
│
├── kubernetes/
│   ├── namespace.yaml              # Namespace: webapp
│   ├── deployment.yaml             # 2 réplicas, RollingUpdate, probes
│   ├── service.yaml                # Exposición del servicio
│   └── hpa.yaml                   # Escalado automático (2–10 réplicas)
│
├── helm/
│   └── webapp/                     # Chart Helm para despliegue multi-entorno
│
├── argocd/                         # Definiciones de aplicaciones GitOps
│
├── ansible/                        # Playbooks de configuración post-despliegue
│
├── monitoring/
│   ├── install.sh                  # Script de instalación del stack
│   └── prometheus-values.yaml      # Valores de configuración de Prometheus
│
└── scripts/
    ├── check_infra.py              # Script de validación de infraestructura
    └── tests/                      # Tests de los scripts de validación
```

---

## Módulos Terraform

La infraestructura se organiza en **7 módulos reutilizables e independientes**, ubicados en `modules/`. Todos son invocados desde `terraform/main.tf` y se parametrizan mediante variables centralizadas.

### `vpc` — Red Virtual Privada

Aprovisiona la red base sobre la que corre toda la infraestructura:

- CIDR configurable (por defecto `10.0.0.0/16`)
- Subnets públicas y privadas distribuidas en 3 zonas de disponibilidad
- Internet Gateway para tráfico público saliente
- NAT Gateway para acceso a internet desde subnets privadas
- Tablas de routing segmentadas por visibilidad

### `eks` — Cluster Kubernetes Gestionado

Despliega el cluster de Kubernetes sobre el que corre la aplicación:

- Kubernetes versión `1.29`
- Node Group con instancias `t3.medium`
- Auto Scaling Group: mínimo 1, deseado 2, máximo 4 nodos
- Integración nativa con roles IAM para los nodos
- Worker nodes en subnets privadas para seguridad

### `rds` — Base de Datos Relacional

Base de datos MySQL gestionada con alta disponibilidad:

- Instancia `db.t3.micro` (configurable)
- Configuración Multi-AZ con failover automático
- Desplegada en subnets privadas (sin acceso público)
- Credenciales gestionadas via variables sensibles de Terraform
- Backup automático habilitado

### `ecr` — Registro de Contenedores

Registro privado de imágenes Docker en AWS:

- Repositorio privado con acceso controlado por IAM
- URL de registro expuesta como output para uso en pipelines
- Integración directa con el pipeline de GitHub Actions

### `iam` — Gestión de Identidades y Accesos

Roles y políticas siguiendo el principio de mínimo privilegio:

- Roles para nodos EKS
- Roles para integración entre servicios AWS
- Políticas con permisos estrictamente necesarios

### `s3_bucket` — Almacenamiento de Estado

Bucket S3 para gestión centralizada del estado de Terraform:

- Versionado habilitado para recuperación ante errores
- Encriptación habilitada en reposo
- Bloqueo de escritura concurrente via DynamoDB (`devops-lab-state-lock`)

### `cloudwatch` — Monitorización Nativa AWS

Configuración de logs y alarmas para el cluster EKS:

- Grupos de logs centralizados
- Métricas del cluster y nodos
- Integración con el stack de Prometheus/Grafana

---

## Aplicación Flask

La aplicación es una **REST API stateless** construida con Python 3.11 y Flask, desplegada con Gunicorn como servidor WSGI de producción.

### Endpoints

| Método | Ruta | Descripción | Respuesta |
|---|---|---|---|
| `GET` | `/` | Información general de la aplicación | `name`, `version`, `aws_region`, `status` |
| `GET` | `/health` | Liveness probe para Kubernetes | `{"status": "healthy"}` — HTTP 200 |
| `GET` | `/ready` | Readiness probe para Kubernetes | `{"status": "ready"}` — HTTP 200 |

### Variables de Entorno

| Variable | Por Defecto | Descripción |
|---|---|---|
| `FLASK_HOST` | `127.0.0.1` | Host de escucha del servidor |
| `FLASK_PORT` | `8080` | Puerto de escucha |
| `FLASK_DEBUG` | `false` | Modo debug (deshabilitado en producción) |
| `APP_VERSION` | — | Versión de la aplicación, expuesta en `/` |
| `AWS_REGION` | `eu-west-1` | Región AWS, inyectada por el deployment |

### Notas de Diseño

La aplicación está diseñada como una API REST stateless pura. La protección CSRF no es aplicable por diseño, ya que todos los endpoints responden con JSON y no gestionan sesiones ni cookies. La configuración de seguridad es consciente y está documentada en el código.

---

## Contenedorización

El `Dockerfile` implementa un **build multi-stage** para optimizar el tamaño de imagen y la seguridad:

```dockerfile
# Stage 1: Builder — instala dependencias
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime — imagen final mínima
FROM python:3.11-slim
WORKDIR /app

# Instalación de curl y creación de usuario no-root
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

# Copia selectiva desde el stage builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY src/ .

RUN chown -R appuser:appuser /app

EXPOSE 8080
USER appuser

# Health check nativo de Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Servidor de producción: Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "60", "app:app"]
```

### Decisiones de Diseño

**Multi-stage build:** Separa las dependencias de compilación del runtime final, reduciendo significativamente el tamaño de la imagen y la superficie de ataque.

**Usuario no-root:** La aplicación corre como `appuser`, eliminando privilegios innecesarios dentro del contenedor.

**Gunicorn:** Se usa como servidor WSGI de producción en lugar del servidor de desarrollo de Flask, con 2 workers y 2 threads para manejar concurrencia.

**Healthcheck integrado:** Permite que Docker y Kubernetes detecten automáticamente si el contenedor está sano, facilitando la auto-recuperación.

---

## Kubernetes y Orquestación

### Deployment

```yaml
# kubernetes/deployment.yaml (resumen)
replicas: 2
strategy: RollingUpdate (maxSurge: 1, maxUnavailable: 0)
image: 538079272432.dkr.ecr.eu-west-1.amazonaws.com/webapp:1.0.0
resources:
  requests: { cpu: 100m, memory: 128Mi }
  limits:   { cpu: 250m, memory: 256Mi }
probes:
  liveness:  GET /health  (delay: 10s, period: 15s)
  readiness: GET /health  (delay: 5s,  period: 10s)
```

La estrategia `RollingUpdate` con `maxUnavailable: 0` garantiza **cero downtime** durante los despliegues: siempre hay pods activos mientras se despliegan los nuevos.

### Horizontal Pod Autoscaler (HPA)

```yaml
# kubernetes/hpa.yaml (resumen)
minReplicas: 2
maxReplicas: 10
metrics:
  - CPU:    targetAverageUtilization: 70%
  - Memory: targetAverageUtilization: 80%
```

El HPA ajusta automáticamente el número de réplicas entre 2 y 10 basándose en el consumo de CPU y memoria, garantizando que la aplicación escale antes de que los recursos se saturen.

### Namespace

Todos los recursos de la aplicación se despliegan en el namespace `webapp`, proporcionando aislamiento lógico dentro del cluster EKS.

---

## Pipeline CI/CD

El archivo `.github/workflows/ci-cd.yml` define el pipeline completo de integración y despliegue continuo, que se activa en **push a `main`** y en **pull requests hacia `main`**.

```
Push / PR a main
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│  Job 1: sonarcloud                                       │
│                                                          │
│  1. Checkout código (full depth para análisis)           │
│  2. Configurar Python 3.11                               │
│  3. Instalar dependencias (pytest, boto3, flask...)      │
│  4. Ejecutar tests — scripts/tests/ + docker/src/tests/  │
│  5. Generar reporte de cobertura XML                     │
│  6. Análisis SonarCloud (Quality Gate)                   │
└────────────────────────┬────────────────────────────────┘
                         │ (solo si pasa)
                         ▼
┌─────────────────────────────────────────────────────────┐
│  Job 2: terraform                                        │
│                                                          │
│  1. Checkout código                                      │
│  2. Configurar credenciales AWS (GitHub Secrets)         │
│  3. Instalar Terraform 1.9.8                             │
│  4. terraform init                                       │
│  5. terraform fmt -check -recursive                      │
│  6. terraform validate                                   │
│  7. terraform plan (con variables de entorno dev)        │
│  8. Subir plan como artefacto de GitHub Actions          │
└─────────────────────────────────────────────────────────┘
```

### Variables de Entorno del Pipeline

| Variable | Valor |
|---|---|
| `AWS_REGION` | `eu-west-1` |
| `TF_DIR` | `terraform/` |
| `CLUSTER_NAME` | `dev-cluster` |

### Secretos Requeridos en GitHub

| Secreto | Descripción |
|---|---|
| `SONAR_TOKEN` | Token de autenticación con SonarCloud |
| `AWS_ACCESS_KEY_ID` | Credencial de acceso AWS |
| `AWS_SECRET_ACCESS_KEY` | Clave secreta AWS |

---

## Monitorización y Observabilidad

El stack de observabilidad se despliega mediante el script `monitoring/install.sh` y se configura con `monitoring/prometheus-values.yaml`.

### Componentes

**Prometheus** (puerto `9090`)
Recoge métricas de los pods de Kubernetes, nodos del cluster EKS y métricas custom de la aplicación Flask. Configurado mediante `prometheus-values.yaml` para adaptarse al entorno del cluster.

**Grafana** (puerto `3000`)
Dashboards preconfigurados para visualizar el estado del cluster, uso de recursos por namespace/pod, métricas de la aplicación y alertas activas.

**CloudWatch**
Logging centralizado de los componentes del cluster EKS. Integrado nativamente con el módulo `cloudwatch` de Terraform y accesible desde la consola de AWS.

### Acceso al Stack de Monitorización

```bash
# Port-forward a Prometheus
kubectl port-forward svc/prometheus-server 9090:9090 -n monitoring

# Port-forward a Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring
# Credenciales iniciales: admin / admin (cambiar en primer acceso)
```

---

## Seguridad

La seguridad se aplica en múltiples capas a lo largo de toda la infraestructura.

### Red

- Subnets privadas para RDS y nodos EKS, sin exposición directa a internet
- Security Groups con reglas restrictivas y acceso mínimo necesario
- NAT Gateway para tráfico saliente controlado desde subnets privadas

### Identidad y Acceso (IAM)

- Principio de mínimo privilegio en todos los roles y políticas
- Roles específicos para cada servicio (nodos EKS, acceso a ECR, S3, etc.)
- Ninguna credencial hardcodeada en el código ni en los archivos de configuración

### Gestión de Secretos

- Todos los secretos (credenciales AWS, tokens de SonarCloud, contraseña de RDS) se gestionan mediante **GitHub Secrets**
- El output de `rds_endpoint` en Terraform está marcado como `sensitive = true`, ocultándolo en logs

### Contenedores

- Imagen Docker basada en `python:3.11-slim` (superficie de ataque mínima)
- Proceso de aplicación ejecutado como usuario no-root (`appuser`)
- Build multi-stage elimina herramientas de compilación de la imagen final

### Datos

- Encriptación en reposo habilitada en S3 (estado de Terraform) y RDS
- Encriptación en tránsito (TLS/SSL) para todas las comunicaciones
- Estado de Terraform con encriptación: `encrypt = true` en `backend.tf`

### Análisis de Código

- **SonarCloud** con Security Rating A y cero vulnerabilidades críticas o altas
- SAST (Static Application Security Testing) integrado en el pipeline
- Análisis de dependencias incluido en cada ejecución del pipeline

---

## Gestión de Entornos

El repositorio soporta múltiples entornos mediante el directorio `environments/`:

```
environments/
├── dev/     ← Configuración de desarrollo (valores reducidos, coste optimizado)
└── prod/    ← Configuración de producción (alta disponibilidad, recursos completos)
```

Cada entorno dispone de su propio fichero de variables (`.tfvars`) que sobreescribe los valores por defecto. El estado de Terraform para cada entorno se mantiene de forma independiente en el bucket S3.

```bash
# Despliegue en dev
terraform plan -var-file="environments/dev/terraform.tfvars"

# Despliegue en producción
terraform plan -var-file="environments/prod/terraform.tfvars"
```

---

## Variables de Configuración

Todas las variables de Terraform se definen en `terraform/variables.tf`:

| Variable | Tipo | Por Defecto | Requerida | Descripción |
|---|---|---|---|---|
| `environment` | `string` | `"dev"` | No | Entorno de despliegue |
| `aws_region` | `string` | `"eu-west-1"` | No | Región AWS objetivo |
| `bucket_name` | `string` | — | **Sí** | Nombre del bucket S3 de la app |
| `vpc_cidr` | `string` | `"10.0.0.0/16"` | No | Bloque CIDR de la VPC |
| `public_subnets` | `list(string)` | — | **Sí** | CIDRs de subnets públicas |
| `private_subnets` | `list(string)` | — | **Sí** | CIDRs de subnets privadas |
| `availability_zones` | `list(string)` | — | **Sí** | Lista de AZs a usar |
| `instance_type` | `string` | `"t3.medium"` | No | Tipo de instancia de nodos EKS |
| `desired_capacity` | `number` | `2` | No | Nodos deseados en el ASG |
| `min_capacity` | `number` | `1` | No | Nodos mínimos en el ASG |
| `max_capacity` | `number` | `4` | No | Nodos máximos en el ASG |
| `kubernetes_version` | `string` | `"1.29"` | No | Versión de Kubernetes en EKS |
| `db_name` | `string` | `"appdb"` | No | Nombre de la base de datos |
| `db_username` | `string` | `"dbadmin"` | No | Usuario de la base de datos |
| `db_password` | `string` | — | **Sí** | Contraseña RDS (sensible) |
| `rds_instance` | `string` | `"db.t3.micro"` | No | Tipo de instancia RDS |

---

## Outputs de Infraestructura

Una vez aplicada la infraestructura, Terraform expone los siguientes valores en `terraform/outputs.tf`:

| Output | Descripción | Sensible |
|---|---|---|
| `vpc_id` | ID de la VPC creada | No |
| `eks_cluster_name` | Nombre del cluster EKS | No |
| `eks_cluster_endpoint` | Endpoint de la API del cluster | No |
| `ecr_repository_url` | URL del repositorio ECR | No |
| `rds_endpoint` | Endpoint de conexión a la base de datos | **Sí** |

```bash
# Obtener todos los outputs
terraform output

# Obtener el endpoint de RDS (requiere --raw para valores sensibles)
terraform output -raw rds_endpoint
```

---

## Requisitos Previos

Antes de desplegar este proyecto, asegúrate de tener instalado y configurado lo siguiente:

| Herramienta | Versión Mínima | Instalación |
|---|---|---|
| Terraform | 1.9.8 | [terraform.io/downloads](https://developer.hashicorp.com/terraform/downloads) |
| AWS CLI | 2.x | [aws.amazon.com/cli](https://aws.amazon.com/es/cli/) |
| kubectl | 1.29+ | [kubernetes.io/docs](https://kubernetes.io/docs/tasks/tools/) |
| Helm | 3.x | [helm.sh](https://helm.sh/docs/intro/install/) |
| Docker | 24.x+ | [docs.docker.com](https://docs.docker.com/get-docker/) |
| Python | 3.11+ | [python.org](https://www.python.org/downloads/) |

**Permisos AWS necesarios:**
- Crear y gestionar VPC, subnets, routing
- Crear y gestionar clusters EKS y node groups
- Crear y gestionar instancias RDS
- Crear y gestionar repositorios ECR
- Crear y gestionar buckets S3
- Crear tablas DynamoDB
- Crear roles y políticas IAM
- Crear grupos de logs en CloudWatch

---

## Guía de Despliegue

### 1. Clonar el repositorio

```bash
git clone https://github.com/Liquenson/aws-terraform-devops-lab.git
cd aws-terraform-devops-lab
```

### 2. Configurar credenciales AWS

```bash
aws configure
# AWS Access Key ID:     [tu-access-key]
# AWS Secret Access Key: [tu-secret-key]
# Default region name:   eu-west-1
# Default output format: json
```

### 3. Preparar el backend remoto de Terraform

Antes de inicializar Terraform, crea el bucket S3 y la tabla DynamoDB para el estado remoto:

```bash
# Crear bucket S3 para el estado
aws s3api create-bucket \
  --bucket devops-lab-tfstate-538079272432 \
  --region eu-west-1 \
  --create-bucket-configuration LocationConstraint=eu-west-1

# Habilitar versionado
aws s3api put-bucket-versioning \
  --bucket devops-lab-tfstate-538079272432 \
  --versioning-configuration Status=Enabled

# Crear tabla DynamoDB para bloqueo de estado
aws dynamodb create-table \
  --table-name devops-lab-state-lock \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region eu-west-1
```

### 4. Inicializar y aplicar Terraform

```bash
cd terraform/

# Inicializar Terraform (descarga providers, configura backend)
terraform init

# Seleccionar o crear workspace de entorno
terraform workspace new dev  # o 'prod'

# Revisar los cambios antes de aplicar
terraform plan -var-file="../environments/dev/terraform.tfvars"

# Aplicar la infraestructura
terraform apply -var-file="../environments/dev/terraform.tfvars"
```

### 5. Configurar kubectl para el cluster EKS

```bash
aws eks update-kubeconfig \
  --region eu-west-1 \
  --name $(terraform output -raw eks_cluster_name)

# Verificar conexión al cluster
kubectl get nodes
```

### 6. Desplegar la aplicación con Helm

```bash
# Construir y subir la imagen Docker a ECR
ECR_URL=$(terraform output -raw ecr_repository_url)
aws ecr get-login-password --region eu-west-1 | docker login --username AWS --password-stdin $ECR_URL

docker build -t webapp ./docker
docker tag webapp:latest $ECR_URL:1.0.0
docker push $ECR_URL:1.0.0

# Desplegar con Helm
helm upgrade --install webapp ./helm/webapp \
  --namespace webapp \
  --create-namespace \
  --set image.repository=$ECR_URL \
  --set image.tag=1.0.0
```

### 7. Instalar el stack de monitorización

```bash
cd monitoring/
chmod +x install.sh
./install.sh
```

### 8. Verificar el despliegue

```bash
# Estado de los pods
kubectl get pods -n webapp

# Estado del HPA
kubectl get hpa -n webapp

# Logs de la aplicación
kubectl logs -l app=webapp -n webapp --tail=100

# Endpoint de la aplicación
kubectl get svc -n webapp
```

---

## Validación de Infraestructura

El script `scripts/check_infra.py` permite validar el estado de la infraestructura desplegada de forma programática:

```bash
cd scripts/
python check_infra.py
```

Este script utiliza `boto3` para conectarse a AWS y verificar que todos los recursos críticos (VPC, EKS, RDS, ECR) están correctamente aprovisionados y operativos.

### Ejecutar los Tests

```bash
# Tests de la aplicación Flask
cd docker/src/
pytest tests/ -v --cov=. --cov-report=term-missing

# Tests de los scripts de validación
cd scripts/
pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## Contribución

Este proyecto sigue un flujo de trabajo basado en Pull Requests. Para contribuir:

1. Crea una rama desde `main`: `git checkout -b feature/nombre-de-la-feature`
2. Realiza tus cambios, asegurándote de que los tests pasan: `pytest`
3. Verifica el formato de Terraform: `terraform fmt -check -recursive`
4. Abre un Pull Request hacia `main`
5. El pipeline de CI/CD validará automáticamente el código y la infraestructura
6. Una vez aprobado el Quality Gate de SonarCloud y el plan de Terraform, se puede hacer merge

---

## Autor

**Rubén Liquenson**
DevOps Engineer || Cloud & Linux Administrator || AWS || Kubernetes · 
Gran Canaria, España

[![GitHub](https://img.shields.io/badge/GitHub-Liquenson-181717?logo=github)](https://github.com/Liquenson)

---

*Este README ha sido generado a partir del análisis completo del repositorio. Refleja el estado del código a fecha de abril de 2026.*
