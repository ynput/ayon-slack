import pyblish.api

from ayon_core.lib.profiles_filtering import filter_profiles
from ayon_core.lib import attribute_definitions
from ayon_core.pipeline import AYONPyblishPluginMixin


class CollectSlackFamilies(pyblish.api.InstancePlugin,
                           AYONPyblishPluginMixin):
    """Collect family for Slack notification

        Expects configured profile in
        Project settings > Slack > Publish plugins > Notification to Slack

        Add Slack family to those instance that should be messaged to Slack
    """
    order = pyblish.api.CollectorOrder + 0.4999
    label = "Collect Slack family"
    settings_category = "slack"

    profiles = []

    @classmethod
    def get_attribute_defs(cls):
        return [
            attribute_definitions.TextDef(
                # Key under which it will be stored
                "additional_message",
                # Use plugin label as label for attribute
                label="Additional Slack message",
                placeholder="<Only if Slack is configured>"
            )
        ]

    def process(self, instance):
        task_data = instance.data["anatomyData"].get("task", {})
        product_type = instance.data["productType"]
        key_values = {
            "product_types": product_type,
            "task_names": task_data.get("name"),
            "task_types": task_data.get("type"),
            "hosts": instance.context.data["hostName"],
            "product_names": instance.data["productName"],

            # Backwards compatibility
            "families": product_type,
            "tasks": task_data.get("name"),
            "subsets": instance.data["productName"],
            "subset_names": instance.data["productName"],
        }
        # Filter 'key_values' for backwards compatibility
        if self.profiles:
            profile_keys = set(self.profiles[0].keys())
            key_values = {
                key: value
                for key, value in key_values.items()
                if key in profile_keys
            }
        profile = filter_profiles(self.profiles, key_values,
                                  logger=self.log)

        if not profile:
            self.log.info("No profile found, notification won't be send")
            return

        self.log.info("Found profile: {}".format(profile))
        instance.data.setdefault("families", []).append("slack")

        selected_profiles = profile["channel_messages"]
        for prof in selected_profiles:
            prof["review_upload_limit"] = profile.get("review_upload_limit",
                                                      50)
        instance.data["slack_channel_message_profiles"] = selected_profiles

        slack_token = (instance.context.data["project_settings"]
                                            ["slack"]
                                            ["token"])
        instance.data["slack_token"] = slack_token

        attribute_values = self.get_attr_values_from_data(instance.data)
        additional_message = attribute_values.get("additional_message")
        if additional_message:
            instance.data["slack_additional_message"] = additional_message
