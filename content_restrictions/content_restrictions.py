"""XBlock for content restrictions."""

import ipaddress
import logging

import pkg_resources
from crum import get_current_request
from django.utils import translation
from edx_django_utils import ip
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.exceptions import JsonHandlerError
from xblock.fields import Boolean, JSONField, List, Scope, String
from xblock.utils.resources import ResourceLoader
from xblock.utils.studio_editable import FutureFields, StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin
from xblock.validation import Validation

from content_restrictions.edxapp_wrapper.modulestore import modulestore

LOCAL_RESOURCE_LOADER = ResourceLoader(__name__)
log = logging.getLogger(__name__)


def _(text):
    """Make '_' a no-op so we can scrape strings."""
    return text


@XBlock.needs("i18n")
class XblockContentRestrictions(StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin, XBlock):
    """
    XBlock for content restrictions that can be applied to the child content.
    """

    CATEGORY = "content_restrictions"

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        default=_("Content With Access Restrictions"),
    )

    password_restriction = Boolean(
        display_name=_("Password Restriction"),
        help=_("When enabled, the content will be restricted by password."),
        scope=Scope.settings,
        default=False,
    )

    password_explanation_text = String(
        display_name=_("Password Explanatory Message"),
        help=_("This message will be shown when the learner is prompted to enter the password."),
        scope=Scope.settings,
        default=_("Please enter the password to access this content."),
    )

    incorrect_password_explanation_text = String(
        display_name=_("Incorrect Password Explanatory Message"),
        help=_("This message will be shown when the learner enters an incorrect password."),
        scope=Scope.settings,
        default=_("Incorrect password. Please try again."),
    )

    password = String(
        display_name=_("Password"),
        help=_(
            "Learners will need to type this password to access the content of the xblock. If the learner"
            " does not type the correct password, they will not have access to the content and will get an"
            " explanatory message instead. If the password is changed after the learner has already accessed"
            " the content, the learner will need to type the new password to access the content."
        ),
        scope=Scope.settings,
        default="",
    )

    user_provided_password = String(
        display_name=_("User Provided Password"),
        help=_(
            "The password that the user has provided. This is used to check if the user has entered the"
            " correct password."
        ),
        scope=Scope.user_state,
        default="",
    )

    ip_restriction = Boolean(
        display_name=_("IP Restriction"),
        help=_("When enabled, the content will be restricted by IP address."),
        scope=Scope.settings,
        default=False,
    )

    ip_whitelist = List(
        display_name=_("IP Whitelist"),
        help=_(
            "List of IP addresses or IP address ranges from which the content can be accessed."
            " The compatible protocols are IPv4 and IPv6. If the learner's IP address is not in the"
            " whitelist, they will not have access to the content. The range should be in the"
            ' CIDR format, e.g. (IPv4) "192.168.1.0/24", in this case only IP addresses from '
            ' "192.168.1.0" to "192.168.1.255" can access to the content, or (IPv6) "2001:db8:85a3::/48",'
            ' in this case only IP addresses from "2001:db8:85a3::" to "2001:db8:85a3:ffff:ffff:ffff:ffff:ffff"'
            ' can access to the content. Also, a single IP address can be provided, e.g. (IPv4) "172.16.0.0",'
            ' or (IPv6) "7ac:264a:dd69::". Alternatively, is possible mix IP addresses and IP ranges'
            ' with different formats, e.g. ["192.168.1.0/24", "172.16.0.0", "65c1:e700::/24", "5c87::"]'
        ),
        scope=Scope.settings,
        enforce_type=True,
        default=[],
    )

    ip_explanation_text = String(
        display_name=_("IP Restriction Explanatory Message"),
        help=_("This message will be shown when the learner is browsing from an IP address that is not whitelisted."),
        scope=Scope.settings,
        default=_(
            "You are entering from an IP address that is not whitelisted. Please follow"
            " the instructions provided in the course introduction video."
        ),
    )

    seb_restriction = Boolean(
        display_name=_("Safe Exam Browser Restriction"),
        help=_(
            "When enabled, the content will be restricted to be accessed only from Safe Exam Browser. "
            "To use this restriction, it is recommended to have the setting 'SEB_INDIVIDUAL_COURSE_ACTIVATION = True' "
            "in the platform. This setting allows activating the Safe Exam Browser restriction for individual "
            "courses. IMPORTANT: seb-openedx plugin must be installed in the Open edX platform."
        ),
        scope=Scope.settings,
        default=False,
    )

    seb_browser_keys = List(
        display_name=_("SEB Browser Keys"),
        help=_("List of keys that are allowed to be accessed from Safe Exam Browser."),
        scope=Scope.settings,
        enforce_type=True,
        default=[],
    )

    seb_config_keys = List(
        display_name=_("SEB Config Keys"),
        help=_("List of keys that are allowed to be accessed from Safe Exam Browser."),
        scope=Scope.settings,
        enforce_type=True,
        default=[],
    )

    seb_whitelist_paths = List(
        display_name=_("SEB Whitelist Paths"),
        help=_(
            "List of paths that are allowed to be accessed from Safe Exam Browser. To "
            "allow a restriction at the unit level it is necessary to maintain the "
            '"courseware" path in the list.'
        ),
        scope=Scope.settings,
        enforce_type=True,
        default=["courseware"],
    )

    editable_fields = [
        "display_name",
        "password_restriction",
        "password_explanation_text",
        "incorrect_password_explanation_text",
        "password",
        "ip_restriction",
        "ip_whitelist",
        "ip_explanation_text",
        "seb_restriction",
        "seb_browser_keys",
        "seb_config_keys",
        "seb_whitelist_paths",
    ]

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def get_seb_settings(self, other_course_settings: dict) -> dict:
        """
        Get the Safe Exam Browser settings.

        Args:
            other_course_settings (dict): The other course settings.

        Returns:
            dict: The Safe Exam Browser settings or an empty dictionary.
        """
        return other_course_settings.get("SAFE_EXAM_BROWSER", {})

    def set_seb_keys_and_paths(self) -> None:
        """
        Set the keys and whitelist_paths for Safe Exam Browser obtained from the other course settings.
        """
        course_module = modulestore().get_course(self.course_id)
        seb_settings = self.get_seb_settings(course_module.other_course_settings)

        self.seb_browser_keys = seb_settings.get("BROWSER_KEYS", [])
        self.seb_config_keys = seb_settings.get("CONFIG_KEYS", [])
        self.seb_whitelist_paths = seb_settings.get("WHITELIST_PATHS", [])

    def author_view(self, context):
        """
        Render the Studio preview by rendering each child so that they can all be seen and edited.
        """
        fragment = Fragment()
        root_xblock = context.get("root_xblock")
        is_root = root_xblock and root_xblock.location == self.location
        if is_root:
            # User has clicked the "View" link. Show a preview of all possible children:
            self.render_children(context, fragment, can_reorder=True, can_add=True)
        # else: When shown on a unit page, don't show any sort of preview -
        # just the status of this block in the validation area.

        return fragment

    def studio_view(self, context):
        """
        Render a form for editing this XBlock with translations.
        """
        self.set_seb_keys_and_paths()

        fragment = Fragment()
        context = {"fields": []}
        # Build a list of all the fields that can be edited:
        for field_name in self.editable_fields:
            field = self.fields[field_name]  # pylint: disable=unsubscriptable-object
            assert field.scope in (Scope.content, Scope.settings), (
                "Only Scope.content or Scope.settings fields can be used with "
                "StudioEditableXBlockMixin. Other scopes are for user-specific data and are "
                "not generally created/configured by content authors in Studio."
            )
            field_info = self._make_field_info(field_name, field)
            if field_info is not None:
                if field_info["type"] == "string":
                    field_info["default"] = self.ugettext(field_info["default"]) if field_info["default"] else ""
                    field_info["value"] = self.ugettext(field_info["value"]) if field_info["value"] else ""
                context["fields"].append(field_info)

        fragment.content = self.loader.render_django_template("templates/studio_edit.html", context)
        fragment.add_javascript(self.loader.load_unicode("public/studio_edit.js"))
        fragment.initialize_js("StudioEditableXBlockMixin")
        return fragment

    def student_view(self, context):
        """
        View for students to see the blocks in the unit.
        """
        children_contents = []
        fragment = Fragment()

        if not self.has_access_to_content:
            return self.render_restricted_student_view()

        for child_id in self.children:
            child = self.runtime.get_block(child_id)
            child_fragment = self._render_child_fragment(child, context, "student_view")
            fragment.add_fragment_resources(child_fragment)
            children_contents.append(child_fragment.content)

        render_context = {
            "block": self,
            "children_contents": children_contents,
        }
        render_context.update(context)
        fragment.add_content(
            LOCAL_RESOURCE_LOADER.render_django_template(
                "static/html/children.html", render_context, i18n_service=self.runtime.service(self, "i18n")
            )
        )
        return fragment

    @property
    def has_access_to_content(self):
        """
        Check if the user has access to the content.

        - If password restriction is enabled, check if the user has entered the correct password.
        - If IP restriction is enabled, check if the user has access with the IP whitelist.
        """
        if self.password_restriction and not self.is_correct_password:
            return False
        if self.ip_restriction:
            return self.has_access_with_ip_whitelist(get_current_request())
        return True

    @property
    def is_correct_password(self) -> bool:
        """
        Check if the user has entered the correct password.

        Returns:
            bool: True if the user has entered the correct password, False otherwise.
        """
        return self.user_provided_password == self.password

    def has_access_with_ip_whitelist(self, request) -> bool:
        """
        Check if the user has access to the content based on the IP whitelist.

        Args:
            request (WSGIRequest): The current request object.

        Returns:
            bool: True if the user has access to the content, False otherwise.
        """
        if self.ip_whitelist is None:
            self.ip_whitelist = []

        client_ips = ip.get_all_client_ips(request)
        for ip_add_or_range in self.ip_whitelist:
            if any(self.ip_has_access(client_ip, ip_add_or_range) for client_ip in client_ips):
                return True
        return False

    @staticmethod
    def ip_has_access(client_ip: str, ip_address_or_range: str) -> bool:
        """
        Check if the client IP matches the IP address or is in the IP range.

        The IP address or range can be in IPv4 or IPv6 format.

        Args:
            client_ip (str): The IP address to check.
            ip_address_or_range (str): The IP address or IP range to check against.

        Returns:
            bool: True if the IP is in the network, False otherwise.
        """
        client_ip = ipaddress.ip_address(client_ip)

        try:
            ip_address = ipaddress.ip_address(ip_address_or_range)
            return client_ip == ip_address
        except ValueError:
            try:
                ip_network = ipaddress.ip_network(ip_address_or_range, strict=False)
                return client_ip in ip_network
            except ValueError:
                log.exception(f"Invalid IP address or range: {ip_address_or_range}")
                return False

    def render_restricted_student_view(self):
        """
        Render the restricted student view, based on the restriction type.

        Returns:
            Fragment: The rendered fragment.
        """
        fragment = Fragment()
        fragment.add_content(
            LOCAL_RESOURCE_LOADER.render_django_template(
                f"static/html/{self.restriction_template}",
                {
                    "block": self,
                },
                i18n_service=self.runtime.service(self, "i18n"),
            )
        )
        fragment.add_css(self.resource_string("static/css/content_restrictions.css"))

        # Add i18n js
        if statici18n_js_url := self._get_statici18n_js_url():
            fragment.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        fragment.add_javascript(self.resource_string("static/js/src/content_restrictions.js"))
        fragment.initialize_js("XblockContentRestrictions")
        return fragment

    @property
    def restriction_template(self):
        """
        Get the current restriction template.

        Returns:
            str: The current restriction template.
        """
        if self.password_restriction and not self.is_correct_password:
            return "password_restriction.html"
        if self.ip_restriction:
            return "ip_restriction.html"
        return "no_access.html"

    @XBlock.json_handler
    def has_access_with_password(self, data, suffix=""):  # pylint: disable=unused-argument
        """
        Check if the user has the correct password.

        Args:
            data: The data sent by the client.
        Returns:
            dict: The result of the check.
        """
        self.user_provided_password = data.get("password")
        if self.is_correct_password:
            return {
                "success": True,
            }
        incorrect_password_explanation_text = self.incorrect_password_explanation_text
        if not incorrect_password_explanation_text:
            incorrect_password_explanation_text = _("Incorrect password. Please try again.")

        return {
            "success": False,
            "error_message": incorrect_password_explanation_text,
        }

    def set_seb_settings(self) -> None:
        """
        Set the Safe Exam Browser settings.

        First, get the other course settings and the Safe Exam Browser settings.
        If the Safe Exam Browser restriction is enabled, add all the necessary settings to the
        Safe Exam Browser settings. If disabled, remove the current vertical from the blacklist.
        Finally, update the course module with the new settings.
        """
        course_module = modulestore().get_course(self.course_id)
        other_course_settings = course_module.other_course_settings
        seb_settings = self.get_seb_settings(other_course_settings)
        parent_id = self.parent.block_id

        if self.seb_restriction:
            seb_settings["ENABLED"] = True
            seb_settings["ALLOW_MFE_ACCESS"] = True
            seb_settings["BROWSER_KEYS"] = list(set(seb_settings.get("BROWSER_KEYS", []) + self.seb_browser_keys))
            seb_settings["CONFIG_KEYS"] = list(set(seb_settings.get("CONFIG_KEYS", []) + self.seb_config_keys))
            seb_settings["WHITELIST_PATHS"] = list(
                set(seb_settings.get("WHITELIST_PATHS", []) + self.seb_whitelist_paths)
            )
            seb_settings["BLACKLIST_VERTICALS"] = list(set(seb_settings.get("BLACKLIST_VERTICALS", []) + [parent_id]))
        elif seb_settings and parent_id in seb_settings["BLACKLIST_VERTICALS"]:
            seb_settings["BLACKLIST_VERTICALS"].remove(parent_id)

        other_course_settings["SAFE_EXAM_BROWSER"] = seb_settings
        course_module.other_course_settings = other_course_settings
        modulestore().update_item(course_module, self.scope_ids.user_id)

    @XBlock.json_handler
    def submit_studio_edits(self, data, suffix=""):
        """
        AJAX handler for studio_view() Save button.
        """
        values = {}  # dict of new field values we are updating
        to_reset = []  # list of field names to delete from this XBlock
        for field_name in self.editable_fields:
            field = self.fields[field_name]  # pylint: disable=unsubscriptable-object
            if field_name in data["values"]:
                if isinstance(field, JSONField):
                    values[field_name] = field.from_json(data["values"][field_name])
                else:
                    raise JsonHandlerError(400, f"Unsupported field type: {field_name}")
            elif field_name in data["defaults"] and field.is_set_on(self):
                to_reset.append(field_name)
        self.clean_studio_edits(values)
        validation = Validation(self.scope_ids.usage_id)
        # We cannot set the fields on self yet, because even if validation fails, studio is going to save any changes we
        # make. So we create a "fake" object that has all the field values we are about to set.
        preview_data = FutureFields(new_fields_dict=values, newly_removed_fields=to_reset, fallback_obj=self)
        self.validate_field_data(validation, preview_data)
        if validation:
            for field_name, value in values.items():
                setattr(self, field_name, value)
            for field_name in to_reset:
                self.fields[field_name].delete_from(self)  # pylint: disable=unsubscriptable-object
            self.set_seb_settings()
            return {"result": "success"}
        else:
            raise JsonHandlerError(400, validation.to_json())

    @staticmethod
    def workbench_scenarios():  # pragma: no cover
        """Create canned scenario for display in the workbench."""
        return [
            (
                "XblockContentRestrictions",
                """<content_restrictions/>
             """,
            ),
            (
                "Multiple XblockContentRestrictions",
                """<vertical_demo>
                <content_restrictions/>
                <content_restrictions/>
                <content_restrictions/>
                </vertical_demo>
             """,
            ),
        ]

    @staticmethod
    def _get_statici18n_js_url():  # pragma: no cover
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = "public/js/translations/{locale_code}/text.js"
        lang_code = locale_code.split("-")[0]
        for code in (locale_code, lang_code, "en"):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop("Dummy")
