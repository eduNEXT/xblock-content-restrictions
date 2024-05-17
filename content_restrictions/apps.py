"""
Content Restrictions Django application initialization.
"""

from django.apps import AppConfig


class ContentRestrictionsConfig(AppConfig):
    """
    Configuration for the Content Restrictions Django application.
    """

    name = "content_restrictions"

    plugin_app = {
        "settings_config": {
            "lms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
            "cms.djangoapp": {
                "common": {"relative_path": "settings.common"},
                "test": {"relative_path": "settings.test"},
                "production": {"relative_path": "settings.production"},
            },
        },
    }
