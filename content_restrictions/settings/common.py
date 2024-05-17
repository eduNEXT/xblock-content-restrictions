"""
Common Django settings for the platform_plugin_turnitin project.
For more information on this file, see
https://docs.djangoproject.com/en/2.22/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.22/ref/settings/
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.CONTENT_RESTRICTIONS_MODULESTORE_BACKEND = "content_restrictions.edxapp_wrapper.backends.modulestore_q_v1"
