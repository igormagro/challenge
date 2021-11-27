# K8s Spark Operator

### Create Service Account
```bash
k create serviceaccount spark -n processing
```

### Create Cluster Role Binding
```bash
k create clusterrolebinding spark-role-binding --clusterrole=edit --serviceaccount=processing:spark -n processing
```

### Add Helm Repo
```bash
helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
```

### Deploy on K8s
```bash
helm install spark spark-operator/spark-operator -n processing
```

### Create Secret

```bash
kubectl create secret generic aws-credentials \
  --from-literal=aws_access_key_id="aws_access_key_id" \
  --from-literal=aws_secret_access_key="aws_secret_access_key" -n processing
```