from aws_cdk import CfnOutput, Stack
from constructs import Construct

from static_site import StaticSitePublicS3, StaticSitePrivateS3


class StaticSiteStack(Stack):
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
        super().__init__(scope, id, **kwargs)

        self._distribution_domain_name = None
        self._distribution_id = None
        self._certificate = None
        self._bucket_name = None

        site_domain_name = props["domain_name"]
        if props["sub_domain_name"]:
            site_domain_name = (
                f'{props["sub_domain_name"]}.{props["domain_name"]}'
            )

        # If S3 website endpoint enabled, it creates the static site using a
        # public S3 as the origin. Otherwise, it creates a private S3 as the
        # origin.
        if props["enable_s3_website_endpoint"]:
            site = StaticSitePublicS3(
                self,
                f"{props['namespace']}-construct",
                site_domain_name=site_domain_name,
                domain_certificate_arn=props["domain_certificate_arn"],
                origin_referer_header_parameter_name=props[
                    "origin_custom_header_parameter_name"
                ],
                hosted_zone_id=props["hosted_zone_id"],
                hosted_zone_name=props["hosted_zone_name"],
            )
        else:
            site = StaticSitePrivateS3(
                self,
                f"{props['namespace']}-construct",
                site_domain_name=site_domain_name,
                domain_certificate_arn=props["domain_certificate_arn"],
                hosted_zone_id=props["hosted_zone_id"],
                hosted_zone_name=props["hosted_zone_name"],
            )

        self._bucket_name = site.bucket.bucket_name
        self._distribution_id = site.distribution.distribution_id
        self._distribution_domain_name = site.distribution.distribution_domain_name
        self._certificate = site.certificate.certificate_arn

        # Add stack outputs
        CfnOutput(
            self,
            "StaticSiteAddress",
            value=f"https://{site.bucket.bucket_name}"
        )

        CfnOutput(
            self,
            "DistributionId",
            value=site.distribution.distribution_id,
        )

        CfnOutput(
            self,
            "DistributionDomainName",
            value=f"https://{site.distribution.distribution_domain_name}",
        )

        CfnOutput(
            self,
            "CertificateArn",
            value=site.certificate.certificate_arn,
        )
