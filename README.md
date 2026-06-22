Slack Addon
===============

Deployment:
----------
Content of addon repo must be prepared for proper deployment to the server.
Currently it is a manual process consisting of steps: (requirements: at least Python3.8)
- clone repo to local machine
- run `python create_package.py` - this will produce `package` folder in root of cloned repo
- copy content of `package` folder to server machine to `openpype4-backend/addons` folder
  - example (current directory is root of cloned repo)
      - `cp -r package/slack SERVER_ROOT/openpype4-backend/addons`

Addon allowing sending notification to Slack channel(s) at the end of publishing.

It allows to upload thumbnail and review(for example mp4/mov) to the channel.
Uploading is limited by configurable file size to spare Slack disk limit.

Direct message to the publishing user:
-------------------------------------
Each message in a profile can also DM the AYON user who triggered the publish
(toggle `Send Slack DM to publishing AYON user`). The AYON user is reconciled to their
Slack account via a user attribute `slackId`; if it is empty the user's `email`
attribute is looked up against the Slack API instead.

Setup:
- Create a user-scoped string attribute named `slackId` in AYON
  (Settings > Attributes, scope = User) and set it per user to their Slack
  member id (e.g. `U0XXXXXXX`), or rely on the email fallback.
- The Slack bot token needs the `users:read.email` (email fallback) and
  `im:write` (DM delivery) scopes in addition to the existing ones.