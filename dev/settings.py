from pydantic import Field
from openpype.settings.common import BaseSettingsModel


class ChannelMessage(BaseSettingsModel):
    channels: list[str] = Field(default_factory=list, title="Channels")
    upload_thumbnail: bool = Field(default=True, title="Upload thumbnail")
    upload_review: bool = Field(default=True, title="Upload review")
    message: str = Field('', title="Message")


class Profile(BaseSettingsModel):

    families: list[str] = Field(default_factory=list, title="Families")
    hosts: list[str] = Field(default_factory=list, title="Hosts")
    task_types: str = Field(title="Task types",
                            enum=["Generic", "Art", "Modeling",
                                  "Texture", "Lookdev", "Rigging",
                                  "Edit", "Layout", "Setdress",
                                  "Animation", "FX", "Lighting",
                                  "Paint", "Compositing"])
    task_names: list[str] = Field(default_factory=list, title="Task names")
    subset_names: list[str] = Field(default_factory=list, title="Subset names")
    review_upload_limit: int = Field(50,
                                     title="Upload review maximum "
                                           "file size (MB)")

    desc = ("Message sent to channel selected by profile. "
           "Message template can contain {} placeholders from anatomyData "
           "or {review_filepath} for too large review files to link only.")
    channel_messages: list[ChannelMessage] = Field(
        default_factory=list,
        title="Messages to channels",
        description=desc,
        section="Messages",
        widget="textarea"
    )


class SlackSettings(BaseSettingsModel):
    """Slack system settings."""
    enabled: bool = Field(default=True)
    token: str = Field("", title="Auth Token")

    profiles: list[Profile] = Field(
        default_factory=list,
        title="Profiles",
        description="Profile and message of Slack notification",
        section="Profiles",
    )

