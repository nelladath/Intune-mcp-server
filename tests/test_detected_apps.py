import asyncio
from urllib.parse import parse_qs, urlsplit

import pytest

from intune_mcp_server.detected_apps import get_detected_apps_for_device


DEVICE_ID = "8f108974-d4b4-4528-895b-a970f6caec57"


class FakeGraphClient:
    def __init__(self, apps):
        self.apps = apps
        self.endpoint = None
        self.use_beta = None

    async def get_all_pages(self, endpoint, use_beta=False):
        self.endpoint = endpoint
        self.use_beta = use_beta
        return self.apps


def test_get_detected_apps_filters_by_managed_device_relationship():
    client = FakeGraphClient(
        [
            {
                "id": "app-1",
                "displayName": "App on requested device",
                "managedDevices": [{"id": DEVICE_ID}],
            },
            {
                "id": "app-2",
                "displayName": "App on another device",
                "managedDevices": [{"id": "00000000-0000-0000-0000-000000000001"}],
            },
        ]
    )

    apps = asyncio.run(get_detected_apps_for_device(client, DEVICE_ID))

    assert [app["id"] for app in apps] == ["app-1"]
    assert "managedDevices" not in apps[0]
    assert client.use_beta is False
    query = parse_qs(urlsplit(client.endpoint).query)
    assert query["$expand"] == [f"managedDevices($filter=id eq '{DEVICE_ID}')"]


def test_get_detected_apps_rejects_invalid_device_id():
    client = FakeGraphClient([])

    with pytest.raises(ValueError):
        asyncio.run(get_detected_apps_for_device(client, "not-a-device-id"))

    assert client.endpoint is None
