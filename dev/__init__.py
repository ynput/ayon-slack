from openpype.addons import BaseServerAddon

from .settings import SlackSettings


class SlackAddon(BaseServerAddon):
    name = "slack"
    version = "dev"
    settings_model = SlackSettings
