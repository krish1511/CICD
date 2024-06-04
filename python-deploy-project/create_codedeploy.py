import boto3

# Initialize a session using AWS CodeDeploy
codedeploy = boto3.client('codedeploy')

# Define deployment details
application_name = 'CodeDeploy-application'
deployment_group = 'CodeDeploy-Group'
revision_location = {
    'revisionType': 'S3',
    's3Location': {
        'bucket': 'my-codebuild-artifacts-bucket-project',
        'key': 'myapp.zip',
        'bundleType': 'zip'
    }
}

# Start deployment
response = codedeploy.create_deployment(
    applicationName=application_name,
    deploymentGroupName=deployment_group,
    revision=revision_location,
    deploymentConfigName='CodeDeployDefault.OneAtATime'  # Example deployment config
)

# Print the deployment ID
print("Deployment initiated. Deployment ID:", response['deploymentId'])
