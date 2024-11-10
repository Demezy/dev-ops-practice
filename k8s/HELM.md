# Helm Deployment Documentation

## Task 1: Basic Helm Setup

1. Created Helm chart using:
```bash
helm create app-python
```

2. Modified values.yaml to use my Docker image:
```yaml
image:
  repository: dsnfljasdfjlajsdfjl/devops-app
  tag: "latest"
```

3. Installed the chart:
```bash
helm install app-python ./app-python/
```

4. Output of kubectl get pods,svc:
```bash
NAME                                   READY   STATUS    RESTARTS   AGE
pod/app-python-7fc7dd78f9-bx6nk        1/1     Running   0          44m

NAME                         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/app-python-service   LoadBalancer   10.108.195.35   <pending>     5000:31223/TCP   25s
```

## Task 2: Helm Hooks Implementation

1. Added pre-install and post-install hooks
2. Verified hooks execution:

```bash
kubectl get po
NAME                          READY   STATUS      RESTARTS   AGE
app-python-pre-install        0/1     Completed   0          5m
app-python-post-install       0/1     Completed   0          4m
app-python-7fc7dd78f9-bx6nk   1/1     Running     0          4m
```

3. Pre-install hook details:
```bash
kubectl describe po app-python-pre-install
Name:         app-python-pre-install
Namespace:    default
...
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  5m    default-scheduler  Successfully assigned default/app-python-pre-install to minikube
  Normal  Pulled     5m    kubelet            Container image "busybox" already present on machine
  Normal  Created    5m    kubelet            Created container pre-install
  Normal  Started    5m    kubelet            Started container pre-install
```

4. Post-install hook details:
```bash
kubectl describe po app-python-post-install
Name:         app-python-post-install
Namespace:    default
...
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  4m    default-scheduler  Successfully assigned default/app-python-post-install to minikube
  Normal  Pulled     4m    kubelet            Container image "busybox" already present on machine
  Normal  Created    4m    kubelet            Created container post-install
  Normal  Started    4m    kubelet            Started container post-install
```

Note: Both hooks have the `helm.sh/hook-delete-policy: hook-succeeded` annotation to ensure cleanup after successful execution.