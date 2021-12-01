# K8s Spark Operator

### Create Service Account
```bash
k create serviceaccount spark -n airflow
```

### Create Cluster Role Binding
```bash
k create clusterrolebinding spark-role-binding --clusterrole=edit --serviceaccount=airflow:spark -n airflow
```

### Add Helm Repo
```bash
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
```

### Deploy on K8s
```bash
helm install spark spark-operator/spark-operator -n airflow
```

### Create Secret

```bash
kubectl create secret generic aws-credentials \
  --from-literal=aws_access_key_id="aws_acess_key_id" \
  --from-literal=aws_secret_access_key="aws_secret_access_key" -n airflow
```
