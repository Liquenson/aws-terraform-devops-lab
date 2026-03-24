from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, "scripts")
from check_infra import check_eks, check_ecr, check_backend

def test_check_eks_not_found():
    with patch("check_infra.boto3.client") as mock:
        mock.return_value.describe_cluster.side_effect = Exception("not found")
        assert check_eks() == False

def test_check_ecr_not_found():
    with patch("check_infra.boto3.client") as mock:
        mock.return_value.describe_repositories.side_effect = Exception("not found")
        assert check_ecr() == False
