"""XBlock for content restrictions."""
import pkg_resources
from django.utils import translation
from xblock.core import XBlock
from xblock.fields import Boolean, Scope, String
from xblock.utils.resources import ResourceLoader
from xblock.utils.studio_editable import StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin

try:
    from xblock.fragment import Fragment
except ModuleNotFoundError:
    from web_fragments.fragment import Fragment

LOCAL_RESOURCE_LOADER = ResourceLoader(__name__)


def _(text):
    """Make '_' a no-op so we can scrape strings."""
    return text

@XBlock.needs("i18n")
class XblockContentRestrictions(
    StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin, XBlock
):
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
        help=_(
            "This message will be shown when the learner enters an incorrect password."
        ),
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

    editable_fields = [
        "display_name",
        "password_restriction",
        "password_explanation_text",
        "incorrect_password_explanation_text",
        "password",
    ]

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

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
        if self.service_declaration("i18n"):
            ugettext = self.ugettext
        else:
            def ugettext(text):
                """Get dummy ugettext method that doesn't do anything."""
                return text

        fragment = Fragment()
        context = {'fields': []}
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
                    # pylint: disable=translation-of-non-string
                    field_info["default"] = ugettext(field_info["default"]) if field_info["default"] else ""
                    field_info["value"] = ugettext(field_info["value"]) if field_info["value"] else ""
                context["fields"].append(field_info)
        fragment.content = self.loader.render_django_template('templates/studio_edit.html', context)
        fragment.add_javascript(self.loader.load_unicode('public/studio_edit.js'))
        fragment.initialize_js('StudioEditableXBlockMixin')
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
        """
        if self.password_restriction:
            return bool(self.user_provided_password == self.password)
        return True

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
        statici18n_js_url = self._get_statici18n_js_url()
        if statici18n_js_url:
            fragment.add_javascript_url(
                self.runtime.local_resource_url(self, statici18n_js_url)
            )

        fragment.add_javascript(
            self.resource_string("static/js/src/content_restrictions.js")
        )
        fragment.initialize_js("XblockContentRestrictions")
        return fragment

    @property
    def restriction_template(self):
        """
        Get the current restriction template.

        Returns:
            str: The current restriction template.
        """
        if self.password_restriction:
            return "password_restriction.html"
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
        if self.user_provided_password == self.password:
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

    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():  # pragma: no cover
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

    @staticmethod
    def _get_statici18n_js_url():  # pragma: no cover
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
