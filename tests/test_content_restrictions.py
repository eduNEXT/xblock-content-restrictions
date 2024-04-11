"""
Tests for XblockContentRestrictions
"""

from django.test import TestCase
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime
from unittest.mock import Mock

from content_restrictions.content_restrictions import XblockContentRestrictions


class TestXblockContentRestrictions(TestCase):
    """Tests for XblockContentRestrictions class."""

    def setUp(self) -> None:
        """Set up the test suite."""
        self.runtime = Mock()
        self.child_block = Mock(
            render=
            Mock(
                return_value=Mock(
                    content='MyXBlock: count is now 0',
                    resources=[],
                ),
            ),
        )
        self.block = XblockContentRestrictions(
            runtime=self.runtime,
            field_data={},
            scope_ids=ScopeIds('1', '2', '3', '4'),
        )

    def test_student_view_without_children(self):
        """Render the student view without children.

        Expected result: an empty div.
        """
        self.block.children = []

        fragment = self.block.student_view({})

        self.assertEqual(
            fragment.content.replace('\n', '').replace(' ', ''),
            '<divclass="content_restrictions_block"></div>',
        )

    def test_student_view_with_children(self):
        """Render the student view with children.

        Expected result: a div with the children content.
        """
        self.block.children = ['child1']
        self.runtime.get_block = Mock(return_value=self.child_block)

        fragment = self.block.student_view({})

        self.assertEqual(
            fragment.content.replace('\n', '').replace(' ', ''),
            '<divclass="content_restrictions_block">MyXBlock:countisnow0</div>',
        )


    def test_author_view_root(self):
        """Render the author view with the root block.

        Expected result: a div with the children content.
        """
        self.block.location = 'root'
        self.block.children = ['child1']
        self.runtime.get_block = Mock(return_value=self.child_block)
        self.runtime.service = Mock(
            return_value=Mock(
                render_template=Mock(
                    return_value='<div class="content_restrictions_block"> MyXBlock: count is now 0 </div>',
                ),
            ),
        )

        fragment = self.block.author_view({'root_xblock': self.block})

        self.assertEqual(
            fragment.content.replace('\n', '').replace(' ', ''),
            '<divclass="content_restrictions_block">MyXBlock:countisnow0</div>',
        )

    def test_author_view(self):
        """Render the author view without the root block.

        Expected result: an empty div.
        """
        fragment = self.block.author_view({})

        self.assertEqual(
            fragment.content.replace('\n', '').replace(' ', ''),
            '',
        )
