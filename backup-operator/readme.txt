
helm install postgres-operator postgres-operator-charts/postgres-operator -f values.yaml


kubectl exec -it my-db-cluster-0 -n default -- psql -U postgres

create database esempio_db;


\c esempio_db;

CREATE TABLE clienti (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50),
    email VARCHAR(100)
);


INSERT INTO clienti (nome, email) VALUES ('Mario Rossi', 'mario.rossi@email.com');
INSERT INTO clienti (nome, email) VALUES ('Anna Bianchi', 'anna.bianchi@email.com');



kubectl create job --from=cronjob/logical-backup-my-db-cluster -n default logical-backup-manual

kubectl logs -l job-name=logical-backup-manual -n default


