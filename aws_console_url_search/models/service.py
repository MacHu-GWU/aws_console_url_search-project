# -*- coding: utf-8 -*-

import typing as T
import enum
import dataclasses

from ..constants import AwsConsoleDomain
from .common import BaseModel, NOTHING


@dataclasses.dataclass
class Service(BaseModel):
    """
    - https://${optional_region}${sub_domain}.${domain}/${service_id}/home?#
    - https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Home:

    Subdomain:

    - console.aws
    - console (for aws-us-gov, or aws-c)

    Domain:

    - aws.amazon.com
    - amazonaws-us-gov.com
    - amazonaws-cn.com

    """

    region: str = dataclasses.field(default="")
    subdomain: str = dataclasses.field(default=AwsConsoleDomain.aws.subdomain)
    domain: str = dataclasses.field(default=AwsConsoleDomain.aws.domain)
    service_id: str = dataclasses.field(default=NOTHING)
    additional_params: T.List[str] = dataclasses.field(default_factory=list)

    @property
    def service_landing_page_url(self) -> str:
        domain_parts = []
        params = []
        if self.region:
            domain_parts.append(self.region)
            params.append(f"region={self.region}")
        domain_parts.append(self.subdomain)
        domain_parts.append(self.domain)
        params.extend(self.additional_params)
        final_domain = ".".join(domain_parts)
        final_params = "&".join(params)
        url = f"https://{final_domain}/{self.service_id}/home?{final_params}#"
        return url
