---
title: "Create, Delete an SQL Database using Azure CLI"
date: 2021-01-10T19:15:30-04:00
categories:
  - blog
tags:
  - Azure
  - SQL
  -AzureCLI
---

# Create, Delete an Azure SQL Database using Azure CLI.

1. Login to Azure CLI 
```az login```

## Create SQL Server

``` 
az sql server create \
--admin-user db_admin_name \
--admin-password p@ssword \
--name db_server_name_unique \
--resource-group resource-group-name \
--location westus2 \
--enable-public-network true \
--verbose
```

## Create Firewall rule
Next, we have to create two firewall rules. 

1. The first one is to allow Allow Azure services and resources to access the server we just created.
    ```
    az sql server firewall-rule create \
    -g resource-group-name \
    -s db_server_name_unique \
    -n azureaccess \
    --start-ip-address 0.0.0.0 \
    --end-ip-address 0.0.0.0 \
    --verbose
    ```
This start and end ip addresss is to cover entire Azure internal IP address.
```-n``` is name if the access
```-s``` is database server we created.


1. Create clientIp firewall rule: This second rule is to set your computer's public Ip address to the server's firewall. 
   ```curl ifconfig.me``` in mac to find your public IP. ```ipconfig``` in windows to check your public IP.

    ```
    az sql server firewall-rule create \
    -g resource-group-name \
    -s db_server_name_unique \
    -n clientip \
    --start-ip-address <PUBLIC-IP-ADDRESS> \
    --end-ip-address <PUBLIC_IP_ADDRESS> \
    --verbose
    ```

    The difference is ```-n clientip```.

## Create SQL Database
Finally, to create the database itself,  use the command below.

 ```
az sql db create \
--name unique_db_name \
--resource-group resource-group-name \
--server db_server_name_unique \
--tier Basic \
--verbose
```

## Cleanup
 CLI commands for cleaning up the SQL resources below.

- Delete DB
```
az sql db delete \
--name unique_db_name \
--resource-group resource-group-name \
--server db_server_name_unique \
--verbose
```
- Delete SQL Server

```
az sql server delete \
--name db_server_name_unique \
--resource-group resource-group-name \
--verbose
```
