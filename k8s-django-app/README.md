# Kubernetes Django
Build up a Django app with deployment, services, scale running on K8s

## Getting Started

## Kubernetes Cluster Configuration
  - Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) on your local machine, a CLI tool to manage Kubernetes cluster
  - Working directory is root of this repo


### Build up a new Cluster
  - Install [Minikube](https://github.com/kubernetes/minikube) to setup cluster on your local

### Docker registry config
- config Docker Registry so Kubernetes can work with
    - `docker login {registry_endpoint}`
    - update the value of key `.dockerconfigjson` by the value of cat `~/.docker/config.json | base64`

### Deploy sample application to the new cluster
Apply sample application at `./development`. This is step by step for creating configrations.

1. Create namespaces
```bash
$ kubectl create -f development/namespace/namespace.yml
```

2. Create secrets
```bash
$ kubectl create -f secrets/secrets.yml
$ kubectl create -f secrets/docker-register-secret.yml
```

3. Create configMaps
```bash
$ kubectl create -f configMaps/env-config.yml
```

4. Create volumes
```bash
$ kubectl create -f volumes/postgres-pv.yml
$ kubectl create -f volumes/postgres-pvc.yml
```

5. Create deployments
```bash
$ kubectl create -f deployments/api-deploy.yml
$ kubectl create -f deployments/postgres-deploy.yml
```

6. Create services
```bash
$ kubectl create -f services/api-svc.yml
$ kubectl create -f services/postgres-svc.yml
```

7. Create ingress
```bash
$ kubectl create -f ingress/ingress.yml
```

### Create all configs in one command line
```bash
$ ./scripts/create-config.sh
```

### Remove all config in one command line
```bash
$ ./scripts/remove-config.sh
```

### Checking pods and services are created
  - Verify all pods are running

```bash
$ kubectl get pod -n development
```

  - Verify all services are available

```bash
$ kubectl get service -n development
```

### Update sample application
  - Modify sample application configuration files `.yml`
  - Apply changes

```bash
$ kubectl apply -f development/path/<file-name>.yml
```

  - To uninstall the sample application

```bash
$ kubectl delete -f development/
```

### Notes

  - With each command line, add flag `--namespace=<name-space-at-here>` to do something with config file have namespace `<name-space-at-here>`

  - If you don't want add flag like above, you can save the namespace for all subsequent kubectl commands in that context (but will lost when start minikube again).

```bash
$ kubectl config set-context $(kubectl config current-context) --namespace=<insert-namespace-name-here>
```

---

Read more about [kubectl](https://kubernetes.io/docs/user-guide/kubectl-overview/) commands to interact with your cluster.

## Testing manifests for application

  - `$(minikube ip):31509` or `mydjango:31509`
  - `$(minikube ip):32302` or `cheeses.all:32302`

### Note

You need update your/etc/hosts file to route requests from `mydjango` and `cheeses.all` to our minikube instance.

```bash
$ echo "$(minikube ip) mydjango cheeses.all" | sudo tee -a /etc/hosts
```