# Flux demo repository

kubectl create secret generic flux-demo-https-secret \
  --from-literal=username=marcobambili \
  --from-literal=password=YOUR_GITHUB_TOKEN \
  --namespace=flux



kubectl create secret generic flux-demo-https-secret --from-literal=username=marcobambili --from-literal=password=REMOVED --namespace=flux-system

REMOVED


docker build -t 01bit/docker-nodejs-demo:1.0.0 .
docker push 01bit/docker-nodejs-demo:1.0.0


git remote set-url origin https://github.com/marcobambili/flux-demo.git





docker build -t 01bit/docker-nodejs-demo:1.0.0 .

docker push 01bit/docker-nodejs-demo:1.0.0


flux reconcile kustomization flux-demo --with-source



docker build -t 01bit/docker-nodejs-demo:1.0.1 .

docker push 01bit/docker-nodejs-demo:1.0.1



# Installation

```
kubectl create ns flux
export GHUSER="marcobambili"
fluxctl install \
--git-user=marcobambili \
--git-email=marcobambili@users.noreply.github.com \
--git-url=git@github.com:marcobambili/flux-demo \
--git-path=namespaces,workloads \
--namespace=flux | kubectl apply -f -
```


$env:GHUSER="marcobambili"
fluxctl install `
  --git-user="marcobambili" `
  --git-email="marcobambili@users.noreply.github.com" `
  --git-url="git@github.com:marcobambili/flux-demo" `
  --git-path="namespaces,workloads" `
  --namespace="flux" | kubectl apply -f -



Check rollout status:
```
kubectl -n flux rollout status deployment/flux
```

# Setup SSH key
```
fluxctl identity --k8s-fwd-ns flux
```

# Sync repo manually
```
fluxctl sync --k8s-fwd-ns flux
```
