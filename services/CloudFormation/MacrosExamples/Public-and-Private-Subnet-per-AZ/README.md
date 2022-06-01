## Summary

This is a Cloudformation Macro used to dynamically add a public and private subnet per Availability Zone when launching a template.  When  CreateStack template is launched and a change set is created,  Macro (named 'CreateSubnetsPerAZ') will dynamically add resources to  template for a public and private subnet per available AZ

## How to Use 

- Create a stack using  `CreateMacro` template, which will create  Lambda function and register it as a CFN Macro (with  name: 'CreateSubnetsPerAZ')
- Now  Macro is registered in your AWS account, and you can reference this macro in any CFN template using a top-level resource, similar to  following:

```yaml
Transform:
  - CreateSubnetsPerAZ
```

- Create a stack using  `CreateStack` template.   template contains a VPC with a public and private subnet.  When this template is launched and  change set is created,  macro will add a private and public subnet to every AZ available in region.  If this template is launched in us-west-2, re 2 public and 2 private subnets.  If launched in us-east-1, re 6 public and 6 private subnets

## References 

See  recently announced CloudFormation Macros feature: [CloudFormation Macros](https://aws.amazon.com/blogs/aws/cloudformation-macros)

## /HT 

[@mike-mosher](https://github.com/mike-mosher)


