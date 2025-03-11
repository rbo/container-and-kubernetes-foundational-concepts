# Demoing foundational concepts of Containers and Kubernetes

## Start KinD Cluster

`kind create cluster --name kind1 --image kindest/node:v1.32.0@sha256:c48c62eac5da28cdadcf560d1d8616cfa6783b58f0d94cf63ad1bf49600cb027`

## Show Images

`podman images`

## Build Image

`podman build -t quay.io/rguske/simple-web-app:v1 -f Containerfile`

## Run Version 1

`podman run -e PORT=8080 -it --rm -p 8080:8080 quay.io/rguske/simple-web-app:v1`

## Customize Version 1

`podman run -e MESSAGE="Hi folks :)" -it --rm -p 8080:8080 quay.io/rguske/simple-web-app:v1`

## Create Version 2

`podman build -t quay.io/rguske/simple-web-app:v2 -f Containerfile`

## Run Version 2

`podman run -e PORT=8080 -it --rm -p 8080:8080 quay.io/rguske/simple-web-app:v2`

## Push the image to Quay

`podman login quay.io -u rguske`

`podman push quay.io/rguske/simple-web-app:v1 quay.io/rguske/simple-web-app:v2`

## Run the app in K8s

`oc create ns demo`

`oc create deployment simple-web-app --image=quay.io/rguske/simple-web-app:v1 --namespace=demo --port=8080 --replicas=2 --dry-run=client -oyaml > deploy.yaml`

`oc apply -f deploy.yaml`

## Expose App locally

`oc port-forward deployment/simple-web-app 8080:8080 -n demo`

// ## Use ENV Variables
// 
// ```yaml
//         env:
//         - name: MESSAGE
//           value: 'HI THERE'
// ```
// 
// Apply the changes:
// 
// `oc apply -f deploy.yaml`

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

`cd ../demo-app-basic-auth`

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

`oc port-forward deployment/web-app-basic-auth 8080:8080 -n demo`