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

import os

PREFIX = "Boto3::"

LAMBDA_ARN = os.environ["LAMBDA_ARN"]

def handle_template(request_id, template):
    for name, resource in template.get("Resources", {}).items():
        if resource["Type"].startswith(PREFIX):
            resource.update({
                "Type": "Custom::Boto3",
                "Version": "1.0",
                "Properties": {
                    "ServiceToken": LAMBDA_ARN,
                    "Mode": resource.get("Mode", ["Create", "Update"]),
                    "Action": resource["Type"][len(PREFIX):],
                    "Properties": resource.get("Properties", {}),
                },
            })

            if "Mode" in resource:
                del resource["Mode"]

    return template

def handler(event, context):
    fragment = event["fragment"]
    status = "success"

    try:
        fragment = handle_template(event["requestId"], event["fragment"])
    except Exception as e:
        status = "failure"

    return {
        "requestId": event["requestId"],
        "status": status,
        "fragment": fragment,
    }
