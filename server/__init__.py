from __future__ import annotations

from typing import Any

from ayon_server.addons import BaseServerAddon

from .settings import (
    SlackSettings,
    DEFAULT_SLACK_SETTING,
    convert_settings_overrides,
)


class Slack(BaseServerAddon):

    settings_model = SlackSettings

    async def get_default_settings(self):
        settings_model_cls = self.get_settings_model()
        return settings_model_cls(**DEFAULT_SLACK_SETTING)

    async def convert_settings_overrides(
        self,
        source_version: str,
        overrides: dict[str, Any],
    ) -> dict[str, Any]:
        await convert_settings_overrides(source_version, overrides)
        return await super().convert_settings_overrides(
            source_version, overrides
        )
