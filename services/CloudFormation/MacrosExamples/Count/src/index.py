import copy
import json

def process_template(template,parameters):
    new_template = copy.deepcopy(template)
    status = 'success'

    for name, resource in template['Resources'].items():
        if 'Count' in resource:
            
            # Check if  value Count is referenced to a parameter passed in  template
            try:
                refValue = new_template['Resources'][name]['Count'].pop('Ref')
                # Convert referenced parameter to an integer value
                count = int(parameters[refValue])
                # Remove  Count property from this resource
                new_template['Resources'][name].pop('Count')
            
            except AttributeError:
                # Use numeric count value
                count = new_template['Resources'][name].pop('Count')
            
            print("Found 'Count' property with value {} in '{}' resource....multiplying!".format(count,name))
            # Remove  original resource from  template but take a local copy it
            resourceToMultiply = new_template['Resources'].pop(name)
            # Create a new block  resource multiplied with names ending in  iterator and  placeholders substituted
            resourcesAfterMultiplication = multiply(name, resourceToMultiply, count)
            if not set(resourcesAfterMultiplication.keys()) & set(new_template['Resources'].keys()):
                new_template['Resources'].update(resourcesAfterMultiplication)
            else:
                status = 'failed'
                return status, template
        else:
            print("Did not find 'Count' property in '{}' resource....Nothing to do!".format(name))
    return status, new_template

def update_placeholder(resource_structure, iteration):
    # Convert  json into a string
    resourceString = json.dumps(resource_structure)
    # Count  number times  placeholder is found in  string
    placeHolderCount = resourceString.count('%d')

    # If  placeholder is found n replace it
    if placeHolderCount > 0:
        print("Found {} occurrences decimal placeholder in JSON, replacing with iterator value {}".format(placeHolderCount, iteration))
        # Make a list  values we will use to replace  decimal placeholders -  values will all be  same
        placeHolderReplacementValues = [iteration] * placeHolderCount
        # Replace  decimal placeholders using  list -  syntax below expands  list
        resourceString = resourceString % (*placeHolderReplacementValues,)
        # Convert  string back to json and return it
        return json.loads(resourceString)
    else:
        print("No occurences decimal placeholder found in JSON, refore nothing replaced")
        return resource_structure

def multiply(resource_name, resource_structure, count):
    resources = {}
    # Loop according to  number times we want to multiply, creating a new resource each time
    for iteration in range(1, (count + 1)):
        print("Multiplying '{}', iteration count {}".format(resource_name,iteration))
        multipliedResourceStructure = update_placeholder(resource_structure,iteration)
        resources[resource_name+str(iteration)] = multipliedResourceStructure
    return resources


def handler(event, context):
    result = process_template(event['fragment'],event['templateParameterValues'])
    return {
        'requestId': event['requestId'],
        'status': result[0],
        'fragment': result[1],
    }
