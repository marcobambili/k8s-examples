


velero install \
    --provider aws \
    --plugins velero/velero-plugin-for-aws:v1.7.0 \
    --bucket <nome-bucket> \
    --secret-file velero-credentials \
    --backup-location-config region=eu-central-1 \
    --use-node-agent \
    --use-volume-snapshots=false



kubectl annotate pvc <nome-pvc> backup.velero.io/backup-volumes=<nome-volume>

velero backup create my-backup --include-namespaces=default
