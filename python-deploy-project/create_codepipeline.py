import boto3

def create_codepipeline():
    # Initialize CodePipeline client
    codepipeline = boto3.client('codepipeline')

    # Define pipeline structure
    pipeline_name = 'python-codepipeline-project'
    role_arn = 'arn:aws:iam::590184094652:role/codepipeline-service-role'  # Update with your actual IAM role ARN
    artifact_bucket = 'my-codebuild-artifacts-bucket-project'  # Update with your actual S3 artifact bucket name
    source_action = {
        'name': 'Source',
        'actionTypeId': {
            'category': 'Source',
            'owner': 'AWS',
            'provider': 'CodeCommit',  # Use CodeCommit as the source provider
            'version': '1'
        },
        'configuration': {
            'RepositoryName': 'CICD',  # Update with your actual CodeCommit repository name
            'BranchName': 'main',  # Update with your actual branch name
            'PollForSourceChanges': 'false'
        },
        'outputArtifacts': [
            {
                'name': 'SourceOutput'
            }
        ],
        'runOrder': 1
    }
    build_action = {
        'name': 'Build',
        'actionTypeId': {
            'category': 'Build',
            'owner': 'AWS',
            'provider': 'CodeBuild',
            'version': '1'
        },
        'configuration': {
            'ProjectName': 'python-deploy-project'  # Update with your actual CodeBuild project name
        },
        'inputArtifacts': [
            {
                'name': 'SourceOutput'
            }
        ],
        'runOrder': 1
    }
    stages = [
        {
            'name': 'Source',
            'actions': [source_action]
        },
        {
            'name': 'Build',
            'actions': [build_action]
        }
    ]

    # Create CodePipeline
    response = codepipeline.create_pipeline(
        pipeline={
            'name': pipeline_name,
            'roleArn': role_arn,
            'artifactStore': {
                'type': 'S3',
                'location': artifact_bucket
            },
            'stages': stages
        }
    )

    print("CodePipeline created successfully:")
    print(response)

if __name__ == "__main__":
    create_codepipeline()
