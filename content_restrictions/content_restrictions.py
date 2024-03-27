"""TO-DO: Write a description of what this XBlock is."""
from enum import Enum
import pkg_resources
from django.utils import translation
from lazy import lazy
from xblock.core import XBlock
from xblock.fields import Integer, ReferenceList, Scope, String
from xblock.fragment import Fragment
from collections import namedtuple
from xblockutils.resources import ResourceLoader
from xblock.utils.studio_editable import StudioContainerWithNestedXBlocksMixin, StudioEditableXBlockMixin, NestedXBlockSpec
from xmodule.modulestore.exceptions import ItemNotFoundError
from xmodule.capa_block import ProblemBlock
from openassessment.xblock.openassessmentblock import OpenAssessmentBlock
from xblock.utils.resources import ResourceLoader


# Make '_' a no-op so we can scrape strings
_ = lambda text: text
loader = ResourceLoader(__name__)


class ContentRestrictions(Enum):
    """Types of content restrictions."""
    IP_WHITELIST = "IP Whitelist"
    PASSWORD = "Password"
    BROWSER = "Browser"


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
        default=ContentRestrictions.IP_WHITELIST,
        scope=Scope.settings,
        values=[
            {
                "display_name": restriction.value,
                "value": restriction.name
            }
            for restriction in ContentRestrictions
        ],
        help="Type of restriction to apply to learners.",
    )

    editable_fields = [
        "display_name",
        "restriction_type",
    ]

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def student_view(self, context):
        """
        View for previewing contents in studio.
        """
        children_contents = []

        fragment = Fragment()
        for child_id in self.children:
            child = self.runtime.get_block(child_id)
            child_fragment = self._render_child_fragment(child, context, 'student_view')
            fragment.add_fragment_resources(child_fragment)
            children_contents.append(child_fragment.content)

        render_context = {
            'block': self,
            'children_contents': children_contents
        }
        render_context.update(context)
        fragment.add_content(self.loader.render_django_template(self.CHILD_PREVIEW_TEMPLATE, render_context))
        return fragment

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
