import os
from openpype.modules import (
    OpenPypeModule,
    IPluginPaths,
    ILaunchHookPaths
)

SLACK_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


class SlackIntegrationModule(OpenPypeModule, IPluginPaths, ILaunchHookPaths):
    """Allows sending notification to Slack channels during publishing."""

    name = "slack"

    def initialize(self, modules_settings):
        try:
            slack_settings = modules_settings[self.name]
        except KeyError:
            # settings cannot be loaded, addon is disabled?
            self.enabled = False
            return
        self.enabled = slack_settings["enabled"]

    def get_launch_hook_paths(self):
        """Implementation of `ILaunchHookPaths`."""
        return os.path.join(SLACK_MODULE_DIR, "launch_hooks")

    def get_plugin_paths(self):
        """Deadline plugin paths."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return {
            "publish": [os.path.join(current_dir, "plugins", "publish")]
        }
