Content Restrictions XBlock
###########################

|status-badge| |license-badge| |ci-badge|


Purpose
*******

Content Restriction XBlock is used when course designers need to control the
conditions under which a learner can access the contents of a course.

This XBlock has been created as an open source contribution to the Open edX
platform and has been funded by Unidigital project from the Spanish Government
- 2023.

Compatibility Notes
===================

+------------------+--------------+
| Open edX Release | Version      |
+==================+==============+
| Palm             | >= 0.4.0     |
+------------------+--------------+
| Quince           | >= 0.4.0     |
+------------------+--------------+
| Redwood          | >= 0.4.0     |
+------------------+--------------+

The settings can be changed in ``content_restrictions/settings/common.py`` or,
for example, in tutor configurations.

**NOTE**: the current ``common.py`` works with Open edX Palm, Quince and Redwood
version.
