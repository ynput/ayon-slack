import os
from openpype.modules import (
    OpenPypeModule,
    IPluginPaths,
    ILaunchHookPaths
)

SLACK_ADDON_DIR = os.path.dirname(os.path.abspath(__file__))


class SlackIntegrationModule(OpenPypeModule, IPluginPaths, ILaunchHookPaths):
    """Allows sending notification to Slack channels during publishing."""

    name = "slack"

    def initialize(self, modules_settings):
        self.enabled = True

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
