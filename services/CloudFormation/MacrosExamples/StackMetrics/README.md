# StackMetrics macro

When  `StackMetrics` macro is used in a CloudFormation template, any CloudFormation stack deployed from template will output custom CloudWatch metrics for  stack.

* CloudFormation stack operations
    * Creates
    * Updates
    * Deletes
* CloudFormation resources created

Metrics are provided both per stack and overall across all stacks are using  macro.

 `macro.template` template also creates a simple dashboard for viewing  aggregated data from se metrics.

See `example.template` for example usage.

## How to install and use  CloudFormation macro in your AWS account

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
        --stack-name stackmetrics-macro \
        --template-file packaged.template \
        --capabilities CAPABILITY_IAM
    ```

4. To test out  macro's capabilities, try launching two stacks from  provided example template:

    ```shell
    aws cloudformation deploy \
        --stack-name stackmetrics-macro-example-1 \
        --template-file example.template \
        --capabilities CAPABILITY_IAM

    aws cloudformation deploy \
        --stack-name stackmetrics-macro-example-2 \
        --template-file example.template \
        --capabilities CAPABILITY_IAM
    ```

### Usage

To make use  macro, add `Transform: StackMetrics` to  top level your CloudFormation template.

Here is a trivial example template:

```yaml
Transform: StackMetrics
Resources:
  Bucket:
    Type: S3::Bucket
```

To see  stack metrics, you can check  `CloudFormation-Stacks` dashboard in  CloudWatch console.

## Authors

[Steve Engledow](https://linkedin.com/in/stilvoid)  
Senior Solutions Builder  
Amazon Web Services

[Jason Gregson](https://linkedin.com/in/jgregson)  
Global Solutions Architect  
Amazon Web Services
