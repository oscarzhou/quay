import os
import re
import subprocess

try:
    from util.config.provider import get_config_provider
except ModuleNotFoundError:
    # Stub out this call so that we can run the external_libraries script
    # without needing the entire codebase.
    def get_config_provider(*args, **kwargs):
        return None


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONF_DIR = os.getenv("QUAYCONF", os.path.join(ROOT_DIR, "conf/"))
STATIC_DIR = os.path.join(ROOT_DIR, "static/")
STATIC_LDN_DIR = os.path.join(STATIC_DIR, "ldn/")
STATIC_FONTS_DIR = os.path.join(STATIC_DIR, "fonts/")
STATIC_WEBFONTS_DIR = os.path.join(STATIC_DIR, "webfonts/")
TEMPLATE_DIR = os.path.join(ROOT_DIR, "templates/")

IS_TESTING = "TEST" in os.environ
IS_BUILDING = "BUILDING" in os.environ
IS_KUBERNETES = "KUBERNETES_SERVICE_HOST" in os.environ
OVERRIDE_CONFIG_DIRECTORY = os.path.join(CONF_DIR, "stack/")


config_provider = get_config_provider(
    OVERRIDE_CONFIG_DIRECTORY,
    "config.yaml",
    "config.py",
    testing=IS_TESTING,
    kubernetes=IS_KUBERNETES,
)


def _get_version_number():
    # Try to get version from environment
    version = os.getenv("QUAY_VERSION", "")

    if not version:
        # Fallback to getting version from changelog for standalone
        version = _get_version_number_changelog()

    return version


def _get_version_number_changelog():
    try:
        with open(os.path.join(ROOT_DIR, "CHANGELOG.md")) as f:
            for line in f:
                if line[0:5] == "## [v":
                    return line.split("[")[1].split("]")[0]
    except IOError:
        return ""


def _get_git_sha():
    if os.path.exists("GIT_HEAD"):
        with open(os.path.join(ROOT_DIR, "GIT_HEAD")) as f:
            return f.read()
    else:
        try:
            return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()[0:8]
        except (OSError, subprocess.CalledProcessError, Exception):
            pass
    return "unknown"


__version__ = _get_version_number()
__gitrev__ = _get_git_sha()
