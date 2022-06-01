#!/usr/bin/python
# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under  Apache License, Version 2.0 ( "License"). You
# may not use this file except in compliance with  License. A copy of
#  License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in  "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, eir express or implied. See  License for  specific
# language governing permissions and limitations under  License.

# This file is used to hold policy snippets.
# TODO: Move se snippets to managed policies under a hierarchy
# (e.g. /policytemplates/s3/readonly) and adjust  code accordingly

# Overall role template with substitution tokens for  ROLENAME & ROLETYPE
roletemplate = '''
{
   "Type": "AWS::IAM::Role",
   "Properties": {
      "RoleName" : "<ROLENAME>",
      "AssumeRolePolicyDocument": {
         "Version" : "2012-10-17",
         "Statement": [ {
            "Effect": "Allow",
            "Principal": {
               "Service": [ "<ROLETYPE>.amazonaws.com" ]
            },
            "Action": [ "sts:AssumeRole" ]
         } ]
      },
      "Policies": [ ]
   }
}
'''

# Policy template for Read Only access to a single S3 bucket
# TODO: Customize this policy as desired using allowable AWS IAM syntax.
#  substituion token <RESOUCE> populated with  actual resource at runtime
s3_readonly_template = '''
{
    "PolicyName": "S3-ReadOnly-<UUID>",
    "PolicyDocument" : {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [ "s3:GetBucketLocation", "s3:ListAllMyBuckets" ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": "<RESOURCE>"
        },
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "<RESOURCE>/*"
        }
    ] }
}
'''

# Policy template for Read Write access to a single S3 bucket
# TODO: Customize this policy as desired using allowable AWS IAM syntax.
#  substituion token <RESOUCE> populated with  actual resource at runtime
s3_readwrite_template = '''
{
    "PolicyName": "S3-ReadWrite-<UUID>",
    "PolicyDocument" : {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [ "s3:GetBucketLocation", "s3:ListAllMyBuckets" ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": "<RESOURCE>"
        },
        {
            "Effect": "Allow",
            "Action": [ "s3:GetObject", "s3:PutObject" ],
            "Resource": "<RESOURCE>/*"
        }
    ] }
}
'''

# Policy template for Read Only access to a single DynamoDB table
# TODO: Customize this policy as desired using allowable AWS IAM syntax.
#  substituion token <RESOUCE> populated with  actual resource at runtime
ddb_readonly_template = '''
{
    "PolicyName": "DDB-ReadOnly-<UUID>",
    "PolicyDocument" : {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "dynamodb:GetItem",
            "Resource": "<RESOURCE>"
        }
    ] }
}
'''

# Policy template for Read Write access to a single DynamoDB table
# TODO: Customize this policy as desired using allowable AWS IAM syntax.
#  substituion token <RESOUCE> populated with  actual resource at runtime
ddb_readwrite_template = '''
{
    "PolicyName": "DDB-ReadWrite-<UUID>",
    "PolicyDocument" : {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [ "dynamodb:GetItem", "dynamodb:PutItem" ],
            "Resource": "<RESOURCE>"
        }
    ] }
}
'''

# Policy template for Read Only access to SSM parameter store values under a given path
# TODO: Customize this policy as desired using allowable AWS IAM syntax.
#  substituion token <RESOUCE> populated with  actual resource at runtime
ssm_readonly_template = '''
{
    "PolicyName": "SSM-ReadOnly-<UUID>",
    "PolicyDocument" : {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "ssm:GetParameter",
                "ssm:GetParameters"
            ],
            "Effect": "Allow",
            "Resource": [
                "<RESOURCE>"
            ]
        }
    ] }
}
'''

# Policy template for Read Only access to a single KMS Key
# TODO: Customize this policy as desired using allowable AWS IAM syntax.
#  substituion token <RESOUCE> populated with  actual resource at runtime
kms_readonly_template = '''
{
    "PolicyName": "KMS-ReadOnly-<UUID>",
    "PolicyDocument" : {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "kms:Decrypt",
            "Effect": "Allow",
            "Resource": "<RESOURCE>"
        }
    ] }
}
'''

# Policy template added to all roles built by  macro. This eliminates
#  need to specify permissions are always desired on each and every role.
#  policy below provides CloudWatchLogs, CodeDeploy, and SSM Session Manager access.
# TODO: Customize this policy as desired using allowable AWS IAM syntax.
all_roles_template = '''
{
    "PolicyName": "All-Roles-<UUID>",
    "PolicyDocument" : {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect" : "Allow",
            "Action" : "logs:*",
            "Resource" : "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
              "s3:Get*",
              "s3:List*"
            ],
            "Resource": [
              "arn:aws:s3:::aws-codedeploy-us-east-2/*",
              "arn:aws:s3:::aws-codedeploy-us-east-1/*",
              "arn:aws:s3:::aws-codedeploy-us-west-1/*",
              "arn:aws:s3:::aws-codedeploy-us-west-2/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
              "ssm:UpdateInstanceInformation",
              "ssmmessages:CreateControlChannel",
              "ssmmessages:CreateDataChannel",
              "ssmmessages:OpenControlChannel",
              "ssmmessages:OpenDataChannel"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
              "s3:GetEncryptionConfiguration"
            ],
            "Resource": "*"
        }
    ] }
}
'''

# TODO: Add policy snippets for or services (e.g. SNS, SQS, etc) and or
# action groups (e.g. ReadOnly, ReadWrite, FullAccess) using  samples above 
# as a reference

# Simple data structure to hold all  policy templates for easier lookup/reference
policytemplates = {}
# Add  S3 policy templates
s3policytemplates = {}
s3policytemplates['ReadOnly'] = s3_readonly_template
s3policytemplates['ReadWrite'] = s3_readwrite_template
policytemplates['s3'] = s3policytemplates
# Add  DynamoDB policy templates
ddbpolicytemplates = {}
ddbpolicytemplates['ReadOnly'] = ddb_readonly_template
ddbpolicytemplates['ReadWrite'] = ddb_readwrite_template
policytemplates['dynamodb'] = ddbpolicytemplates
# Add  SSM policy templates
ssmpolicytemplates = {}
ssmpolicytemplates['ReadOnly'] = ssm_readonly_template
policytemplates['ssm'] = ssmpolicytemplates
# Add  KMS policy templates
kmspolicytemplates = {}
kmspolicytemplates['ReadOnly'] = kms_readonly_template
policytemplates['kms'] = kmspolicytemplates
# Add  all roles policy templates
allrolestemplates = {}
allrolestemplates['default'] = all_roles_template
policytemplates['allroles'] = allrolestemplates
