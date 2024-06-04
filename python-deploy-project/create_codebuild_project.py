import boto3

# Initialize a session using Amazon CodeBuild
codebuild = boto3.client('codebuild')
s3 = boto3.client('s3')

# Define the project details
project_name = 'python-deploy-project'
source_location = 'https://github.com/krish1511/CICD.git'
artifact_bucket = 'my-codebuild-artifacts-bucket-project'
service_role_arn = 'arn:aws:iam::590184094652:role/codebuild-service-role'
region = 'us-east-1'

# Create S3 bucket if it doesn't exist
try:
    s3.create_bucket(Bucket=artifact_bucket)
    print(f"S3 bucket {artifact_bucket} created successfully.")
except s3.exceptions.BucketAlreadyOwnedByYou:
    print(f"S3 bucket {artifact_bucket} already exists.")
except Exception as e:
    print(f"Error creating S3 bucket: {e}")

# Define environment variables from parameter store
environment_variables = [
    {
        'name': 'DOCKER_REGISTRY_USERNAME',
        'value': '/myapp/docker-credentials/username',
        'type': 'PARAMETER_STORE'
    },
    {
        'name': 'DOCKER_REGISTRY_PASSWORD',
        'value': '/myapp/docker-credentials/password',
        'type': 'PARAMETER_STORE'
    },
    {
        'name': 'DOCKER_REGISTRY_URL',
        'value': '/myapp/docker-registry/url',
        'type': 'PARAMETER_STORE'
    }
]

# Define the CodeBuild project configuration
project_config = {
    'name': project_name,
    'source': {
        'type': 'GITHUB',
        'location': source_location
    },
    'artifacts': {
        'type': 'S3',
        'location': artifact_bucket
    },
    'environment': {
        'type': 'LINUX_CONTAINER',
        'computeType': 'BUILD_GENERAL1_SMALL',
        'image': 'aws/codebuild/standard:5.0',
        'environmentVariables': environment_variables
    },
    'serviceRole': service_role_arn
}

# Create the CodeBuild project
response = codebuild.create_project(**project_config)

# Print the response
print(response)
