# -*- coding: utf-8 -*-

from aws_console_url_search.models.service import Service

def print_url(srv: Service):
    print(f"{srv.service_id}: {srv.service_landing_page_url}")


class TestService:
    def test_get_service_landing_page_url(self):
        print_url(Service(service_id="ec2"))
        print_url(Service(service_id="s3"))
        print_url(Service(service_id="vpc"))
        print_url(Service(service_id="apigateway"))
        print_url(Service(service_id="sagemaker"))
        print_url(Service(service_id="cleanrooms"))


if __name__ == "__main__":
    from aws_console_url_search.tests import run_cov_test

    run_cov_test(__file__, "aws_console_url_search.models.service", preview=False)
