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

1. Go to Studio and open the course to which you want to add the XBlock.
2. Go to **Settings** > **Advanced Settings** from the top menu.
3. Search for **Advanced Module List** and add ``"content_restrictions"`` to the list.
4. Click **Save Changes** button.


Adding a Content Restrictions Component to a course unit
********************************************************

From Studio, you can add the Content Restrictions Component to a course unit.

1. Click on the **Advanced** button in **Add New Component**.

   .. image:: https://github.com/eduNEXT/xblock-content-restrictions/assets/64440265/b0ee88bb-f3d3-40da-ba4d-281c3efbabb6
      :alt: Open Advanced Components

2. Select **Content With Access Restrictions** from the list.

   .. image:: https://github.com/eduNEXT/xblock-content-restrictions/assets/64440265/4e191109-37ca-458a-b338-32d5b1a84cd3
      :alt: Select Content Restrictions Component

3. Configure the component as needed.


View from the Learning Management System (CMS)
**********************************************

Password Restriction
--------------------

When you select the Password restriction option, you need to specify a password that the learner must enter to access the content.
Specify the password in the **Password** field in the Content Restrictions component configuration. The password is case-sensitive.
After publishing the unit with the Content Restrictions component, the learner will see a message indicating that the content is restricted and will be prompted to enter the password to access the content.
When the learner enters the correct password, the content will be displayed.

There are the available configuration options for the Password restriction:

- **Password Restriction**: Enable or disable the password restriction. If disabled, the other configuration options will be ignored.
- **Password**: The password that the learner must enter to access the content.
- **Password Explanation Text**: The text that will be displayed to the learner to explain how to access the content.
- **Incorrect Password Explanation Text**: The text that will be displayed to the learner when the entered password is incorrect.

Here is how the Content Restrictions component looks in the Author View:

   .. image:: https://github.com/eduNEXT/xblock-content-restrictions/assets/64440265/5f9e73d0-4def-41bd-b3ab-ffae1ec958b3
      :alt: Author view for component

When accessing the component by selecting the **view** button, you will see the list of children components that are restricted by the Content Restrictions component.

   .. image:: https://github.com/eduNEXT/xblock-content-restrictions/assets/64440265/e8dedf11-4e04-4592-8d8f-a23a4db7952a
      :alt: View of the component

Here is an example of a Content Restrictions component with a Problem component as a child:

    .. image:: https://github.com/eduNEXT/xblock-content-restrictions/assets/64440265/724a5a32-1488-41e6-b52d-236c53af8179
       :alt: Example of a Content Restrictions component with a Problem component as a child

These restrictions are applied to children in the Content Restrictions component. So in the Author View, you can add
any other component as a child of the Content Restrictions component and the restrictions will be applied to those components.

View from the Learning Management System (LMS)
**********************************************

When a learner accesses the course, the Content Restrictions component will be displayed as a message indicating the
restriction that applies to the content and the action the learner needs to take to access the content.

Password Restriction
--------------------

When the Password restriction is enabled, the learner will see a message indicating that the content is restricted and will be prompted to enter the password to access the content.
After entering the correct password, the content will be displayed. If the learner enters an incorrect password, a message will be displayed indicating that the password is incorrect.

Here is an example of the message that the learner will see when the content is restricted by a password:

   .. image:: https://github.com/eduNEXT/xblock-content-restrictions/assets/64440265/e6a14193-4370-4752-b82a-751c35afc8e5
        :alt: Password restriction message

When the learner enters the correct password, the content will be displayed. However, if the learner enters an incorrect password, a message will be displayed indicating that the password is incorrect.

   .. image:: https://github.com/eduNEXT/xblock-content-restrictions/assets/64440265/f345f874-1a58-4f8d-ae12-7fa6087c6c8b
        :alt: Incorrect password message

As specified in the configuration, the learner will see the explanation text and the incorrect password explanation text.

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
