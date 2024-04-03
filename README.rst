Content Restrictions XBlock
############################

|status-badge| |license-badge| |ci-badge|


Purpose
*******

Used when course designers need to control the conditions under which a learner can access the contents of a course.


Enabling the XBlock in a course
*******************************

Once the XBlock has been installed in your Open edX installation, you can enable it in a course from Studio
through the **Advanced Settings**.

1. Go to Studio and open the course you want to add the XBlock to.
2. Go to **Settings** > **Advanced Settings** from the top menu.
3. Search for **Advanced Module List** and add ``"content_restrictions"`` to the list.
4. Click **Save Changes** button.


Adding a Content Restrictions Component to a course unit
********************************************************

From Studio, you can add the Content Restrictions Component to a course unit.

1. Click on the **Advanced** button in **Add New Component**.
2. Select **Content Restrictions** from the list.
3. Configure the component as needed.

There are four restriction options that can be applied to the content:

**No Restriction**: The content is always available.
**IP Whitelist**: The content is only available to users with an IP address that matches the specified list. For this restriction, you need to specify a list of IP addresses.
**Password**: The content is only available to users who enter the specified password. For this restriction, you need to specify a password.
**Secure Exam Browser (SEB)**: The content is only available to users who access the course using the Secure Exam Browser.

These restrictions are applied to the children of the Content Restrictions component. So in the Author View, you can add
any other component as a child of the Content Restrictions component, and the restrictions will be applied to that component.


View from the Learning Management System (LMS)
**********************************************

When a learner accesses the course, the Content Restrictions component will be displayed as a message indicating the
restriction that applies to the content and the action that the learner needs to take to access the content.

Experimenting with this XBlock in the Workbench
************************************************

`XBlock`_ is the Open edX component architecture for building custom learning
interactive components.

.. _XBlock: https://openedx.org/r/xblock

You can see the Content Restrictions component in action in the XBlock Workbench.
Running the Workbench requires having docker running.

.. code:: bash

    git clone git@github.com:eduNEXT/xblock-content-restrictions
    virtualenv venv/
    source venv/bin/activate
    cd xblock-content-restrictions
    make upgrade
    make install
    make dev.run

Once the process is done, you can interact with the Content Restrictions XBlock in
the Workbench by navigating to http://localhost:8000

For details regarding how to deploy this or any other XBlock in the Open edX
platform, see the `installing-the-xblock`_ documentation.

.. _installing-the-xblock: https://edx.readthedocs.io/projects/xblock-tutorial/en/latest/edx_platform/devstack.html#installing-the-xblock


Getting Help
*************

If you're having trouble, the Open edX community has active discussion forums
available at https://discuss.openedx.org where you can connect with others in
the community.

Also, real-time conversations are always happening on the Open edX community
Slack channel. You can request a `Slack invitation`_, then join the
`community Slack workspace`_.

For anything non-trivial, the best path is to open an `issue`_ in this
repository with as many details about the issue you are facing as you can
provide.

For more information about these options, see the `Getting Help`_ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/
.. _issue: https://github.com/eduNEXT/xblock-content-restrictions/issues
.. _Getting Help: https://openedx.org/getting-help


License
*******

The code in this repository is licensed under the AGPL-3.0 unless otherwise
noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


Contributing
************

Contributions are very welcome.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.


Reporting Security Issues
*************************

Please do not report a potential security issue in public. Please email
security@edunext.co.


.. |ci-badge| image:: https://github.com/eduNEXT/xblock-content-restrictions/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/xblock-content-restrictions/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/xblock-content-restrictions.svg
    :target: https://github.com/eduNEXT/xblock-content-restrictions/blob/main/LICENSE.txt
    :alt: License

.. |status-badge| image:: https://img.shields.io/badge/Status-Maintained-brightgreen
