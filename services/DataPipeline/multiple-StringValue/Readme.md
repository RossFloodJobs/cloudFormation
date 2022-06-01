## DataPipeline with multiple StringValue's
 CloudFormation documentation shows how to provide a StringValue for atomic values as part your DataPipeline definition. 
 documentation also lacks a little in providing an example how to cross reference RefValue as part one pipeline object
with properties anor. 

### Usage
This template is for use as-is and does not require any Parameters or user input whatsoever. You can deploy this in any region
supports DataPipeline and CloudFormation.  Pipeline itself does not serve any particular purpose, rar, this exemplifies  translation DataPipeline definitions using Cloudformation. 

You can see when we look at  following: 

```
              {
                "Key": "applications",
                "StringValue": "spark"
              },
              {
                "Key": "applications",
                "StringValue": "hive"
              },
              {
                "Key": "applications",
                "StringValue": "pig"
              },
```

We can pass multiple 'StringValue'  same 'Key' multiple times

And here we have an example providing parameters for RefValues given in a different part  PipelineObjects: 

``` 
         {
            "Id": "coresite",
            "Name": "coresite",
            "Fields": [
              {
                "Key": "type",
                "StringValue": "EmrConfiguration"
              },
              {
                "Key": "classification",
                "StringValue": "core-site"
              },
              {
                "Key": "property",
                "RefValue": "io-file-buffer-size"
              },
              {
                "Key": "property",
                "RefValue": "fs-s3-block-size"
              }
            ]
          },
          {
            "Id": "io-file-buffer-size",
            "Name": "io-file-buffer-size",
            "Fields": [
              {
                "Key": "type",
                "StringValue": "Property"
              },
              {
                "Key" : "value",
                "StringValue": "4096"
              },
              {
                "Key" : "key",
                "StringValue": "io.file.buffer.size"
              }

            ]
          },
```

### Basis
 template was originally requested as a 1:2:1 copy  DataPipeline definition found in  Documentation here: 
http://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-object-emrconfiguration.html
