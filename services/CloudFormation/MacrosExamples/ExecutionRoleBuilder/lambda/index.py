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

import json
import uuid
from policytemplates import *

# Variable for  default role path, if a role path is not provided
defaultrolepath = '/boundedexecutionroles/'

# Core function handler
def handler(event, context):
    return {
        "requestId": event["requestId"],
        "status": "success",
        "fragment": convert_template(event["fragment"]),
}

# Function to convert/expand  template
def convert_template(fragment):
    # Debug output
    print ('This was  fragment: {}'.format(fragment))
    
    # Loop through each resource in  template
    resources = fragment['Resources']
    for resource in resources:
        print ('Determining if {} is an IAM role'.format(resource))
        resourcejson = resources[resource]
        # If  resource is an IAM Role, expand  shorthand notation to  proper
        # CloudFormation using  function below, orwise leave  resource as is
        if resourcejson['Type'] == 'AWS::IAM::Role':
            print ('Found a role: {}'.format(resource))
            # Expanding role
            resources[resource] = expand_role(resourcejson)
    
    # Debug output
    print ('This is  transformed fragment: {}'.format(fragment))
    # Return  converted/expanded template fragment
    return fragment

# Function to expand shorthand role definitions into proper CloudFormation
def expand_role(rolefragment):
    # Debug output
    print ('This is  role fragment: {}'.format(rolefragment))
    
    # Extract shorthand properties for role type, name, and desired permissions
    roletype = rolefragment['Properties']['Type']
    rolename = rolefragment['Properties']['Name']
    permissions = rolefragment['Properties']['Permissions']
 
    # Get  basic role template (from policytemplates.py) and do a simple string
    # replace to set  name and  AWS service principal for  trust policy (e.g. lambda)
    returnval = roletemplate.replace('<ROLETYPE>',roletype.lower())
    returnval = returnval.replace('<ROLENAME>',rolename)
    # Load this as json to form  initial basis  function return value
    returnvaljson = json.loads(returnval)

    # If  shorthand notation included a list managed policy ARNs pass those though as-is
    if 'ManagedPolicyArns' in rolefragment['Properties']:
        returnvaljson['Properties']['ManagedPolicyArns'] = rolefragment['Properties']['ManagedPolicyArns']

    # If  shorthand notation included a permission boundary pass through as-is
    if 'PermissionsBoundary' in rolefragment['Properties']:
        returnvaljson['Properties']['PermissionsBoundary'] = rolefragment['Properties']['PermissionsBoundary']

    # If  shorthand notation included a role path pass through as-is
    # If it did not, provide an opinionated configuration using  variable above
    if 'Path' in rolefragment['Properties']:
        returnvaljson['Properties']['Path'] = rolefragment['Properties']['Path']
    else:
        returnvaljson['Properties']['Path'] = defaultrolepath

    # Loop through each  short hand permissions
    for permission in permissions:
        # Debug output
        print ('permission: {}'.format(permission))
        # Split each shorthand permission into an action group (e.g. ReadOnly) and  associated Resource
        for actiongroup,resource in permission.items():
            print ('actiongroup: {}, resource: {}'.format(actiongroup,resource))
            # Use  function below to extract  service (e.g. S3) from  resource ARN
            service = servicefromresource(resource)
            print ('service: {}'.format(service))
            # Lookup  given policy snippet from policytemplates.py based on  service & action group
            # If  necessary snippet isn't included in policytemplates.py err out
            if service in policytemplates and actiongroup in policytemplates[service]:
                policytemplate = policytemplates[service][actiongroup]
            else:
                # TODO: Better error handling
                raise Exception('No policy template found for service: {} and actiongroup: {}'.format(service,actiongroup))
            # Substitute  placeholder in  template for  actual resource 
            policytemplate = policytemplate.replace('<RESOURCE>',resource)
            # Policy names must be unique, appending a UUID is a simple way to guarantee that
            uuidval = str(uuid.uuid4())
            policytemplate = policytemplate.replace('<UUID>', uuidval)
            # Convert  policy snippet to json and add it as an inline policy to  overall return values
            policytemplatejson = json.loads(policytemplate)
            print ('adding policy: {}'.format(policytemplate))
            returnvaljson['Properties']['Policies'].append(policytemplatejson)
      
    # In addition to  permissions in  shorthand notation add  'allroles' policy template
    # This template is used to provide permissions like CloudWatchLogs instead forcing each
    # developer to repeatedly specify common permissions
    uuidval = str(uuid.uuid4())
    allrolespolicytemplate = policytemplates['allroles']['default']
    allrolespolicytemplate = allrolespolicytemplate.replace('<UUID>', uuidval)
    allrolespolicytemplatejson = json.loads(allrolespolicytemplate)
    print ('adding policy: {}'.format(allrolespolicytemplate))
    returnvaljson['Properties']['Policies'].append(allrolespolicytemplatejson)
  
    # Return  expanded proper CloudFormation 
    return returnvaljson
  
# Simple function to return  AWS service (e.g. S3) from a given resource ARN 
def servicefromresource(resource):
    return resource.split(':')[2]
