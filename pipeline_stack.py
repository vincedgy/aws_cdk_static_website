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

        # Get the repository
        repo = codecommit.Repository.from_repository_name(self, id=id, repository_name='CdkStaticWebsiteRepo')

        # Pipeline code will go here
        pipeline = pipelines.CodePipeline(
            self,
            "CdkStaticWebsitePipeline",
            synth=pipelines.CodeBuildStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "main"),
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cd website",
                    "npm ci && npm run build --prod",
                    "cd ..",
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
