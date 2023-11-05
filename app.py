#!/usr/bin/env python3

from aws_cdk import App

from pipeline_stack import StaticSitePipelineStack
from repository_stack import StaticSiteRepositoryStack

app = App()
props = {
    "namespace": app.node.try_get_context("namespace"),
    "domain_name": app.node.try_get_context("domain_name"),
    "sub_domain_name": app.node.try_get_context("sub_domain_name"),
    "domain_certificate_arn": app.node.try_get_context(
        "domain_certificate_arn"
    ),
    "enable_s3_website_endpoint": app.node.try_get_context(
        "enable_s3_website_endpoint"
    ),
    "origin_custom_header_parameter_name": app.node.try_get_context(
        "origin_custom_header_parameter_name"
    ),
    "hosted_zone_id": app.node.try_get_context("hosted_zone_id"),
    "hosted_zone_name": app.node.try_get_context("hosted_zone_name"),
}


try:
    StaticSiteRepositoryStack(app, f"{props['namespace']}-repository-stack")
except Exception as e:
    print(e)


StaticSitePipelineStack(app,
                        f"{props['namespace']}-pipeline-stack",
                        props
                        )

app.synth()
