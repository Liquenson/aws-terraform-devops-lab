from unittest.mock import patch, MagicMock
import sys
import botocore.exceptions

sys.path.insert(0, "scripts")
from check_infra import check_eks, check_ecr, check_backend


# ─── check_eks ────────────────────────────────────────────────────────────────

def test_check_eks_active():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.describe_cluster.return_value = {
            "cluster": {"status": "ACTIVE"}
        }
        assert check_eks() is True


def test_check_eks_not_active():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.describe_cluster.return_value = {
            "cluster": {"status": "CREATING"}
        }
        assert check_eks() is False


def test_check_eks_client_error():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.describe_cluster.side_effect = (
            botocore.exceptions.ClientError(
                {"Error": {"Code": "ResourceNotFoundException", "Message": "Not found"}},
                "DescribeCluster",
            )
        )
        assert check_eks() is False


def test_check_eks_generic_error():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.describe_cluster.side_effect = Exception("unexpected")
        assert check_eks() is False


# ─── check_ecr ────────────────────────────────────────────────────────────────

def test_check_ecr_found():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.describe_repositories.return_value = {
            "repositories": [{"repositoryUri": "123456789.dkr.ecr.eu-west-1.amazonaws.com/webapp"}]
        }
        assert check_ecr() is True


def test_check_ecr_client_error():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.describe_repositories.side_effect = (
            botocore.exceptions.ClientError(
                {"Error": {"Code": "RepositoryNotFoundException", "Message": "Not found"}},
                "DescribeRepositories",
            )
        )
        assert check_ecr() is False


def test_check_ecr_generic_error():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.describe_repositories.side_effect = Exception("unexpected")
        assert check_ecr() is False


# ─── check_backend ────────────────────────────────────────────────────────────

def test_check_backend_found():
    with patch("check_infra.boto3.client") as mock_client:
        mock_sts = MagicMock()
        mock_sts.get_caller_identity.return_value = {"Account": "123456789012"}
        mock_s3 = MagicMock()
        mock_s3.head_bucket.return_value = {}
        mock_client.side_effect = lambda service, **kwargs: (
            mock_sts if service == "sts" else mock_s3
        )
        assert check_backend() is True


def test_check_backend_client_error():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.head_bucket.side_effect = (
            botocore.exceptions.ClientError(
                {"Error": {"Code": "NoSuchBucket", "Message": "Not found"}},
                "HeadBucket",
            )
        )
        assert check_backend() is False


def test_check_backend_generic_error():
    with patch("check_infra.boto3.client") as mock_client:
        mock_client.return_value.head_bucket.side_effect = Exception("unexpected")
        assert check_backend() is False