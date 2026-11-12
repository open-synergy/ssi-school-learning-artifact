.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
School Learning Artifact
========================

Inventory of learning artifacts (photos, videos and documents of learning
activities and achievements) for schools. A teacher records an artifact,
submits it for curation, and may withdraw it until the curator starts the
curation. The curator first picks a level for every ethics gate aspect of the
rubric of the school in the Ethics Gate table (an aspect whose gate source is
Inventory Consent is filled by the system from the inventory consent of the
students and cannot be picked by hand); only when every gate aspect
passes, the curator picks a level for every scored aspect in the Artifact
Assessment table, and the server refuses a scored level before that, also
through import or API. The score of each level is recorded
automatically and the module calculates the total and the curation status, and
the curation is finished with the Done action. A curated artifact whose status
needs a revision can be reopened a limited number of times; when the limit
is reached the curator picks an archive or not eligible status as the final
status. The rubric of an artifact that is not assessed yet is picked again when
the curation starts, and a report counts the aspects assessed by each person.
Everything specific to a school or a branch - learning areas, categories,
dimensions, phases, distinctive programs and their components, graduate
profiles, curation rubrics (with their aspect levels and ethics gate aspects),
statuses, the link prefix and the required fields - is configuration data, not
module data.

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
curation status or membership of a group, any stage needs a parental
consent that allows the showcase, and every move of a card is logged in the
chatter. An artifact leaves the board by itself when its consent is withdrawn
or its ethics gate no longer passes, and a limited inventory consent needs a
consent review first. The consent policy of the showcase is set per school: the lowest accepted publication
consent, whether a limited consent is blocked or becomes a review task, and
whether the students who refused the publication are left out. A channel can
also require a full publication consent: a production is refused for it when
the effective publication consent of the artifact is not full, and when the
consent is later lowered or withdrawn the production is marked as not meeting
the channel and its Ready check is cleared.

The narrative of each channel goes through a workflow. The inventory
coordinator returns a curated artifact narrative to the teacher who made the
artifact, the teacher writes it within the minimum and maximum words of the
channel and submits it, and the coordinator returns it for a revision (the
limit is set per school, beyond it the coordinator revises it) or sends it to
a multiple approval. The approvers (for example the principal, then the branch
person in charge) are added by the administrator as details of the approval
template of the narrative: while the template has no detail the approval is
refused. Only an approved narrative can be ready, and the content is locked
once the narrative is submitted.


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
* `Return Showcase Narrative to the Teacher <docs/school_learning_artifact/13-return-narrative-to-teacher.html>`_
* `Submit Showcase Narrative <docs/school_learning_artifact/14-submit-narrative.html>`_
* `Request Approval of Showcase Narrative <docs/school_learning_artifact/15-request-narrative-approval.html>`_
* `Return Showcase Narrative for Revision <docs/school_learning_artifact/16-return-narrative.html>`_
* `Approve Showcase Narrative <docs/school_learning_artifact/17-approve-narrative.html>`_
* `Reject Showcase Narrative <docs/school_learning_artifact/18-reject-narrative.html>`_
* `Set the Final Status of a Learning Artifact <docs/school_learning_artifact/12-set-final-status.html>`_

Learning Artifact Area
----------------------

* `Create Learning Artifact Area <docs/school_learning_artifact_area/01-create.html>`_

Learning Artifact Category
--------------------------

* `Create Learning Artifact Category <docs/school_learning_artifact_category/01-create.html>`_

Learning Artifact Curation Status
---------------------------------

* `Create Learning Artifact Curation Status <docs/school_learning_artifact_curation_status/01-create.html>`_

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
