# DEPLOY AIRFLOW ON KUBERNETES

### Add helm repo and download default values.yaml
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm show values bitnami/airflow > airflow/values.yaml
```

### Create Service Account and Requirements ConfigMap
```bash
kubectl apply -f requirements-configmap.yaml -n airflow
```

```bash
kubectl apply -f serviceaccount.yaml -n airflow
```


