from aws_cdk import (
    aws_codecommit as codecommit,
    pipelines as pipelines,
    Stack,
)
from constructs import Construct

from pipeline_stage import StaticSitePipelineStage


class StaticSitePipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, props: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'CdkStaticWebsiteRepo'
        repo = codecommit.Repository(
            self, 'CdkStaticWebsiteRepo',
            repository_name="CdkStaticWebsiteRepo"
        )

        # Pipeline code will go here
        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                install_commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    # Instructs Codebuild to install required packages
                    # "pip install --upgrade pip",
                    "pip install -r requirements.txt",
                ],
                commands=[
                    "export STARTING_DIR=$(pwd)"
                    "cd ./website && npm ci && npm run build",
                    "cd $STARTING_DIR",
                    "cdk synth --ci --app cdk.out StaticSitePipelineStack --ci",
                ]
            ),
        )

        deploy = StaticSitePipelineStage(self, id="Deploy-StaticWebSite", props=props)
        deploy_stage = pipeline.add_stage(deploy)

        # deploy_stage.add_post(
        #     pipelines.ShellStep(
        #         "TestViewerEndpoint",
        #         env={
        #             "ENDPOINT_URL": deploy.distribution_domain_name
        #         },
        #         commands=["curl -Ssf $ENDPOINT_URL"],
        #     )
        # )
