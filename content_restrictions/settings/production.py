"""
Production Django settings for platform_plugin_turnitin project.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.CONTENT_RESTRICTIONS_MODULESTORE_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "CONTENT_RESTRICTIONS_MODULESTORE_BACKEND", settings.CONTENT_RESTRICTIONS_MODULESTORE_BACKEND
    )
