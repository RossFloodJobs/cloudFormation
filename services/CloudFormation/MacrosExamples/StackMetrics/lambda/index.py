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

def handler(event, context):
    template = event["fragment"]

    template["Resources"]["StackMetrics"] = {
        "Type": "Custom::StackMetrics",
        "Properties": {
            "ServiceToken": {
                "Fn::ImportValue": "StackMetricsMacroFunction",
            },
            "StackName": {
                "Ref": "AWS::StackName",
            },
            "ResourceCount": len(template["Resources"].keys()),
        },
    }

    return {
        "requestId": event["requestId"],
        "status": "success",
        "fragment": template,
    }
