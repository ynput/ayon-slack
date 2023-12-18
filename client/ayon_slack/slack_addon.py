import os
from openpype.modules import (
    AYONAddon,
    IPluginPaths,
    ILaunchHookPaths
)

SLACK_ADDON_DIR = os.path.dirname(os.path.abspath(__file__))


class SlackIntegrationModule(AYONAddon, IPluginPaths, ILaunchHookPaths):
    """Allows sending notification to Slack channels during publishing."""

    name = "slack"

    def get_launch_hook_paths(self):
        """Implementation of `ILaunchHookPaths`."""
        return [
            os.path.join(SLACK_ADDON_DIR, "launch_hooks")
        ]

    def get_plugin_paths(self):
        """Deadline plugin paths."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return {
            "publish": [os.path.join(current_dir, "plugins", "publish")]
        }
