.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
School Learning Artifact
========================

Inventory of learning artifacts (photos, videos and documents of learning
activities and achievements) for schools. A teacher records an artifact,
submits it for curation, and may withdraw it until the curator starts the
curation. The curator then fills in the ethics gate and scores the aspects of
the rubric of the school; the module calculates the total and the curation
status, and the curation is finished with the Done action. A curated artifact
whose status needs a revision can be reopened a limited number of times.
Everything specific to a school or a branch - learning areas, categories,
dimensions, phases, distinctive programs and their components, graduate
profiles, curation rubrics, statuses and ethics reasons, the link prefix and
the required fields - is configuration data, not module data.

The module also keeps the parental consent of the students. The consent is
recorded in the data privacy consent log of the contact of the student, once
per student per school unit, as a full or a limited consent for four usages of
an artifact: inventory, internal assessment, publication and promotion. Every
artifact shows the strictest consent of its students per usage, and it cannot
be submitted when a student refused the inventory consent (or has no inventory
consent recorded, when the school requires it).

A curated artifact is also placed on a showcase board. The showcase is an
internal record of the selection of the artifact, the content produced for
each channel and the distribution, which happens outside Odoo. The stages and
the channels are configuration data per school, a stage can require an eligible
curation status, a publication consent that allows the showcase, or membership
of a group, and every move of a card is logged in the chatter. The consent
policy of the showcase is set per school: the lowest accepted publication
consent, whether a limited consent is blocked or becomes a review task, and
whether the students who refused the publication are left out.


Work Instruction
================

Learning Artifact
-----------------

* `Create Learning Artifact <docs/school_learning_artifact/01-create.html>`_
* `Submit Learning Artifact for Curation <docs/school_learning_artifact/02-submit.html>`_
* `Withdraw Learning Artifact from Curation <docs/school_learning_artifact/03-withdraw.html>`_
* `Start Curation of Learning Artifact <docs/school_learning_artifact/04-start-curation.html>`_
* `Cancel Learning Artifact <docs/school_learning_artifact/05-cancel.html>`_
* `Curate Learning Artifact <docs/school_learning_artifact/06-curate.html>`_
* `Reopen Learning Artifact for Revision <docs/school_learning_artifact/07-reopen.html>`_
* `Select Learning Artifact for Showcase <docs/school_learning_artifact/08-select-for-showcase.html>`_
* `Record Showcase Production of Learning Artifact <docs/school_learning_artifact/09-produce-showcase.html>`_
* `Review Limited Publication Consent of Learning Artifact <docs/school_learning_artifact/10-review-limited-consent.html>`_

Learning Artifact Area
----------------------

* `Create Learning Artifact Area <docs/school_learning_artifact_area/01-create.html>`_

Learning Artifact Category
--------------------------

* `Create Learning Artifact Category <docs/school_learning_artifact_category/01-create.html>`_

Learning Artifact Curation Status
---------------------------------

* `Create Learning Artifact Curation Status <docs/school_learning_artifact_curation_status/01-create.html>`_

Learning Artifact Ethics Reason
-------------------------------

* `Create Learning Artifact Ethics Reason <docs/school_learning_artifact_ethics_reason/01-create.html>`_

Learning Artifact Showcase Stage
--------------------------------

* `Create Learning Artifact Showcase Stage <docs/school_learning_artifact_showcase_stage/01-create.html>`_

Learning Artifact Showcase Channel
----------------------------------

* `Create Learning Artifact Showcase Channel <docs/school_learning_artifact_showcase_channel/01-create.html>`_

Learning Artifact Rubric
------------------------

* `Create Learning Artifact Rubric <docs/school_learning_artifact_rubric/01-create.html>`_

Learning Artifact Dimension
---------------------------

* `Create Learning Artifact Dimension <docs/school_learning_artifact_dimension/01-create.html>`_

Learning Artifact Phase
-----------------------

* `Create Learning Artifact Phase <docs/school_learning_artifact_phase/01-create.html>`_

Distinctive Program
-------------------

* `Create Distinctive Program <docs/school_distinctive_program/01-create.html>`_

Distinctive Program Component
-----------------------------

* `Create Distinctive Program Component <docs/school_distinctive_program_component/01-create.html>`_

Graduate Profile
----------------

* `Create Graduate Profile <docs/school_graduate_profile/01-create.html>`_

Student
-------

* `Record Learning Artifact Consent <docs/school_student/01-record-learning-artifact-consent.html>`_

Consent Purpose
---------------

* `Set Learning Artifact Usage on a Consent Purpose <docs/partner_consent_purpose/01-set-learning-artifact-usage.html>`_


Installation
============

To install this module, you need to:

1.  Clone the branch 14.0 of the repository https://github.com/open-synergy/ssi-school-learning-artifact
2.  Add the path to this repository in your configuration (addons-path)
3.  Update the module list (Must be on developer mode)
4.  Go to menu *Apps -> Apps -> Main Apps*
5.  Search For *School Learning Artifact*
6.  Install the module


Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/open-synergy/ssi-school-learning-artifact/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.


Credits
=======

Contributors
------------

* Andhitia Rama <andhitia.r@gmail.com>

Maintainer
----------

.. image:: https://simetri-sinergi.id/logo.png
   :alt: PT. Simetri Sinergi Indonesia
   :target: https://simetri-sinergi.id

This module is maintained by the PT. Simetri Sinergi Indonesia.
