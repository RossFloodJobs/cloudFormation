# Count CloudFormation Macro

 `Count` macro provides a template-wide `Count` property for CloudFormation resources. It allows you to specify multiple resources  same type without having to cut and paste.

## How to install and use  Count macro in your AWS account

### Deploying

1. You will need an S3 bucket to store  CloudFormation artifacts:
    * If you don't have one already, create one with `aws s3 mb s3://<bucket name>`

2. Package  Macro CloudFormation template.  provided template uses [ AWS Serverless Application Model](https://aws.amazon.com/about-aws/whats-new/2016/11/introducing--aws-serverless-application-model/) so must be transformed before you can deploy it.

    ```shell
    aws cloudformation package \
        --template-file template.yaml \
        --s3-bucket <your bucket name here> \
        --output-template-file packaged.yaml
    ```

3. Deploy  packaged CloudFormation template to a CloudFormation stack:

    ```shell
    aws cloudformation deploy \
        --stack-name Count-macro \
        --template-file packaged.yaml \
        --capabilities CAPABILITY_IAM
    ```

4. To test out  macro's capabilities, try launching  provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name Count-test \
        --template-file test.yaml \
        --capabilities CAPABILITY_IAM
    ```

### Usage

To make use  macro, add `Transform: Count` to  top level your CloudFormation template.

To create multiple copies a resource, add a Count propert with an integer value.

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: Count
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Count: 3
  SQS:
    Type: AWS:::SQS::Queue
    Count: 2
```
#### Note
This will cause  resource "Bucket" to be multiplied 3 times.  new template will contain Bucket1, Bucket2 and Bucket3 but will not contain Bucket as this removed.

### Using decimal placeholders
When resources are multiplied, you can put a decimal placeholder %d into any string value you wish to be replaced with  iterator index number.

e.g. 
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Transform: Count
Resources:
  Bucket:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: TestKey
          Value: my bucket %d
    Count: 3
```

Using this example,  processed template will result become:
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  Bucket1:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: TestKey
          Value: my bucket 1
  Bucket2:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: TestKey
          Value: my bucket 2
  Bucket3:
    Type: AWS::S3::Bucket
    Properties:
      Tags:
        - Key: TestKey
          Value: my bucket 3
```

### Important - Naming resources

You cannot use Count on resources use a hardcoded name (`Name:` property). Duplicate names will cause a CloudFormation runtime failure.
If you wish to specify a name n you can use  decimal place holder %d in  name which will cause  name to incorporate  iterator value.

e.g. 
```yaml
AWSTemplateFormatVersion: "2010-09-09"
Resources:
  Bucket1:
    Type: AWS::S3::Bucket
    Properties:
        BucketName: MyBucket%d
```

## Author

[Jose Ferraris](https://github.com/j0lly)
AWS ProServ DevOps Consultant
Amazon Web Services
