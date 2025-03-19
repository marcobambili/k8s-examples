import kopf
import kubernetes.client as k8s_client
import base64

namespace = "default"  # Modifica se necessario

@kopf.on.create('example.com', 'v1', 'staticpages')
def create_static_page(spec, name, **kwargs):
    content = spec.get('content', '<h1>Pagina di default</h1>')

    # Creiamo una ConfigMap per memorizzare l'HTML della pagina
    api = k8s_client.CoreV1Api()
    configmap = k8s_client.V1ConfigMap(
        metadata=k8s_client.V1ObjectMeta(name=f"{name}-config"),
        data={"index.html": content}
    )
    api.create_namespaced_config_map(namespace=namespace, body=configmap)

    # Creiamo un Deployment con Nginx
    apps_api = k8s_client.AppsV1Api()
    deployment = k8s_client.V1Deployment(
        metadata=k8s_client.V1ObjectMeta(name=name),
        spec=k8s_client.V1DeploymentSpec(
            replicas=1,
            selector={"matchLabels": {"app": name}},
            template=k8s_client.V1PodTemplateSpec(
                metadata=k8s_client.V1ObjectMeta(labels={"app": name}),
                spec=k8s_client.V1PodSpec(
                    containers=[
                        k8s_client.V1Container(
                            name="nginx",
                            image="nginx:alpine",
                            volume_mounts=[k8s_client.V1VolumeMount(
                                name="html-volume",
                                mount_path="/usr/share/nginx/html",
                                read_only=True
                            )]
                        )
                    ],
                    volumes=[
                        k8s_client.V1Volume(
                            name="html-volume",
                            config_map=k8s_client.V1ConfigMapVolumeSource(name=f"{name}-config")
                        )
                    ]
                )
            )
        )
    )
    apps_api.create_namespaced_deployment(namespace=namespace, body=deployment)

    # Creiamo un Service per esporre la pagina
    service = k8s_client.V1Service(
        metadata=k8s_client.V1ObjectMeta(name=name),
        spec=k8s_client.V1ServiceSpec(
            selector={"app": name},
            ports=[k8s_client.V1ServicePort(port=80, target_port=80)]
        )
    )
    api.create_namespaced_service(namespace=namespace, body=service)

    kopf.info(f"Static page '{name}' created successfully!")

