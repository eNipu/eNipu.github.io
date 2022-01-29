---
title: "Azure Glossary"
date: 2021-01-09T20:00:30-04:00
categories:
  - blog
tags:
  - Azure
---


|Key Term | Definition
|:--- | :---
|Subscription |Multiple of these can exist within a single Azure account; often used for billing and other management purposes.
| Resource Group | Help to organize resources you use, such as Virtual Machines, App Services or storage, in order to make resource management easier. Groups are often set up for different projects or regions.
Region | Locations of Azure data centers around the world. The closer the region of app resources is to the end user, the lower the latency experienced.
ARM Templates | Created within Azure Resource Manager to more easily spin up a set of given resources multiple times.
Virtual Machine | An Azure IaaS option giving you full access to the underlying operating system of a compute resource. These can be either Windows or Linux machines, with great availability, scalability and redundancy. These require more on-going maintenance and up-keep by cloud developers.
App Service| An Azure PaaS option allowing developers to focus more on their apps than the underlying infrastructure. It is an HTTP-based service for hosting web applications, REST APIs, and mobile back ends. It supports multiple languages and continuous deployment. While they are good for scaling, there is also a limit of up to 14 GB or 4 CPU cores on the highest tier.
App Service Plan|Contains certain settings of an App Service, such as region, number of VM instances (App Services still run on VMs, but the developer does not have control of the underlying VM, and the app may share the VM with other apps), size of those instances, and pricing tier.
Azure Batch | Used for running large-scale and high-performance compute applications beyond the capabilities of an App Service.
Azure Functions | A serverless, event-driven, compute-on-demand platform .
Container Instances | A platform for deploying serverless docker containers, without the container orchestration provided by AKS.
Service Fabric|Microsoft's own distributed systems platform, similar to Kubernetes.
Azure Kubernetes Service (AKS)|Microsoft's own platform for hosting and managing Kubernetes, including deploying docker containers into clusters (covered in a later course).
