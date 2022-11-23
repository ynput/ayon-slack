from openpype.addons import BaseServerAddon

from .settings import SlackSettings
from .version import __version__


class SlackAddon(BaseServerAddon):
    name = "slack"
    version = __version__

    settings_model = SlackSettings
