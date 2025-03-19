

minikube start --mount --mount-string="/Users/marcobambili/Documents/kubernetes/k8s-examples/backup-etcd:/mnt/data"

minikube start --network=socket_vmnet


minikube mount /Users/marcobambili/Documents/kubernetes/k8s-examples/backup-etcd:/mnt/data


scp -i $(minikube ssh-key) docker@192.168.49.2:/tmp/etcd-backup.db /Users/marcobambili/Documents/kubernetes/k8s-examples/backup-etcd/

ETCDCTL_API=3

/mnt/vdb1/var/lib/docker/overlay2/cc162016e04b37380ab6eca3e798035a9a1b79ed22392253a9e0ef0ef412ae88/merged/usr/local/bin/etcdctl snapshot save /home/docker/etcd-backup.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/var/lib/minikube/certs/etcd/ca.crt \
  --cert=/var/lib/minikube/certs/etcd/server.crt \
  --key=/var/lib/minikube/certs/etcd/server.key



kubectl delete pod -n kube-system -l app=etcd



minikube cp minikube:/home/docker/etcd-backup.db $(pwd)/etcd-backup.db


minikube cp $(pwd)/etcd-backup.db minikube:/home/docker/etcd-backup.db

sudo rm -rf /var/lib/minikube/etcd/*


/mnt/vdb1/var/lib/docker/overlay2/4e72f894466f8c7358eb52e51e33f9b183cb87018d5520f15a6ad0affd65ebfc/diff/usr/local/bin/etcdctl snapshot restore /home/docker/etcd-backup.db \
  --data-dir=/var/lib/minikube/etcd



kubectl apply -f https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/admin/dns/etcd.yaml
