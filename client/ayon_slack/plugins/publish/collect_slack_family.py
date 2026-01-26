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
        task_name = task_type = None
        task_entity = instance.data.get("taskEntity")
        if task_entity:
            task_name = task_entity["name"]
            task_type = task_entity["taskType"]
        product_type = instance.data["productType"]
        product_base_type = instance.data.get("productBaseType")
        if not product_base_type:
            product_base_type = product_type
        key_values = {
            "task_names": task_name,
            "task_types": task_type,
            "host_names": instance.context.data["hostName"],
            "product_base_types": product_base_type,
            "product_names": instance.data["productName"],
        }

        profile = filter_profiles(
            self.profiles, key_values, logger=self.log
        )
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
