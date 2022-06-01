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

from datetime import datetime
import boto3
import cfnresponse
import json

client = boto3.client("cloudwatch")

def log(stack, metric, value):
    # Do it for  stack
    client.put_metric_data(
        Namespace="CloudFormation",
        MetricData=[
            {
                "MetricName": metric,
                "Unit": "Count",
                "Value": value,
                "Timestamp": datetime.now(),
                "Dimensions": [
                    {
                        "Name": "By Stack Name",
                        "Value": stack,
                    },
                ],
            },
        ],
    )

    client.put_metric_data(
        Namespace="CloudFormation",
        MetricData=[
            {
                "MetricName": metric,
                "Unit": "Count",
                "Value": value,
                "Timestamp": datetime.now(),
            },
        ],
    )

def handler(event, context):
    print("Received request:", json.dumps(event, indent=4))

    action = event["RequestType"]

    stack = event["ResourceProperties"]["StackName"]
    resources = int(event["ResourceProperties"]["ResourceCount"])

    try:
        log(stack, action, 1)

        if action == "Create":
            log(stack, "ResourceCount", resources)

        cfnresponse.send(event, context, cfnresponse.SUCCESS, {}, "{} metrics".format(stack))
    except Exception as e:
        cfnresponse.send(event, context, cfnresponse.FAILED, {
            "Data": str(e),
        }, "{} metrics".format(stack))
