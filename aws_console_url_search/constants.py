# -*- coding: utf-8 -*-

import enum

CACHE_EXPIRE = 3600
MAX_SERVICE_RANK = 10000
MAX_MENU_RANK = 1000

REGION_LIST = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
    "us-gov-east-1",
    "us-gov-west-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "ca-central-1",
    "ca-west-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "af-south-1",
]


class _AwsConsoleDomain:
    domain = "amazon.com"
    subdomain = "console.aws"


class _AwsUsGovConsoleDomain:
    domain = "amazonaws-us-gov.com"
    subdomain = "console"


class _AwsCNConsoleDomain:
    domain = "amazonaws-cn.com"
    subdomain = "console"


class AwsConsoleDomain:
    """
    This is the full domain (subdomain + domain)

    Reference:

    - https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/signing-into-govcloud.html
    """

    aws = _AwsConsoleDomain
    aws_us_gov = _AwsUsGovConsoleDomain
    aws_cn = _AwsCNConsoleDomain
