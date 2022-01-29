---
title: "Creating Storage Account, Blob in AzureCLI"
date: 2021-01-10T21:30:30-04:00
categories:
  - blog
tags:
  - Azure
  - AzureCLI
---

# Create Azure Storage Account and a Storage Container using Azure CLI.

1. Create  storage account. Use the following command:

```
az storage account create \
 --name helloworld12345 \
 --resource-group resource-group-name \
 --location westus2
 ```

The storage will default to general purpose V2 and the access tier cannot be set, so it will default to hot.

2. Create a  container.

```
az storage container create \
 --account-name helloworld12345 \
 --name images \
 --auth-mode login \
 --public-access container
 ```