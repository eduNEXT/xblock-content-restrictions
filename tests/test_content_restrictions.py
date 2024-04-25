"""
Tests for XblockContentRestrictions
"""

from unittest.mock import Mock, patch

from django.test import TestCase
from edx_django_utils import ip
from xblock.fields import ScopeIds
from xblock.test.toy_runtime import ToyRuntime

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
        self.block.ip_restriction = False
        self.block.password = ''
        self.block.user_provided_password = ''
        self.block.incorrect_password_explanation_text = 'Incorrect password'
        self.block.password_explanation_text = 'Enter the password'
        self.block.ip_whitelist = []
        self.block.ip_explanation_text = "Your IP address is not allowed to access this content."

    def test_student_view_without_children(self):
        """Render the student view without children.

        Expected result: an empty div.
        """
        self.block.children = []

        fragment = self.block.student_view({})
        self.assertIn(
            '<divclass="content_restrictions_block"><br></div>',
            fragment.content.replace('\n', '').replace(' ', ''),
        )

    def test_student_view_with_children(self):
        """Render the student view with children.

        Expected result: a div with the children content.
        """
        self.block.children = ['child1']
        self.runtime.get_block = Mock(return_value=self.child_block)

        fragment = self.block.student_view({})

        self.assertIn(
            '<divclass="content_restrictions_block">MyXBlock:countisnow0<br><hr><br></div>',
            fragment.content.replace('\n', '').replace(' ', ''),
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
        self.runtime.service = ToyRuntime().service
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

    @patch.object(ip, "get_all_client_ips")
    def test_student_view_with_ip_restriction(self, mock_get_all_client_ips: Mock):
        """Render the student view with IP restriction.

        Expected result: the IP template.
        """
        self.runtime.service = ToyRuntime().service
        self.block.ip_restriction = True
        self.block.ip_whitelist = ["172.16.0.1"]
        mock_get_all_client_ips.return_value = ["192.68.0.1"]

        fragment = self.block.student_view({})

        self.assertEqual(
            fragment.content.replace("\n", "").replace(" ", ""),
            """
            <div class="content_restrictions_block">
                <div class="content_restrictions">
                    <div class="ip_explanation_text"> Your IP address is not allowed to access this content. </div>
                </div>
            </div>
            """.replace(
                "\n", ""
            ).replace(
                " ", ""
            ),
        )

    @patch.object(ip, "get_all_client_ips")
    def test_has_access_with_ip_whitelist(self, mock_get_all_client_ips: Mock):
        """Test the `has_access_with_ip_whitelist` method.

        Expected result: True if the IP is in the whitelist, False otherwise.
        """
        mock_request = Mock()
        mock_get_all_client_ips.return_value = ["172.16.0.1"]
        self.block.ip_restriction = True
        self.block.ip_whitelist = ["172.16.0.1"]

        result = self.block.has_access_with_ip_whitelist(mock_request)

        self.assertTrue(result)

        mock_get_all_client_ips.return_value = ["192.168.0.1"]

        result = self.block.has_access_with_ip_whitelist(mock_request)

        self.assertFalse(result)

    @patch.object(XblockContentRestrictions, "has_access_with_ip_whitelist")
    def test_ip_restriction(self, mock_has_access_with_ip_whitelist: Mock):
        """Test the IP restriction.

        Expected result: True if the IP is in the whitelist, False otherwise.
        """
        self.block.ip_restriction = True
        mock_has_access_with_ip_whitelist.return_value = True

        self.assertTrue(self.block.has_access_to_content)

        mock_has_access_with_ip_whitelist.return_value = False

        self.assertFalse(self.block.has_access_to_content)

    @patch.object(XblockContentRestrictions, "has_access_with_ip_whitelist")
    def test_multiple_restrictions(self, mock_has_access_with_ip_whitelist: Mock):
        """Test the multiple restrictions.

        Expected result: True if all the restrictions are met, False otherwise.
        """
        self.block.password_restriction = True
        self.block.password = "1234"
        self.block.ip_restriction = True

        self.assertFalse(self.block.has_access_to_content)

        self.block.user_provided_password = "1234"
        mock_has_access_with_ip_whitelist.return_value = False

        self.assertFalse(self.block.has_access_to_content)

        mock_has_access_with_ip_whitelist.return_value = True

        self.assertTrue(self.block.has_access_to_content)

    def test_ip_has_access(self):
        """Test the `ip_has_access` method."""
        # client IP exactly matches the IP address (IPv4)
        self.assertTrue(self.block.ip_has_access("192.168.1.1", "192.168.1.1"))

        # client IP exactly matches the IP address (IPv6)
        self.assertTrue(self.block.ip_has_access("2001:db8::1", "2001:db8::1"))

        # client IP is within the IP range (IPv4)
        self.assertTrue(self.block.ip_has_access("192.168.1.2", "192.168.1.0/24"))

        # client IP is within the IP range (IPv6)
        self.assertTrue(self.block.ip_has_access("2001:db8::2", "2001:db8::/32"))

        # client IP is outside the IP range (IPv4)
        self.assertFalse(self.block.ip_has_access("192.168.2.1", "192.168.1.0/24"))

        # client IP is outside the IP range (IPv6)
        self.assertFalse(self.block.ip_has_access("2001:db9::1", "2001:db8::/32"))

        # invalid IP
        self.assertFalse(self.block.ip_has_access("192.168.1.1", "invalid_ip"))

        # invalid IP range
        self.assertFalse(self.block.ip_has_access("192.168.1.1", "invalid_range"))
