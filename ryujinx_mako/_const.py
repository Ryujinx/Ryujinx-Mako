import os

try:
    # Available with Python 3.11
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class ConfigKey(StrEnum):
    DryRun = "MAKO_DRY_RUN"
    AppID = "MAKO_APP_ID"
    PrivateKey = "MAKO_PRIVATE_KEY"
    InstallationID = "MAKO_INSTALLATION_ID"


NAME = "Ryujinx-Mako"
SCRIPT_NAME = NAME.lower().replace("-", "_")

if ConfigKey.DryRun not in os.environ.keys() or len(os.environ[ConfigKey.DryRun]) == 0:
    IS_DRY_RUN = False
    # Check environment variables
    for key in ConfigKey:
        if key == ConfigKey.DryRun:
            continue
        if key not in os.environ.keys() or len(os.environ[key]) == 0:
            raise KeyError(f"Required environment variable not set: {key}")

    APP_ID = int(os.environ[ConfigKey.AppID])
    PRIVATE_KEY = os.environ[ConfigKey.PrivateKey]
    INSTALLATION_ID = int(os.environ[ConfigKey.InstallationID])
else:
    IS_DRY_RUN = True
    APP_ID = 0
    PRIVATE_KEY = ""
    INSTALLATION_ID = 0

GH_BOT_SUFFIX = "[bot]"
GH_EMAIL_TEMPLATE = "{user_id}+{username}@users.noreply.github.com"
