# Running RedLM and local inference services in Kubernetes on a cluster of RTX PCs

To run services in kubernetes, set up a cluster. I use microk8s for setting up a local cluster. You will need the `nvidia` add-on for GPU support.

Make a copy of the `k8s/.env.sample` file and rename it to `k8s/.env`. Replace values as needed.

The `.env` file is used to create a ConfigMap, and Kustomize uses the ConfigMap to replace placeholder values in the manifests.

Run the following command from the root of the repository to preview the manifests the Kustomize will create:

```
kubectl kustomize k8s
```

To apply the changes, you can run the following command:

```
kubectl apply -k k8s/
```