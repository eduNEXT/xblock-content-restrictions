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
        self.block.password_restriction = False
        self.block.password = ''
        self.block.user_provided_password = ''
        self.block.incorrect_password_explanation_text = 'Incorrect password'
        self.block.password_explanation_text = 'Enter the password'

    def test_student_view_without_children(self):
        """Render the student view without children.

        Expected result: an empty div.
        """
        self.block.children = []

        fragment = self.block.student_view({})

        self.assertEqual(
            fragment.content.replace('\n', '').replace(' ', ''),
            '<divclass="content_restrictions_block"><br></div>',
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
            '<divclass="content_restrictions_block">MyXBlock:countisnow0<br><br></div>',
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

    def test_password_restriction(self):
        """Test the password restriction.

        Expected result: True if the password is correct, False otherwise.
        """
        self.block.password_restriction = True
        self.block.password = '1234'

        self.assertFalse(self.block.has_access_to_content)

        self.block.user_provided_password = '1234'

        self.assertTrue(self.block.has_access_to_content)

    def test_student_view_with_password_restriction(self):
        """Render the student view with password restriction.

        Expected result: the password template.
        """
        self.block.password_restriction = True
        self.block.password = '1234'
        self.block.user_provided_password = ''

        fragment = self.block.student_view({})

        self.assertEqual(
            fragment.content.replace('\n', '').replace(' ', ''),
            """
            <div class="content_restrictions_block">
                <div class="content_restrictions">
                    <div class="password_explanation_text"> Enter the password </div>
                </div>
                <input type="password" class="password" name="password"/>
                <button class="submit-button">Submit</button>
                <div class="incorrect_password_explanation_text"></div>
            </div>
            """.replace('\n', '').replace(' ', ''),
        )

    def test_has_access_with_password(self):
        """Test the has_access_with_password method.

        Expected result: True if the password is correct, False otherwise.
        """
        self.block.password_restriction = True
        self.block.password = '1234'
        request = Mock(method='POST', body=b'{"password": "1234"}')

        self.assertTrue(self.block.has_access_with_password(request).json['success'])

        request = Mock(method='POST', body=b'{"password": "12345"}')

        self.assertFalse(self.block.has_access_with_password(request).json['success'])
