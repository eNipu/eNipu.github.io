# Build and store images by using Azure Container Registry

- Azure Container Registry enables you to store Docker images in the cloud, in an Azure storage account.

## What is Container Registry?

- Container Registry is an Azure service that you can use to create your own private Docker registries. 
- It contains more that one Docker images ususally called **repository**.
- Images can be build in the Container Registry.
- Container Registry also lets you automate tasks such as redeploying an app when an image is rebuilt.

## Why Container Registry instead of Docker Hub?

- Security
- One has much more control over who can see and use your images.
- *You can sign images to increase trust and reduce the chances of an image becoming accidentally (or intentionally) corrupted or otherwise infected.????*
- All images stored in a container registry are encrypted at rest.

## Using Container Registry

You create a registry by using either the Azure portal or the Azure CLI acr create command. In the following code example, the name of the new registry is **myregistry**:

``` az acr create --name myregistry --resource-group mygroup --sku standard --admin-enabled true```

### Build Image in the ACR

Instead of building an image yourself and pushing it to Container Registry, use the CLI to upload the Docker file and other files that make up your image. Container Registry will then build the image for you. Use the acr build command to run a build:

``` az acr build --file Dockerfile --registry myregistry --image myimage .```

N.B. The docker file need to be in the local dir.

## Build a Docker image and upload it to Azure Container Registry

```az acr build --registry <container_registry_name> --image webimage .```

## Deploy a web app from a repository in Azure Container Registry

- The registry that contains the image. The registry can be Docker Hub, Azure Container Registry, or some other private registry.

- The image. This item is the name of the repository.
- The tag. 
- Startup File. This item is the name of an executable file or a command to be run when the image is loaded. It's equivalent to the command that you can supply to Docker when running an image from the command line by using docker run.

## Enable Docker access to the Azure Container Registry (ACR)

You'll use Docker to login to the registry and pull the web image that you want to deploy. Docker needs a username and password to perform this action. The ACR allows you to enable the registry name as the username and admin access key as the password to allow Docker to login to your container registry.

1. Sign in to the Azure portal , navigate to all resources.
2. Select the container registry you created earlier to navigate to the Overview page for the container registry.
3. Under Settings, select Access keys.
4. Set the Admin user option to Enable. This change saves automatically.

## Create a web app

1. Select Create a resource > Web > Web App.
2. Specify these settings for each of the properties:
___
| Property  |  Value |
|:---|:---|
|  Subscription | Select your default Azure subscription in which you are allowed to create and manage resources.  |
| Resource Group | Reuse the existing resource group learn-deploy-container-acr-rg.  |
| Name  | Enter a unique name and make a note of it for later.  |
| Publish  | Docker Container  |
| OS  |  Linux |
|App Service plan |Use the default.|
___	
	
	
	
	
	