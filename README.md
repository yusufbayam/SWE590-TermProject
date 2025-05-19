In this project, you are expected to design, implement, and evaluate
a cloud-native architecture using a commercial Cloud Service Provider
(Google Cloud Platform – GCP). You will integrate containerized
workloads, virtual machines, and serverless functions to create a
complete, scalable, and efficient system.
Scope & Requirements
You are not required to write application code from scratch. You may
reuse projects from earlier coursework or use open-source code from
repositories (e.g., GitHub). However, the entire cloud-native design
and implementation must be your original work.
Your architecture must include all of the following:
1. Containerized workloads on Kubernetes, deployed in a scalable
manner (e.g., using Deployments, HPA).
2. Virtual Machines, integrated into your system and serving a
functional role.
3. Serverless Functions, implemented using Google Cloud Functions.
Performance Evaluation of your design

You must design performance tests to evaluate the behavior of
your system under realistic workloads.
Use Locust to simulate realistic user behavior and generate
traffic.
Identify relevant independent and dependent variables (e.g.,
request load, response time, CPU utilization).
Collect and interpret metrics such as:
* Request latency
* Throughput (requests per second)
* Resource usage (CPU, memory)
* Error rates under loadTechnical Report Requirements

You will submit a report that documents your entire work. It should
include:
* A cloud architecture diagram
* A description of each component and how they interact
* A step-by-step explanation of the deployment process
* Locust experiment design and parameter configurations
* Visualized performance results (e.g., charts, graphs)
* A clear explanation of the observed results, supported by
reasoning and performance metrics
* A cost breakdown demonstrating compliance with the $300 GCP
trial budget

Project Deliverables
Your submission must include:
* A fully working system deployed on GCP
* A comprehensive term project report (as described above)
* A demo video showcasing your system in action (maximum 2
minutes)
A GitHub repository containing:
* Application source code
* All deployment scripts/manifests (e.g., Kubernetes YAMLs,
Terraform, etc.)
* Locust test scripts
* A README.md file with clear instructions to replicate your
setup

Cloud Platform & Budget Constraints
* You are required to use Google Cloud Platform (GCP).
* You must stay within the $300 free trial credit for all
resources used.
* You are responsible for monitoring and optimizing your
spending.

Bonus Challenge (Optional)
* You may earn bonus points if you use Terraform to implement your
cloud infrastructure using Infrastructure as Code (IaC). This
demonstrates advanced DevOps practices and improves system
reproducibility.
