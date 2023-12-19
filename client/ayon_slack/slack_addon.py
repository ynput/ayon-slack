import os
from openpype.modules import (
    AYONAddon,
    IPluginPaths,
    ILaunchHookPaths
)

SLACK_ADDON_DIR = os.path.dirname(os.path.abspath(__file__))


class SlackIntegrationAddon(AYONAddon, IPluginPaths, ILaunchHookPaths):
    """Allows sending notification to Slack channels during publishing."""

    name = "slack"

    def get_launch_hook_paths(self):
        """Implementation of `ILaunchHookPaths`."""
        return [
            os.path.join(SLACK_ADDON_DIR, "launch_hooks")
        ]

    def get_plugin_paths(self):
        """Implementation of abstract method for `IPluginPaths`."""

        return {
            "publish": self.get_publish_plugin_paths(),
        }

    def get_publish_plugin_paths(self, host_name=None):
        return [
            os.path.join(SLACK_ADDON_DIR, "plugins", "publish")
        ]