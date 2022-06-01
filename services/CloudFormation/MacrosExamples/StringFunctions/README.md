# String functions

Provides string transformation utility functions.

## Basic Usage

Place  transform where you would like  output to be placed and provide  input string as  value for 
InputString Parameter.  example below shows converting an input parameter to upper case and setting it as  value
for a tag on an s3 bucket.

```yaml
Parameters:
  InputString:
    Default: "This is a test input string"
    Type: String
Resources:
  S3Bucket:
    Type: "AWS::S3::Bucket"
    Properties:
      Tags:
        - Key: Upper
          Value:
            'Fn::Transform':
             - Name: 'String'
               Parameters:
                 InputString: !Ref InputString
                 Operation: Upper
```

## Available Operations

### Upper

Return a copy  string with all  cased characters converted to uppercase.

### Lower

Return a copy  string with all  cased characters [4] converted to lowercase.

### Capitalize

Return a copy  string with its first character capitalized and  rest lowercased.

### Title

Return a titlecased version  string where words start with an uppercase character and  remaining characters
are lowercase.

### SwapCase

Return a copy  string with uppercase characters converted to lowercase and vice versa.

### Strip

Return a copy  string with  leading and trailing characters removed.  `Chars` parameter is a string
specifying  set characters to be removed. If omitted default is to remove whitespace.  Chars argument is not a
prefix or suffix; rar, all combinations its values are stripped.

#### Additional Parameters

*Chars*: [optional] characters to strip from beginning and end string

### Replace

Return a copy  string with all occurrences substring `Old` replaced by `New`.

#### Additional Parameters

*Old*: [required] sub-string to search for

*New*: [required] string to replace Old with

### MaxLength

Return a copy  string with a maximum length as specified by  `Length` parameter. Default is to strip
characters from  end  string.

#### Additional Parameters

*Length*: [required] maximum length string

*StripFrom*: [optional] specifying `Left` will strip characters from  beginning  string, `Right` from  end
(default)

## Author

[Jay McConnell](https://github.com/jaymccon)  
Partner Solutions Architect  
Amazon Web Services
