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

import json

SPEC = json.load(open("spec.json"))

def resource(name):
    """
    Returns resource types match `name`, working right-to-left
    E.g. S3::Bucket will match AWS::S3::Bucket
    """

    return [
        key for key in SPEC["ResourceTypes"].keys()
        if key.endswith(name)
    ]
