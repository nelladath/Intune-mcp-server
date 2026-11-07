"""Helpers for querying device-specific Intune detected apps."""

import asyncio
from typing import Any
from urllib.parse import quote, urlencode
from uuid import UUID

_BATCH_SIZE = 20
_BATCH_RETRIES = 3


async def _get_managed_devices(
    client: Any,
    apps: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    pending = {str(index): app for index, app in enumerate(apps)}
    managed_devices: dict[str, list[dict[str, Any]]] = {}

    for attempt in range(_BATCH_RETRIES + 1):
        if not pending:
            break

        requests = [
            {
                "id": request_id,
                "method": "GET",
                "url": (
                    f"/deviceManagement/detectedApps/{quote(str(app['id']), safe='')}"
                    "/managedDevices?$select=id"
                ),
            }
            for request_id, app in pending.items()
        ]
        response = await client.post(
            "/$batch",
            json={"requests": requests},
            use_beta=False,
        )
        responses = {str(item["id"]): item for item in response.get("responses", [])}
        retry_pending: dict[str, dict[str, Any]] = {}
        retry_after = 0

        for request_id, app in pending.items():
            item = responses.get(request_id)
            if item is None:
                raise RuntimeError(f"Graph batch response omitted request {request_id}")

            status = item.get("status")
            if status == 200:
                managed_devices[str(app["id"])] = item.get("body", {}).get("value", [])
            elif status in (429, 503) and attempt < _BATCH_RETRIES:
                retry_pending[request_id] = app
                headers = item.get("headers", {})
                retry_after_header = next(
                    (value for key, value in headers.items() if key.lower() == "retry-after"),
                    None,
                )
                if retry_after_header:
                    retry_after = max(retry_after, int(retry_after_header))
            else:
                raise RuntimeError(
                    f"Graph API error ({status}) retrieving detected-app devices "
                    f"for app {app['id']}"
                )

        pending = retry_pending
        if pending:
            await asyncio.sleep(retry_after or min(2**attempt, 16))

    return managed_devices


async def get_detected_apps_for_device(client: Any, device_id: str) -> list[dict[str, Any]]:
    """Return detected apps linked to a managed device through Graph's relationship."""
    normalized_device_id = str(UUID(device_id)).lower()
    query = urlencode(
        {
            "$select": "id,displayName,version,sizeInByte,deviceCount,publisher,platform",
        }
    )
    apps = await client.get_all_pages(
        f"/deviceManagement/detectedApps?{query}",
        use_beta=False,
    )
    candidates = [
        app for app in apps
        if app.get("deviceCount") is None or app.get("deviceCount", 0) > 0
    ]

    managed_devices: dict[str, list[dict[str, Any]]] = {}
    for start in range(0, len(candidates), _BATCH_SIZE):
        batch_devices = await _get_managed_devices(
            client,
            candidates[start:start + _BATCH_SIZE],
        )
        managed_devices.update(batch_devices)

    return [
        app
        for app in candidates
        if any(
            str(managed_device.get("id", "")).lower() == normalized_device_id
            for managed_device in managed_devices.get(str(app["id"]), [])
        )
    ]
