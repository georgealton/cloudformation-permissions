# can-i-stack-it

Check if your CloudFormation Template can be deployed by a Role.

## Use Me

To generate findings, iam-sarif-report makes AWS API requests. The AWS Principal you use must be allowed to use the `access-analyzer:ValidatePolicy` command.

```json
{
    "Effect": "Allow",
    "Action":[
        "iam:SimulatePrincipalPolicy",
        "iam:GetContextKeysForPrincipalPolicy"
    ],
    "Resource": "*"
},
{
    "Effect": "Allow",
    "Action":[
        "cloudformation:ListStackResources",
        "cloudformation:GetTemplate"
    ],
    "Resource": "*"
}
```

### GitHub Action

See the [action.yaml](action.yaml) for detailed usage information.

```yaml
on: [push]
jobs:
  example:
    permissions:
      id-token: write
      actions: read
      contents: read
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # setup aws access
      - uses: aws-actions/configure-aws-credentials@v3
        with:
          role-to-assume: arn:aws:iam::111111111111:role/my-github-actions-role-test
          aws-region: eu-west-1

      # validate some policies and write a SARIF result file
      - uses: georgealton/can-i-stack-it@v2
```

### Locally

```sh
pipx run can-i-stack-it --template-source '' verify --role-arn ''
```

## Limitations

### Simulation of resource-based policies isn't supported for IAM roles.

This tool won't be able to tell you if there is Resource Policy 

