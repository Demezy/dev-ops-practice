# Lab 9: Introduction to Kubernetes


## Task 1: Kubernetes Setup and Basic Deployment

1. Deploy the application using:
```bash
kubectl create deployment app-python --image=dsnfljasdfjlajsdfjl/devops-app
```

2. Create a service to expose the application:
```bash
kubectl expose deployment app-python --type=LoadBalancer --port=5000 --target-port=5000
```

3. Output of `kubectl get pods,svc`:
```bash
NAME                              READY   STATUS    RESTARTS   AGE
pod/app-python-7fc7dd78f9-bx6nk   1/1     Running   0          42s

NAME                 TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
service/app-python   LoadBalancer   10.110.47.33   <pending>     5000:31863/TCP   17s
service/kubernetes   ClusterIP      10.96.0.1      <none>        443/TCP          2m33s
```

4. Pod logs from `kubectl logs app-python-7fc7dd78f9-bx6nk`:
```bash
The server is hosting on http://127.0.0.1:5000
 * Serving Flask app 'main'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.244.0.3:5000
```

5. Access the application using:
```bash
minikube service app-python
```

Output:
```bash
|-----------|------------|-------------|---------------------------|
| NAMESPACE   | NAME         | TARGET PORT   | URL                         |
| ----------- | ------------ | ------------- | --------------------------- |
| default     | app-python   | 5000          | http://192.168.49.2:31863   |
| ----------- | ------------ | ------------- | --------------------------- |
```

6. Cleanup resources:
```bash
kubectl delete service app-python
kubectl delete deployment app-python
```

## Task2: Declarative way using .yml files

1. Create deployment.yml file and apply it
```bash
kubectl apply -f k8s/deployment.yml
deployment.apps/app-python-depl created

```
2. Create service.yml file and apply it
```bash
kubectl apply -f k8s/service.yml       
service/app-python-service created

```

3. Check the pods and its output

```bash
kubectl get pods,svc
```

```bash

NAME                                   READY   STATUS         RESTARTS   AGE
pod/app-python-7fc7dd78f9-bx6nk        1/1     Running        0          44m
pod/app-python-depl-548979fcb7-2972z   0/1     ErrImagePull   0          71s
pod/app-python-depl-548979fcb7-7gzsx   0/1     ErrImagePull   0          71s
pod/app-python-depl-548979fcb7-9pmdt   0/1     ErrImagePull   0          71s

NAME                         TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/app-python           LoadBalancer   10.110.47.33    <pending>     5000:31863/TCP   44m
service/app-python-service   LoadBalancer   10.108.195.35   <pending>     5000:31223/TCP   25s
service/kubernetes           ClusterIP      10.96.0.1       <none>        443/TCP          46m

```
4. Output of ```minikube service --all``` command

```
|-----------|------------|-------------|---------------------------|
| NAMESPACE   | NAME                 | TARGET PORT   | URL                         |
| ----------- | -------------------- | ------------- | --------------------------- |
| default     | app-python           | 5000          | http://192.168.49.2:31863   |
| ----------- | ------------         | ------------- | --------------------------- |
| ----------- | -------------------- | ------------- | --------------------------- |
| NAMESPACE   | NAME                 | TARGET PORT   | URL                         |
| ----------- | -------------------- | ------------- | --------------------------- |
| default     | app-python-service   | 5000          | http://192.168.49.2:31223   |
| ----------- | -------------------- | ------------- | --------------------------- |
| ----------- | ------------         | ------------- | --------------              |
| NAMESPACE   | NAME                 | TARGET PORT   | URL                         |
| ----------- | ------------         | ------------- | --------------              |
| default     | kubernetes           |               | No node port                |
| ----------- | ------------         | ------------- | --------------              |
😿  service default/kubernetes has no node port
🏃  Starting tunnel for service app-python.
🏃  Starting tunnel for service app-python-service.
🏃  Starting tunnel for service kubernetes.
|-----------|--------------------|-------------|------------------------|
| NAMESPACE   | NAME                 | TARGET PORT   | URL                      |
| ----------- | -------------------- | ------------- | ------------------------ |
| default     | app-python           |               | http://127.0.0.1:49825   |
| default     | app-python-service   |               | http://127.0.0.1:49829   |
| default     | kubernetes           |               | http://127.0.0.1:49833   |
| ----------- | -------------------- | ------------- | ------------------------ |
🎉  Opening service default/app-python in default browser...
🎉  Opening service default/app-python-service in default browser...
🎉  Opening service default/kubernetes in default browser...
❗  Because you are using a Docker driver on darwin, the terminal needs to be open to run it.

```

Output of remote IP:

![](screenshots/output.png)

## Bonus Task
1. Construct ingress.yml and enable it
```bash
minikube addons enable ingress   
```
```bash
 You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
💡  After the addon is enabled, please run "minikube tunnel" and your ingress resources would be available at "127.0.0.1"
    ▪ Using image registry.k8s.io/ingress-nginx/controller:v1.9.4
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20231011-8b53cabe0
    ▪ Using image registry.k8s.io/ingress-nginx/kube-webhook-certgen:v20231011-8b53cabe0
🔎  Verifying ingress addon...
🌟  The 'ingress' addon is enabled
```
2. Apply ingress ```kubectl apply -f k8s/ingress.yml```
```bash
ingress.networking.k8s.io/combined-app-python created
```
2. Check pods
```bash
kubectl get pods,svc -n ingress-nginx
```
```bash
NAME                                            READY   STATUS      RESTARTS   AGE
pod/ingress-nginx-admission-create-5psfq        0/1     Completed   0          2m13s
pod/ingress-nginx-admission-patch-hxb7l         0/1     Completed   0          2m13s
pod/ingress-nginx-controller-7c6974c4d8-422m8   1/1     Running     0          2m13s

NAME                                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
service/ingress-nginx-controller             NodePort    10.108.136.84   <none>        80:30217/TCP,443:30191/TCP   2m13s
service/ingress-nginx-controller-admission   ClusterIP   10.105.111.50   <none>        443/TCP                      2m13s
```

3. Use curl command
```bash
curl --resolve "app.python:5000:192.168.49.2" -i http://app.python:5000
```

```bash

HTTP/1.1 200 OK
Date: Sun, 31 Mar 2024 17:51:23 GMT
Content-Type: text/html; charset=utf-8
Connection: keep-alive
Content-Language: en-US
<!DOCTYPE html>
<html>
    <head>
        <title>Current Time in Moscow</title>
    </head>
    <body>
        <h1>Current Time in Moscow: 2024-03-31 17:51:23</h1>
    </body>
</html>
```
