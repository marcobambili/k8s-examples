helm repo add openfaas https://openfaas.github.io/faas-netes/
helm repo update

kubectl create namespace openfaas
kubectl create namespace openfaas-fn

helm install openfaas openfaas/openfaas --namespace openfaas --set functionNamespace=openfaas-fn --set generateBasicAuth=true

PASSWORD=$(kubectl -n openfaas get secret basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
echo "La password per l'accesso a OpenFaaS è: $PASSWORD"

kubectl port-forward svc/gateway -n openfaas 8080:8080

faas-cli login --gateway http://localhost:8080 -u admin --password $PASSWORD

faas-cli new hello-world --lang python3


faas-cli build -f hello-world.yml
faas-cli push -f hello-world.yml



faas-cli deploy -f  hello-world.yml





RllMaFJkejd5RTRS

FYLhRdz7yE4R

faas-cli login --gateway http://localhost:8080 -u admin --password FYLhRdz7yE4R




echo "Test" | faas-cli invoke hello-world

curl -X POST http://127.0.0.1:8080/function/hello-world -d "Test"
