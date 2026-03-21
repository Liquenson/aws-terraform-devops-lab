#!/usr/bin/env python3
"""Valida el estado de la infraestructura AWS en eu-west-1"""
import boto3, sys

REGION = "eu-west-1"

def check_eks():
    eks = boto3.client("eks", region_name=REGION)
    try:
        r = eks.describe_cluster(name="devops-cluster")
        status = r["cluster"]["status"]
        print(f"[OK] EKS devops-cluster: {status}")
        return status == "ACTIVE"
    except:
        print("[WARN] EKS cluster no encontrado")
        return False

def check_ecr():
    ecr = boto3.client("ecr", region_name=REGION)
    try:
        r = ecr.describe_repositories(repositoryNames=["webapp"])
        print(f"[OK] ECR webapp: {r['repositories'][0]['repositoryUri']}")
        return True
    except:
        print("[WARN] ECR repo webapp no encontrado")
        return False

def check_backend():
    s3 = boto3.client("s3", region_name=REGION)
    bucket = "devops-lab-tfstate-538079272432"
    try:
        s3.head_bucket(Bucket=bucket)
        print(f"[OK] S3 backend: {bucket}")
        return True
    except:
        print(f"[WARN] S3 bucket {bucket} no encontrado")
        return False

if __name__ == "__main__":
    print(f"\n==> Verificando infraestructura en {REGION}\n")
    results = [check_backend(), check_eks(), check_ecr()]
    print()
    if all(results):
        print("==> Todo OK.")
        sys.exit(0)
    else:
        print("==> Hay componentes pendientes.")
        sys.exit(1)
