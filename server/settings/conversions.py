from typing import Any


def _convert_product_base_types(overrides: dict[str, Any]):
    profiles = (
        overrides
        .get("publish", {})
        .get("CollectSlackFamilies", {})
        .get("profiles")
    )
    if not profiles:
        return

    for profile in profiles:
        if "hosts" in profile:
            profile["host_names"] = profile.pop("hosts")

        if "product_base_types" not in profile and "product_types" in profile:
            profile["product_base_types"] = profile.pop("product_types")


async def convert_settings_overrides(
    source_version: str,
    overrides: dict[str, Any],
) -> dict[str, Any]:
    _convert_product_base_types(overrides)
    return overrides
