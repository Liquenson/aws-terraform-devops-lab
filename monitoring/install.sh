#!/bin/bash
set -euo pipefail
aws eks update-kubeconfig --name devops-cluster --region eu-west-1
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm upgrade --install monitoring prometheus-community/kube-prometheus-stack \
  -f monitoring/prometheus-values.yaml \
  --namespace monitoring \
  --create-namespace \
  --wait
echo "Grafana: kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring"
