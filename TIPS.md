# Group IAM By Resource

Lets say you want to manage the CloudFormation Deployment of Lambda Functions in your Organization.

We can ask CloudFormation to tell us the Permissions required For a Resource

```shell
PERMISSIONS=$(cloudformation-permissions resource AWS::Lambda::Function permissions --permission-level full --output iam)
echo $PERMISSIONS

```
We could spend our time manually grouping these together, but that seems like 
something a computer do best.

```shell
IAM=$(echo $PERMISSIONS | jq '.Action | group_by(split(":")[0]) | map({Effect: "Allow", Action: ., "Resource": "*"})') 
echo $IAM 
```
You're probably using CloudFormation YAML so let's run that through yq to format it 

```shell
echo $IAM | yq -p json -o y
```
Or do it all in one hit

```shell
cloudformation-permissions resource AWS::Lambda::Function permissions --permission-level full --output iam | jq '.Action | group_by(split(":")[0]) | map({Effect: "Allow", Action: ., "Resource": "*"})' | yq -p json -o yaml 
```
And this is your Output

```yaml
- Effect: Allow
  Action:
    - ec2:DescribeNetworkInterfaces
    - ec2:DescribeSecurityGroups
    - ec2:DescribeSubnets
    - ec2:DescribeVpcs
  Resource: '*'
- Effect: Allow
  Action:
    - elasticfilesystem:DescribeMountTargets
  Resource: '*'
- Effect: Allow
  Action:
    - iam:PassRole
  Resource: '*'
- Effect: Allow
  Action:
    - kms:CreateGrant
    - kms:Decrypt
    - kms:Encrypt
    - kms:GenerateDataKey
  Resource: '*'
- Effect: Allow
  Action:
    - lambda:CreateFunction
    - lambda:DeleteFunction
    - lambda:DeleteFunctionCodeSigningConfig
    - lambda:DeleteFunctionConcurrency
    - lambda:GetCodeSigningConfig
    - lambda:GetFunction
    - lambda:GetFunctionCodeSigningConfig
    - lambda:GetFunctionRecursionConfig
    - lambda:GetLayerVersion
    - lambda:GetRuntimeManagementConfig
    - lambda:ListFunctions
    - lambda:ListTags
    - lambda:PutFunctionCodeSigningConfig
    - lambda:PutFunctionConcurrency
    - lambda:PutFunctionRecursionConfig
    - lambda:PutRuntimeManagementConfig
    - lambda:TagResource
    - lambda:UntagResource
    - lambda:UpdateFunctionCode
    - lambda:UpdateFunctionConfiguration
  Resource: '*'
- Effect: Allow
  Action:
    - s3:GetObject
    - s3:GetObjectVersion
  Resource: '*'
```
