from __future__ import annotations

from ayon_server.addons import BaseServerAddon

from .settings.main import SlackSettings, DEFAULT_SLACK_SETTING
from .version import __version__


class Slack(BaseServerAddon):
    name = "slack"
    version = __version__

    settings_model = SlackSettings

    async def get_default_settings(self):
        settings_model_cls = self.get_settings_model()
        return settings_model_cls(**DEFAULT_SLACK_SETTING)
