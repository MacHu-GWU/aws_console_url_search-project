# -*- coding: utf-8 -*-

import json

from ..paths import (
    path_console_urls_json,
    path_data_json,
)


def load_console_url_data() -> dict:
    return json.loads(path_console_urls_json.read_text())


def dump_console_url_data(console_url_data: dict):
    content = json.dumps(console_url_data, indent=4)
    path_console_urls_json.write_text(content)
    path_data_json.write_text(content)


def get_sort_key(id: str, weight: int):
    return f"{str(9999 - weight).zfill(4)}-{id}"


def sort_console_url_data(console_url_data: dict) -> dict:
    service_list = list()

    for service_id, service in console_url_data.items():
        service_sort_key = get_sort_key(id=service_id, weight=service.get("weight", 1))
        sub_service_list = list()
        for sub_service_id, sub_service in service.get("sub_services", {}).items():
            sub_service_sort_key = get_sort_key(
                id=sub_service_id, weight=sub_service.get("weight", 1)
            )
            sub_service_list.append((sub_service_sort_key, sub_service_id, sub_service))

        service["sub_services"] = {
            sub_service_id: sub_service
            for _, sub_service_id, sub_service in sorted(
                sub_service_list,
                key=lambda x: x[0],
            )
        }

        service_list.append((service_sort_key, service_id, service))

    console_url_data = {
        service_id: service
        for _, service_id, service in sorted(
            service_list,
            key=lambda x: x[0],
        )
    }
    return console_url_data
