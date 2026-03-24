#!/usr/bin/env python3
"""Valida el estado de la infraestructura AWS en eu-west-1"""

import sys

import boto3
import botocore

REGION = "eu-west-1"

def check_eks():
    eks = boto3.client("eks", region_name=REGION)
    try:
        r = eks.describe_cluster(name="devops-cluster")
        status = r["cluster"]["status"]
        print(f"[OK] EKS devops-cluster: {status}")
        return status == "ACTIVE"

    except botocore.exceptions.ClientError as e:
        print(f"[WARN] EKS cluster no encontrado: {e}")
        return False

    except Exception as e:   # ✅ correcto
        print(f"[ERROR] Error inesperado en EKS: {e}")
        return False


def check_ecr():
    ecr = boto3.client("ecr", region_name=REGION)
    try:
        r = ecr.describe_repositories(repositoryNames=["webapp"])
        print(f"[OK] ECR webapp: {r['repositories'][0]['repositoryUri']}")
        return True

    except botocore.exceptions.ClientError as e:
        print(f"[WARN] ECR repo webapp no encontrado: {e}")
        return False

    except Exception as e:   # ✅ correcto
        print(f"[ERROR] Error inesperado en ECR: {e}")
        return False


def check_backend():
    s3 = boto3.client("s3", region_name=REGION)
    bucket = "devops-lab-tfstate-538079272432"
    try:
        account_id = boto3.client("sts", region_name=REGION).get_caller_identity()["Account"]
        s3.head_bucket(Bucket=bucket, ExpectedBucketOwner=account_id)
        print(f"[OK] S3 backend: {bucket}")
        return True

    except botocore.exceptions.ClientError as e:
        print(f"[WARN] S3 bucket {bucket} no encontrado: {e}")
        return False

    except Exception as e:   # ✅ correcto
        print(f"[ERROR] Error inesperado en S3: {e}")
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
