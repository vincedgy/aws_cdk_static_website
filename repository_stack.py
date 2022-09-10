from aws_cdk import (
    aws_codecommit as codecommit,
    pipelines as pipelines,
    Stack, RemovalPolicy,
)
from constructs import Construct

from pipeline_stage import StaticSitePipelineStage


class StaticSiteRepositoryStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'CdkStaticWebsiteRepo'
        repo = codecommit.Repository(
            self, 'CdkStaticWebsiteRepo',
            repository_name="CdkStaticWebsiteRepo"
        )
        repo.apply_removal_policy(RemovalPolicy.RETAIN);