"""Helpers for querying device-specific Intune detected apps."""

from typing import Any
from urllib.parse import urlencode
from uuid import UUID


async def get_detected_apps_for_device(client: Any, device_id: str) -> list[dict[str, Any]]:
    """Return detected apps linked to a managed device through Graph's relationship."""
    normalized_device_id = str(UUID(device_id))
    query = urlencode(
        {
            "$expand": f"managedDevices($filter=id eq '{normalized_device_id}')",
            "$select": "id,displayName,version,sizeInByte,deviceCount,publisher,platform",
        }
    )
    apps = await client.get_all_pages(
        f"/deviceManagement/detectedApps?{query}",
        use_beta=False,
    )

    return [
        {key: value for key, value in app.items() if key != "managedDevices"}
        for app in apps
        if any(
            str(managed_device.get("id", "")).lower() == normalized_device_id
            for managed_device in app.get("managedDevices") or []
        )
    ]
