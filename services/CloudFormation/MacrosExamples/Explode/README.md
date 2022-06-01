# Explode CloudFormation Macro

 `Explode` macro provides a template-wide `Explode` property for CloudFormation resources, conditions and outputs. Similar to  Count macro, it will create multiple copies a template Resource, but looks up values to inject into each copy in a Mapping, and this capability is expanded to Condition and Output statements in  template.

## How to install and use  Explode macro in your AWS account

### Deploying

1. You will need an S3 bucket to store  CloudFormation artifacts. If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package  Macro CloudFormation template.  provided template uses [ AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing--aws-serverless-application-model/) so must be transformed before you can deploy it.

```shell
aws cloudformation package \
    --template-file macro.yml \
    --s3-bucket <your bucket name here> \
    --output-template-file packaged.yaml
```

3. Deploy  packaged CloudFormation template to a CloudFormation stack:

```shell
aws cloudformation deploy \
    --stack-name Explode-macro \
    --template-file packaged.yaml \
    --capabilities CAPABILITY_IAM
```

4. To test out  macro's capabilities, try launching  provided example template:

```shell
aws cloudformation deploy \
    --stack-name Explode-test \
    --template-file test.yaml \
    --capabilities CAPABILITY_IAM
```

### Usage

To make use  macro, add `Transform: Explode` to  top level your CloudFormation template.

Add a mapping (to  `Mappings` section your template) which defines  instances each template statement you want to explode by instantiating multiple times. Each entry in  mapping used for anor copy  resource/condition/output, and  values inside it copied into instance.  entry name appended to  statement's name, unless a value `ResourceName` is given, which if present used as  complete instance name.  Note `ResourceName` is only useful if exploding a single statement as orwise it creates naming conflicts.

For each statement you want to explode, add an `ExplodeMap` value at  top level pointing at  entry from your Mappings which should be used. You can use  same mapping against multiple resource entries.

Inside  resource properties, you can use `!Explode KEY` to pull  value `KEY` out your mapping.

An example is probably in order:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: Explode
Mappings:
  BucketMap:
    Monthly:
      ResourceName: MyThirtyDayBucket
      Retention: 30
    Yearly:
      Retention: 365

Resources:
  Bucket:
    ExplodeMap: BucketMap
    Type: AWS::S3::Bucket
    Properties:
      LifecycleConfiguration:
        Rules:
          -
            ExpirationInDays: !Explode Retention
            Status: Enabled
```

This will result in two Bucket resources; one named `MyThirtyDayBucket` with a
lifecycle rule for 30 day retention, and anor named `BucketYearly` with 365
day retention.

### Important - Naming resources

You cannot use Explode on resources use a hardcoded name (`Name:`
property). Duplicate names will cause a CloudFormation runtime failure.
If you wish to specify a name n you must use `!Explode` with a mapped value
to make each resource's name unique.

For example:

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Mappings:
  BucketMap:
    Example:
      Name: MyExampleBucket
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    ExplodeMap: BucketMap
    Properties:
        BucketName: !Explode Name
```

## Author

[James Seward](https://github.com/jamesoff); AWS Solutions Architect, Amazon Web Services
