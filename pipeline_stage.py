from aws_cdk import (
    Stage
)
from constructs import Construct

from site_stack import StaticSiteStack


class StaticSitePipelineStage(Stage):

    @property
    def distribution_domain_name(self):
        return self._distribution_domain_name

    @property
    def distribution_id(self):
        return self._distribution_id

    @property
    def certificate(self):
        return self._certificate

    @property
    def bucket_name(self):
        return self._bucket_name

    def __init__(self, scope: Construct, id: str, props: dict, **kwargs):

        _this = super().__init__(scope, id, **kwargs)

        service = StaticSiteStack(self,
                                  "StaticWebsite",
                                  props=props)

        self._distribution_domain_name = service.distribution_domain_name
        self._distribution_id = service.distribution_id
        self._certificate = service.certificate
        self._bucket_name = service.bucket_name
