# How to install and use  Boto3 macro in your AWS account

 `Boto3` macro adds  ability to create CloudFormation resources represent operations performed by [boto3](http://boto3.readdocs.io/). Each `Boto3` resource represents one function call.

A typical use case for this macro might be, for example, to provide some basic configuration resources.

## Deploying

1. You will need an S3 bucket to store  CloudFormation artifacts:
    * If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package  CloudFormation template.  provided template uses [ AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing--aws-serverless-application-model/) so must be transformed before you can deploy it.

    ```shell
    aws cloudformation package \
        --template-file macro.template \
        --s3-bucket <your bucket name here> \
        --output-template-file packaged.template
    ```

3. Deploy  packaged CloudFormation template to a CloudFormation stack:

    ```shell
    aws cloudformation deploy \
        --stack-name boto3-macro \
        --template-file packaged.template \
        --capabilities CAPABILITY_IAM
    ```

4. To test out  macro's capabilities, try launching  provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name boto3-macro-example \
        --template-file example.template
    ```

## Usage

To make use  macro, add `Transform: Boto3` to  top level your CloudFormation template.

Here is a trivial example template adds a readme file to a new CodeCommit repository:

```yaml
Transform: Boto3
Resources:
  Repo:
    Type: AWS::CodeCommit::Repository
    Properties:
      RepositoryName: my-repo

  AddReadme:
    Type: Boto3::CodeCommit.put_file
    Mode: Create
    Properties:
      RepositoryName: !GetAtt Repo.Name
      BranchName: master
      FileContent: "Hello, world!"
      FilePath: README.md
      CommitMessage: Add a readme file
      Name: CloudFormation
```

## Features

### Resource type

 resource `Type` is used to identify a [boto3 client](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/clients.html) and  method client to execute.

 `Type` must start with `Boto3::` and be followed by  name a client, a `.` and finally  name a method.

 client name converted to lower case so you can use resource names look similar to or CloudFormation resource types.

Examples:
* `Boto3::CodeCommit.put_file`
* `Boto3::IAM.put_user_permissions_boundary`
* `Boto3::EC2.create_snapshot`

### Resource mode

 resource may contain a `Mode` property which specifies wher  boto3 call should be made on `Create`, `Update`, `Delete` or any combination those.

 `Mode` may eir be a string or a list strings. For example:

* `Mode: Create`
* `Mode: Delete`
* `Mode: [Create, Update]`

### Resource properties

 `Properties`  resource passed to  specified boto3 method as arguments.  name each property modified so it started with a lower-case character so you can use property names look similar to or CloudFormation resource properties.

### Controlling  order execution

You can use  standard CloudFormation property `DependsOn` when you need to ensure your `Boto3` resources are executed in  correct order.

## Examples


 following resource:

```yaml
ChangeBinaryTypes:
  Type: Boto3::CloudFormation.execute_change_set
  Mode: [Create, Update]
  Properties:
    ChangeSetName: !Ref ChangeSet
    StackName: !Ref Stack
```

will result in running  equivalent  following:

```python
boto3.client("cloudformation").execute_change_set(changeSetName=<value ChangeSet>, stackName=<value StackName>)
```

when  stack is created or updated.

## Author

[Steve Engledow](https://linkedin.com/in/stilvoid)  
Senior Solutions Builder  
Amazon Web Services
