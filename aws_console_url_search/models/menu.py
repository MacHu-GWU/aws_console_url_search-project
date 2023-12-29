# -*- coding: utf-8 -*-

import typing as T
import enum
import dataclasses

from ..constants import AwsConsoleDomain
from .common import BaseModel, NOTHING

if T.TYPE_CHECKING:
    from .service import Service


@dataclasses.dataclass
class Menu(BaseModel):
    """
    - https://${optional_region}${sub_domain}.${domain}/${service_id}/home?#
    - https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Home:

    Subdomain:

    - console.aws
    - console (for aws-us-gov, or aws-c)

    Examples:

    - Ec2 - Instances: https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances:search=:test;v=3;$case=tags:true%5C,client:false;$regex=tags:false%5C,client:false
    - Ec2 - Security Groups: https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#SecurityGroups:
    - S3 - Buckets: https://s3.console.aws.amazon.com/s3/buckets?region=us-east-1
    - S3 - Access Points: https://s3.console.aws.amazon.com/s3/ap?region=us-east-1
    - VPC - Vpcs: https://us-east-1.console.aws.amazon.com/vpc/home?region=us-east-1#vpcs:
    - VPC - Subnets: https://us-east-1.console.aws.amazon.com/vpc/home?region=us-east-1#subnets:
    """
    service: "Service" = dataclasses.field(default=NOTHING)


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
