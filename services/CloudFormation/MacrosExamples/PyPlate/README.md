# PyPlate

Run arbitrary python code in your CloudFormation templates

## Basic Usage

Place python code as a literal bock anywhere in your template,  literal block replaced with  contents of
 `output` variable defined in your code. re are several variables available to your code:

params: dict containing  contents  templateParameterValues
template: dict containing  entire template
account_id: AWS account ID
region: AWS Region

```yaml
AWSTemplateFormatVersion: "2010-09-09"
Description: tests String macro functions
Parameters:
  Tags:
    Default: "Env=Prod,Application=MyApp,BU=ModernisationTeam"
    Type: "CommaDelimitedList"
Resources:
  S3Bucket:
    Type: "AWS::S3::Bucket"
    Properties:
      Tags: |
        #!PyPlate
        output = []
        for tag in params['Tags']:
           key, value = tag.split('=')
           output.append({"Key": key, "Value": value})
Transform: [PyPlate]
```

## Author

[Jay McConnell](https://github.com/jaymccon)  
Partner Solutions Architect  
Amazon Web Services
