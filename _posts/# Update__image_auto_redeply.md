# Update the image and automatically redeploy the web app

Thhe target is to configure the continuous deployment of a web app that uses an image in Azure Container Registry.

## What is a **webhook**?

- Azure App Service supports continuous deployment using **webhooks**. 
- A webhook is a service offered by **Azure Container Registry**.

:whale: 
:red_circle:
A web app that uses App Service can subscribe to an Azure Container Registry webhook to receive notifications about updates to the image that contains the web app. When the image is updated, and App Service receives a notification, your app automatically restarts the site and pulls the latest version of the image.

## What is the Container Registry tasks feature?

- You use the tasks feature of Container Registry to rebuild your image whenever its source code changes automatically. 
- You configure a Container Registry task to monitor the GitHub repository that contains your code and trigger a build each time it changes. 
- If the build finishes successfully, Container Registry can store the image in the repository.
- If your web app is set up for continuous integration in App Service, it receives a notification via the webhook and updates the app.

## Enable continuous integration from App Service

-  App Services > Container settings > Container settings
  
The Container settings page of an App Service resource in the Azure portal automates the setup of continuous integration. If you turn on Continuous Deployment, App Service configures a webhook in your container registry to notify an App Service endpoint. Notifications from the registry that reach this endpoint cause your app to restart and pull the latest version of the container image.

## Extend continuous integration to source control by using a **Container Registry task
**

- Container Registry tasks must be created from the command line. 
- Unlike the ```az acr build``` command that we used earlier to build our image, the ```az acr task create``` command creates and registers a long-lived task.


## Configure continuous deployment and create a webhook
 
 - Enable continuous deployment ```-  App Services > Container settings > Container settings```
 - ```az acr build --registry <container_registry_name> --image webimage .```