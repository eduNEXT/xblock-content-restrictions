"""TO-DO: Write a description of what this XBlock is."""
import logging
from enum import Enum
import pkg_resources
from django.utils import translation
from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment
from collections import namedtuple
from xblockutils.resources import ResourceLoader
from xblock.utils.studio_editable import StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin
from xblock.utils.resources import ResourceLoader
from edx_django_utils import ip
from crum import get_current_request
from seb_openedx.permissions import get_enabled_permission_classes


# Make '_' a no-op so we can scrape strings
_ = lambda text: text
loader = ResourceLoader(__name__)
LOG = logging.getLogger(__name__)


class ContentRestrictions(Enum):
    """
    Enum for content restrictions.
    """
    NO_RESTRICTION = 'NO_RESTRICTION'
    IP_WHITELIST = 'IP_WHITELIST'
    PASSWORD = 'PASSWORD'
    SEB_BROWSER = 'SEB_BROWSER'

class XblockContentRestrictions(StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin, XBlock):
    """
    TO-DO: document what your XBlock does.
    """

    CATEGORY = "content_restrictions"

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        default=_("Content Restrictions")
    )

    restriction_type = String(
        display_name=_("Restriction Type"),
        scope=Scope.settings,
        default="NO_RESTRICTION",
        values=[
            {
                "display_name": "No Restriction",
                "value": "NO_RESTRICTION",
            },
            {
                "display_name": "IP Whitelist",
                "value": "IP_WHITELIST",
            },
            {
                "display_name": "Password",
                "value": "PASSWORD",
            },
            {
                "display_name": "SEB Browser",
                "value": "SEB_BROWSER",
            },
        ],
        help="Type of restriction to apply to learners.",
    )

    ip_whitelist = String(
        display_name=_("IP Whitelist"),
        scope=Scope.settings,
        help=_("List of IP addresses that can access the content. Use commas to separate multiple IP addresses."),
    )

    password = String(
        display_name=_("Password"),
        scope=Scope.settings,
        help=_("Password required to access the content."),
    )

    user_provided_password = String(
        display_name=_("Password"),
        scope=Scope.user_state,
        help=_("Password provided by the user to access the content."),
    )

    editable_fields = [
        "display_name",
        "restriction_type",
        "ip_whitelist",
        "password",
    ]

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def render_restricted_student_view(self, context):
        """
        Render the restricted student view.
        """
        templates = {
            ContentRestrictions.IP_WHITELIST.name: 'restricted_ip_whitelist.html',
            ContentRestrictions.PASSWORD.name: 'restricted_password.html',
            ContentRestrictions.SEB_BROWSER.name: 'restricted_seb_browser.html',
        }
        html = self.resource_string(f"static/html/{templates[self.restriction_type]}")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/content_restrictions.css"))

        # Add i18n js
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            frag.add_javascript_url(self.runtime.local_resource_url(self, statici18n_js_url))

        frag.add_javascript(self.resource_string("static/js/src/content_restrictions.js"))
        frag.initialize_js('XblockContentRestrictions')
        return frag

    def student_view(self, context):
        """
        View for previewing contents in studio.
        """
        if not self.has_access_to_content:
            return self.render_restricted_student_view(context)

        children_contents = []
        fragment = Fragment()

        for child_id in self.children:
            child = self.runtime.get_block(child_id)
            child_fragment = self._render_child_fragment(child, context, 'student_view')
            fragment.add_fragment_resources(child_fragment)
            children_contents.append(child_fragment.content)

        render_context = {
            'block': self,
            'children_contents': children_contents,
        }
        render_context.update(context)
        fragment.add_content(self.loader.render_django_template(self.CHILD_PREVIEW_TEMPLATE, render_context))
        return fragment

    @property
    def has_access_to_content(self):
        """
        Check if the user has access to the content.
        """
        if self.restriction_type == ContentRestrictions.NO_RESTRICTION.name:
            return True
        if self.restriction_type == ContentRestrictions.PASSWORD.name:
            return bool(self.user_provided_password == self.password)
        if self.restriction_type == ContentRestrictions.IP_WHITELIST.name:
            return self.has_access_with_ip_whitelist(get_current_request())
        elif self.restriction_type == ContentRestrictions.SEB_BROWSER.name:
            return self.has_access_with_seb_browser(
                get_current_request(),
                self.runtime.user_id,
                self.course_id,
            )
        return True

    def has_access_with_ip_whitelist(self, request):
        """
        Check if the user is in the IP whitelist.
        """
        client_ips = ip.get_all_client_ips(request)
        whitelist = self.ip_whitelist.split(',')
        return any(ip in whitelist for ip in client_ips)

    def has_access_with_seb_browser(self, request, username, course_key):
        """
        Check if the user has access to the content based on the browser used.

        Returns:
            bool: True if the user has access, False otherwise.
        """
        access_granted = False

        for permission in get_enabled_permission_classes(course_key):
            if permission().check(request, course_key):
                access_granted = True
            else:
                LOG.info("Permission: %s denied for: %s.", permission, username)

        return access_granted

    @XBlock.json_handler
    def has_access_with_password(self, data, suffix=''):
        """
        Check if the user has the correct password.
        """
        self.user_provided_password = data.get('password')
        if data.get('password') == self.password:
            return {'success': True}
        return {
            'success': False,
            'error_message': 'Incorrect password.',
        }

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """Create canned scenario for display in the workbench."""
        return [
            ("XblockContentRestrictions",
             """<content_restrictions/>
             """),
            ("Multiple XblockContentRestrictions",
             """<vertical_demo>
                <content_restrictions/>
                <content_restrictions/>
                <content_restrictions/>
                </vertical_demo>
             """),
        ]

    def author_view(self, context):
        """
        Renders the Studio preview by rendering each child so that they can all be seen and edited.
        """
        fragment = Fragment()
        root_xblock = context.get('root_xblock')
        is_root = root_xblock and root_xblock.location == self.location
        if is_root:
            # User has clicked the "View" link. Show a preview of all possible children:
            self.render_children(context, fragment, can_reorder=True, can_add=True)
        # else: When shown on a unit page, don't show any sort of preview -
        # just the status of this block in the validation area.

        return fragment

    @staticmethod
    def _get_statici18n_js_url():
        """
        Return the Javascript translation file for the currently selected language, if any.

        Defaults to English if available.
        """
        locale_code = translation.get_language()
        if locale_code is None:
            return None
        text_js = 'public/js/translations/{locale_code}/text.js'
        lang_code = locale_code.split('-')[0]
        for code in (locale_code, lang_code, 'en'):
            loader = ResourceLoader(__name__)
            if pkg_resources.resource_exists(
                    loader.module_name, text_js.format(locale_code=code)):
                return text_js.format(locale_code=code)
        return None

    @staticmethod
    def get_dummy():
        """
        Generate initial i18n with dummy method.
        """
        return translation.gettext_noop('Dummy')
