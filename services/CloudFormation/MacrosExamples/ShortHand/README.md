# ShortHand CloudFormation Macro

 `ShortHand` macro provides convenience syntax to allow you to create short CloudFormation templates expand into larger documents upon deployment to a stack.

See below for instructions to install and use  macro and for a full description  macro's features.

## How to install and use  ShortHand macro in your AWS account

### Deploying

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
        --stack-name shorthand-macro \
        --template-file packaged.template \
        --capabilities CAPABILITY_IAM
    ```

4. To test out  macro's capabilities, try launching  provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name shorthand-macro-example \
        --template-file example.template \
        --capabilities CAPABILITY_IAM
    ```

### Usage

To make use  macro, add `Transform: ShortHand` to  top level your CloudFormation template.

Here is a trivial example template:

```yaml
Transform: ShortHand
Resources:
  - S3::Bucket
```

## Features

 ShortHand macro provides  following features to your CloudFormation templates:

* A resource can be defined by a single string contains its name, type, and proprties.

    For example:

    ```yaml
    "MyBucket AWS::S3::Bucket AccessControl=PublicRead"
    ```

    This would translate into:

    ```yaml
    MyBucket:
      Type: AWS::S3::Bucket
      Properties:
        AccessControl: PublicRead
    ```

* You can omit  resource name and one generated for you.

    For example:

    ```yaml
    "AWS::S3::Bucket AccessControl=PublicRead"
    ```

* You can shorten  resource type name by omitting parts it from  left. As long as  result unambiguously refers to a valid CloudFormation resource type,  `ShortHand` macro will deal with it.

    For example:

    ```yaml
    "Bucket AccessControl=PublicRead"
    ```

    And:

    ```yaml
    "EC2::Instance"  # We need  `EC2::` prefix as re are or resource types end with `Instance` (e.g. `AWS::OpsWorks::Instance`)
    ```

* All string values automatically use `Fn::Sub` if  value contains a sequence like `${something}`

    For example:

    ```yaml
    "MyBucketPolicy BucketPolicy Bucket=${MyBucket}"
    ```

    Will result in:

    ```yaml
    MyBucketPolicy:
      Type: AWS::S3::BucketPolicy
      Properties:
        Bucket:
          Fn::Sub: "${MyBucket}"
    ```

* You can address sub-properties using dot-notation.

    For example:

    ```yaml
    "MyBucket Bucket VersioningConfiguration.Status=Enabled"
    ```

* If you need to specify lots properties (as is often  case) you can use object synax instead a string.

    For example:

    ```yaml
    MyBucket S3::Bucket:
      AccessControl: PublicRead
      VersioningConfiguration.Status: Enabled
    ```

* To make all se features possible,  `Resources` section your template must now be an array rar than an object.

    A full example template would look like this:

    ```yaml
    Transform: ShortHand

    Parameters:
      Name:
        Type: String

    Resources:
      - S3::Bucket BucketName=${Name}
    ```

## Author

[Steve Engledow](https://linkedin.com/in/stilvoid)  
Senior Solutions Builder  
Amazon Web Services
