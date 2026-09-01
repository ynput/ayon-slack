import pyblish.api

from ayon_core.lib.profiles_filtering import filter_profiles
from ayon_core.lib.attribute_definitions import TextDef
from ayon_core.lib.local_settings import get_ayon_user_entity
from ayon_core.pipeline import OptionalPyblishPluginMixin


class CollectSlackFamilies(pyblish.api.InstancePlugin,
                           OptionalPyblishPluginMixin):
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
    def get_attr_defs_for_instance(
        cls, create_context, instance
    ):
        # get attrs from OptionalPyblishPluginMixin
        attr_defs = super().get_attribute_defs()

        # Attributes logic
        publish_attributes = instance["publish_attributes"].get(
            cls.__name__, {})

        default_optional = getattr(cls, "optional", True)
        default_active = getattr(cls, "active", True)
        current_active =  publish_attributes.get("active", True)

        visiblity = default_active if not default_optional else current_active

        return  attr_defs + [
            TextDef(
                # Key under which it will be stored
                "additional_message",
                # Use plugin label as label for attribute
                label="Additional Slack message",
                placeholder="<Only if Slack is configured>",
                visible=visiblity,
            )
        ]

    @classmethod
    def register_create_context_callbacks(cls, create_context):
        create_context.add_value_changed_callback(cls.on_values_changed)

    @classmethod
    def on_values_changed(cls, event):
        """Update instance attribute definitions on attribute changes."""

        # Update attributes if any of the following plug-in attributes
        # change:
        keys = {"active"}

        for instance_change in event["changes"]:
            instance = instance_change["instance"]
            if not cls.instance_matches_plugin_families(instance):
                continue

            value_changes = instance_change["changes"]

            plugin_attribute_changes = (
                value_changes.get("publish_attributes", {})
                .get(cls.__name__, {}))

            if not any(key in plugin_attribute_changes for key in keys):
                continue

            # Update the attribute definitions
            new_attrs = cls.get_attr_defs_for_instance(
                event["create_context"], instance
            )
            instance.set_publish_plugin_attr_defs(cls.__name__, new_attrs)

    def process(self, instance):
        if not self.is_active(instance.data):
            return

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

        if any(p.get("send_to_current_user") for p in selected_profiles):
            attrib = get_ayon_user_entity().get("attrib", {})
            instance.data["slack_current_user"] = {
                "slackId": attrib.get("slackId"),
                "email": attrib.get("email"),
            }

        slack_token = (instance.context.data["project_settings"]
                                            ["slack"]
                                            ["token"])
        instance.data["slack_token"] = slack_token

        attribute_values = self.get_attr_values_from_data(instance.data)
        additional_message = attribute_values.get("additional_message")
        if additional_message:
            instance.data["slack_additional_message"] = additional_message
