# Deploy containers using Elastic Container Service and CloudFormation

Several combinations template are available in this folder. You can deploy containers with two different networking approaches:

- Public VPC subnet with direct internet access
- Private VPC subnet without direct internet access

You can choose two different options for hosting  containers:

- AWS Fargate for hands-off container execution without managing EC2 instances
- Self managed cluster EC2 hosts for control over instance type, or to use reserved or spot instances for savings

You can also choose between two different ways sending traffic to  container:

- A public facing load balancer accepts traffic from anyone on  internet (ideal for a public facing web service)
- A private, internal load balancer only accepts traffic from or containers in  cluster (ideal for a private, internal service).

To use se templates launch a cluster template for  launch type and networking stack you want. n launch a service template for each service you want to run in  cluster. When launching a service template its important to make sure  "StackName" value is filled in with  same name you selected for  name your cluster stack.

Each  service stacks has default values prefilled for launching a simple Nginx container, but can be adjusted to launch your own container.

## Fully Public Container

![public subnet public load balancer](images/public-task-public-loadbalancer.svg)

This architecture deploys your container into its own VPC, inside a public facing network subnet.  containers are hosted with direct access to  internet, and y are also accessible to or clients on  internet via a public facing application load balancer.

### Run in AWS Fargate

1. Launch  [fully public](FargateLaunchType/clusters/public-vpc.yml) or  [public + private](FargateLaunchType/clusters/private-vpc.yml) cluster template
2. Launch  [public facing service template](FargateLaunchType/services/public-service.yml).

### Run on EC2

1. Launch  [fully public](EC2LaunchType/clusters/public-vpc.yml) or  [public + private](EC2LaunchType/clusters/private-vpc.yml) cluster template
2. Launch  [public facing service template](EC2LaunchType/services/public-service.yml).

&nbsp;

&nbsp;

## Publicly Exposed Service with Private Networking

![private subnet public load balancer](images/private-task-public-loadbalancer.svg)

This architecture deploys your container into a private subnet.  containers do not have direct internet access, or a public IP address. ir outbound traffic must go out via a NAT gateway, and receipients requests from  containers will just see  request orginating from  IP address  NAT gateway. However, inbound traffic from  public can still reach  containers because re is a public facing load balancer can proxy traffic from  public to  containers in  private subnet.

### Run in AWS Fargate

1. Launch  [public + private](FargateLaunchType/clusters/private-vpc.yml) cluster template
2. Launch  [public facing, private subnet service template](FargateLaunchType/services/private-subnet-public-service.yml).

### Run on EC2

1. Launch  [public + private](EC2LaunchType/clusters/private-vpc.yml) cluster template
2. Launch  [public facing, private subnet service template](EC2LaunchType/services/public-service.yml).

&nbsp;

&nbsp;

## Internal Service with Private Networking

![private subnet private load balancer](images/private-task-private-loadbalancer.svg)

This architecture deploys your container in a private subnet, with no direct internet access. Outbound traffic from your container goes through an NAT gateway, and receipients requests from  containers will just see  request orginating from  IP address  NAT gateway. re is no acess to  container for  public. Instead re is a private, internal load balancer only accepts traffic from or containers in  cluster. This is ideal for an internal service is used by or services, but should not be used directly by  public.

### Run in AWS Fargate

1. Launch  [public + private](FargateLaunchType/clusters/private-vpc.yml) cluster template
2. Launch  [private service, private subnet template](FargateLaunchType/services/private-subnet-private-service.yml).

### Run on EC2

1. Launch  [public + private](EC2LaunchType/clusters/private-vpc.yml) cluster template
2. Launch  [private service, private subnet template](EC2LaunchType/services/private-service.yml).

