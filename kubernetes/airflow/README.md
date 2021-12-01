# DEPLOY AIRFLOW ON KUBERNETES

### Add helm repo and download default values.yaml
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm show values bitnami/airflow > airflow/values.yaml
```

### Create Service Account and Requirements ConfigMap
```bash
kubectl apply -f requirements-configmap.yml -n airflow
kubectl create role airflow --verb=get,list,watch --resource=pods,pods/status --namespace=airflow 
kubectl create rolebinding airflow-binding --role=airflow --user=system --serviceaccount=airflow:default -n airflow 
```
### Deploy Airflow
```bash
helm install airflow bitnami/airflow -n airflow -f values.yaml
```

## In case you need to update
1. Get the Airflow URL by running:

  NOTE: It may take a few minutes for the LoadBalancer IP to be available.
        Watch the status with: 'kubectl get svc --namespace airflow -w airflow'

  export AIRFLOW_HOST=$(kubectl get svc --namespace airflow airflow --template "{{ range (index .status.loadBalancer.ingress 0) }}{{ . }}{{ end }}")
  export AIRFLOW_PORT=80
  export AIRFLOW_PASSWORD=$(kubectl get secret --namespace "airflow" airflow -o jsonpath="{.data.airflow-password}" | base64 --decode)
  export AIRFLOW_FERNETKEY=$(kubectl get secret --namespace "airflow" airflow -o jsonpath="{.data.airflow-fernetKey}" | base64 --decode)
  export AIRFLOW_SECRETKEY=$(kubectl get secret --namespace "airflow" airflow -o jsonpath="{.data.airflow-secretKey}" | base64 --decode)
  export POSTGRESQL_PASSWORD=$(kubectl get secret --namespace "airflow" airflow-postgresql -o jsonpath="{.data.postgresql-password}" | base64 --decode)
  export REDIS_PASSWORD=$(kubectl get secret --namespace "airflow" airflow-redis -o jsonpath="{.data.redis-password}" | base64 --decode)

2. Complete your Airflow deployment by running:

  helm upgrade --namespace airflow airflow bitnami/airflow \
    --set service.type=LoadBalancer \
    --set web.baseUrl=http://$AIRFLOW_HOST:$AIRFLOW_PORT \
    --set auth.password=$AIRFLOW_PASSWORD \
    --set auth.fernetKey=$AIRFLOW_FERNETKEY \
    --set auth.secretKey=$AIRFLOW_SECRETKEY \
    --set postgresql.postgresqlPassword=$POSTGRESQL_PASSWORD \
    --set redis.auth.password=$REDIS_PASSWORD

