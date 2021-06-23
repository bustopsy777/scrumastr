## Setup to Chatscrum on Helm

Chatscrum is a task management software. That allow users to giv track of their task in an agile system. It also has
built chat system which allows user to communicate with each other.

## Install Helm CLI
```
curl -LO https://get.helm.sh/helm-v3.6.1-linux-amd64.tar.gz
tar -C /tmp/ -zxvf helm-v3.6.1-linux-amd64.tar.gz
rm helm-v3.6.1-linux-amd64.tar.gz
mv /tmp/linux-amd64/helm /usr/local/bin/helm
chmod +x /usr/local/bin/helm
```

## Create Our first Chart
```
cd helm
helm create chatscrum
```

## Cleanup the template
We can delete unwanted files:
- delete everything under templates, keeping only _helpers.tpl
- delete tests folder under templates

## Add kubernetes files to our new Chart
copy the following files into our chatscrum-app/templates/ folder

```
- <GitRepo>/yamlfiles/deployments/cs-deployment.yaml
- <GitRepo>/yamlfiles/deployments/cs-service.yaml
- <GitRepo>/yamlfiles/database/mysql-deploy.yaml
- <GitRepo>/yamlfiles/deployments/mysql-service.yaml
- <GitRepo>/yamlfiles/deployments/deployment.yaml
- <GitRepo>/yamlfiles/deployments/deployment.yaml

```

## Test the rendering of our template

```
helm template chatscrum chatscrum-app
```

## Install our app using our Chart
```
helm install chatscrum chatscrum-app
```

#list our releases

helm list

# See our deployed components

kubectl get all
kubectl get pv
kubectl get pvc

## Value injections for our Chart

For CI systems, we may want to inject an image tag as a build number

Basic parameter injection:

# values.yaml
```
deployment:
  image: "jerito1/chatscrum"
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "dev"
name: "cs-int"
```

```
#chatscrum-deployment.yaml

image: `{{ .Values.deployment.image }}:{{ .Values.deployment.tag }}


#upgrade our release

helm upgrade chatscrum-app chatscrum --values ./chatscrum/values.yaml

#see revision increased

helm list

```

## Make our chart more generic

Let's make our chart generic so it can be reused:
For the following objects, replace chatscrum-deployment and chatscrum-app to inject "{{ .Values.name }}"

- chatscrum-deployment.yaml
- services.yaml
- database-deployment.yaml
- database-service.yaml

Now that our application is generic
We can deploy another copy of it.


Rename values.yaml to int-values.yaml. Create our second app values file stage-values.yaml



















