# -*- coding: utf-8 -*-

import enum

CACHE_EXPIRE = 3600


class _AwsConsoleDomain:
    domain = "amazon.com"
    subdomain = "console.aws"


class _AwsUsGovConsoleDomain:
    domain = "amazonaws-us-gov.com"
    subdomain = "console"


class _AwsCNConsoleDomain:
    domain = "amazonaws-cm.com"
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
