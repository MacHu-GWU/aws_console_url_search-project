import typing as T
import dataclasses

import jmespath

from ..constants import AwsConsoleDomain
from .common import BaseModel, NOTHING


@dataclasses.dataclass
class Request(BaseModel):
    client: str = dataclasses.field(default=NOTHING)
    method: str = dataclasses.field(default=NOTHING)
    kwargs: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)
    is_paginator: bool = dataclasses.field(default=NOTHING)
    result_path: str = dataclasses.field(default=NOTHING)


@dataclasses.dataclass
class Token:
    value: str = dataclasses.field()
    params: T.Dict[str, T.Any] = dataclasses.field(default_factory=dict)

    def evaluate(
        self,
        data: T.Dict[str, T.Any],
        aws_account_id: T.Optional[str] = None,
        aws_region: T.Optional[str] = None,
    ) -> str:
        params = dict()
        for k, v in self.params.items():
            if v.startswith("$"):
                expr = jmespath.compile(v[1:])
                params[k] = expr.search(data)
            else:
                params[k] = v
        params["AWS_ACCOUNT_ID"] = aws_account_id
        params["AWS_REGION"] = aws_region
        return self.value.format(**params)


@dataclasses.dataclass
class Response(BaseModel):
    id: T.Union[str, Token] = dataclasses.field(default=NOTHING)
    arn: T.Union[str, Token] = dataclasses.field(default="No arn")
    title: T.Union[str, Token] = dataclasses.field(default="No title")
    subtitle: T.Union[str, Token] = dataclasses.field(default="No subtitle")
    kvs: T.Dict[str, T.Union[str, Token]] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Resource(BaseModel):
    """ """

    client: str
    method: str
    max_result_key: T.Optional[str]
    max_result_value: T.Optional[int]
    page_size_key: T.Optional[str]
    page_size_value: T.Optional[int]
    is_paginator: T.Optional[bool]
    items_path: str
    id_field: str
    title: str
    subtitle: str

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
