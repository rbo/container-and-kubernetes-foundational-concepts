# Demoing foundational concepts of Containers and Kubernetes

## Start KinD Cluster

```shell
kind create cluster --name kind1 \
  --image kindest/node:v1.32.0
```

## Show Images

```shell
podman images
```

## Build Image

```shell
podman build \
  -t quay.io/rguske/simple-web-app:v1 \
  -f Containerfile
```

## Run Version 1

```shell
podman run -e PORT=8080 \
  -it --rm -p 8080:8080 \
  quay.io/rguske/simple-web-app:v1
```

## Customize Version 1

```shell
podman run -e MESSAGE="Hi folks :)" \
  -it --rm -p 8080:8080 \
  quay.io/rguske/simple-web-app:v1
```

## Create Version 2

```shell
podman build \
  -t quay.io/rguske/simple-web-app:v2 \
  -f Containerfile
```

## Run Version 2

```shell
podman run -e PORT=8080 \
  -it --rm -p 8080:8080 \
  quay.io/rguske/simple-web-app:v2
```

## Push the image to Quay

```shell
podman login quay.io -u rguske
```

```shell
podman push \
  quay.io/rguske/simple-web-app:v1 \
  quay.io/rguske/simple-web-app:v2
```

## Run the app in K8s

```shell
oc new-project demo
oc create deployment simple-web-app \
  --image=quay.io/rguske/simple-web-app:v1 
  --port=8080 --replicas=2 \
  --dry-run=client -oyaml > deploy.yaml

oc apply -f deploy.yaml
```

## Expose App locally

```shell
oc port-forward \
  deployment/simple-web-app 8080:8080
```

## Use ENV Variables

```shell
oc edit deployment simple-web-app
```

And add

```yaml
env:
  - name: MESSAGE
    value: 'HI THERE'
```

## Use a ConfigMap to apply the ENV

```yaml
oc create -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: simple-web-app-config
  namespace: demo
data:
  MESSAGE: "It's getting serious"
EOF
```

Adjust the deployment file:

```yaml
        envFrom:
        - configMapRef:
            name: simple-web-app-config
```

## Use Kubernetes Secrets to use Basic Auth

```shell
cd ../demo-app-basic-auth
```

Create the Kubernetes Secret:

```yaml
oc create -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: web-app-basic-auth-secret
  namespace: demo
type: Opaque
data:
  BASIC_AUTH_USER: dXNlcg==
  BASIC_AUTH_PASS: cjNkaDR0MSE=
EOF
```

Adjust the deployment file:

```yaml
        env:
        - name: BASIC_AUTH_USER
          valueFrom:
            secretKeyRef:
              name: web-app-basic-aut-secret
              key: BASIC_AUTH_USER
        - name: BASIC_AUTH_PASS
          valueFrom:
            secretKeyRef:
              name: web-app-basic-aut-secret
              key: BASIC_AUTH_PASS
```

Port forward the new app:

```shell
oc port-forward \
  deployment/web-app-basic-auth \
  8080:8080
```