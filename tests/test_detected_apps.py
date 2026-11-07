import asyncio
from urllib.parse import parse_qs, urlsplit

import pytest

from intune_mcp_server.detected_apps import get_detected_apps_for_device


DEVICE_ID = "8f108974-d4b4-4528-895b-a970f6caec57"


class FakeGraphClient:
    def __init__(self, apps, managed_devices, throttle_once=False):
        self.apps = apps
        self.managed_devices = managed_devices
        self.list_endpoint = None
        self.list_use_beta = None
        self.batch_calls = []
        self.throttle_once = throttle_once

    async def get_all_pages(self, endpoint, use_beta=False):
        self.list_endpoint = endpoint
        self.list_use_beta = use_beta
        return self.apps

    async def post(self, endpoint, json, use_beta=False):
        self.batch_calls.append((endpoint, json, use_beta))
        responses = []
        for request in json["requests"]:
            app_id = request["url"].split("/detectedApps/")[1].split("/")[0]
            if self.throttle_once:
                self.throttle_once = False
                responses.append({
                    "id": request["id"],
                    "status": 429,
                    "headers": {"Retry-After": "0"},
                })
            else:
                responses.append({
                    "id": request["id"],
                    "status": 200,
                    "body": {"value": self.managed_devices.get(app_id, [])},
                })
        return {"responses": responses}


def test_get_detected_apps_filters_by_managed_device_relationship():
    client = FakeGraphClient(
        [
            {
                "id": "app-1",
                "displayName": "App on requested device",
                "deviceCount": 1,
            },
            {
                "id": "app-2",
                "displayName": "App on another device",
                "deviceCount": 1,
            },
            {"id": "app-3", "deviceCount": 0},
        ],
        {
            "app-1": [{"id": DEVICE_ID}],
            "app-2": [{"id": "00000000-0000-0000-0000-000000000001"}],
        },
    )

    apps = asyncio.run(get_detected_apps_for_device(client, DEVICE_ID))

    assert [app["id"] for app in apps] == ["app-1"]
    assert client.list_use_beta is False
    query = parse_qs(urlsplit(client.list_endpoint).query)
    assert query["$select"] == [
        "id,displayName,version,sizeInByte,deviceCount,publisher,platform"
    ]
    assert len(client.batch_calls) == 1
    endpoint, payload, use_beta = client.batch_calls[0]
    assert endpoint == "/$batch"
    assert use_beta is False
    assert len(payload["requests"]) == 2


def test_get_detected_apps_rejects_invalid_device_id():
    client = FakeGraphClient([], {})

    with pytest.raises(ValueError):
        asyncio.run(get_detected_apps_for_device(client, "not-a-device-id"))

    assert client.list_endpoint is None
    assert client.batch_calls == []


def test_get_detected_apps_retries_throttled_relationship(monkeypatch):
    async def no_wait(_):
        return None

    monkeypatch.setattr("intune_mcp_server.detected_apps.asyncio.sleep", no_wait)
    client = FakeGraphClient(
        [{"id": "app-1", "deviceCount": 1}],
        {"app-1": [{"id": DEVICE_ID}]},
        throttle_once=True,
    )

    apps = asyncio.run(get_detected_apps_for_device(client, DEVICE_ID))

    assert [app["id"] for app in apps] == ["app-1"]
    assert len(client.batch_calls) == 2
