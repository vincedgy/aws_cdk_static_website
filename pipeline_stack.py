from aws_cdk import (
    aws_codecommit as codecommit,
    pipelines as pipelines,
    Stack, RemovalPolicy,
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
        repo.apply_removal_policy(RemovalPolicy.RETAIN);

        # Pipeline code will go here
        pipeline = pipelines.CodePipeline(
            self,
            "CdkStaticWebsitePipeline",
            synth=pipelines.CodeBuildStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    # Instructs Codebuild to install required packages
                    # "pip install --upgrade pip",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ]
            ),
        )

        deploy = StaticSitePipelineStage(self, id="CdkStaticWebsitePipeline-Deploy-Stage", props=props)
        deploy_stage = pipeline.add_stage(deploy)

        # deploy_stage.add_pre(
        #     pipelines.ShellStep("CdkStaticWebsitePipeline-prebuild",
        #                         commands=["cd ./website && npm ci && npm run build"]
        #                         ))
        #
        # deploy_stage.add_post(
        #     pipelines.ShellStep(
        #         "CdkStaticWebsitePipeline-TestViewerEndpoint",
        #         env={
        #             "ENDPOINT_URL": deploy.distribution_domain_name
        #         },
        #         commands=["curl -Ssf $ENDPOINT_URL"],
        #     )
        # )
