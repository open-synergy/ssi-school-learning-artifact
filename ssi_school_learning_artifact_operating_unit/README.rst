.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

=============================================
School Learning Artifact - Operating Unit
=============================================

Adds operating unit support to the Learning Artifact so the artifacts of a
branch can be separated per unit inside one company.

Every artifact carries one operating unit. It is taken from the school of the
artifact whenever that school belongs to exactly one operating unit; a school
without operating unit or with several operating units never triggers a guess
and the value already set (by default the operating unit of the creating user)
is kept. An operating unit entered explicitly always wins, and it is derived
again only when the school of an existing artifact is changed.

The module adds the data ownership group "Operating Unit". A user in this
group only sees the artifacts of the operating units assigned to the user, so
a unit role is a user with this group and the operating unit of the unit, and a
branch role is a user with this group and all the operating units of the
branch. The "Company" data ownership group of the learning artifact implies the
new group, so the users that see every artifact of the company keep doing so.

The module also adds the field Operating Unit (many operating units) to the
seven master data of the learning artifact: category, phase, dimension,
rubric, curation status, showcase stage and showcase channel. A global read
rule limits every user, whatever the group, to the records without operating
unit and the records of the operating units of the user. The master data choices
of an artifact (and the rubric of the artifact) follow the operating unit of the
artifact: a record without operating unit applies to every unit, an artifact
without operating unit is only offered the records without operating unit. On
upgrade the operating units of each master are filled from the operating units
of the schools it listed.

Which operating units exist and which user receives which operating unit are
configuration data, not module data.

Work Instruction
================

Learning Artifact
-----------------

* `Create Learning Artifact (Operating Unit) <docs/school_learning_artifact/01-create.html>`_

Learning Artifact Category
--------------------------

* `Create Learning Artifact Category (Operating Unit) <docs/school_learning_artifact_category/01-create.html>`_

Learning Artifact Phase
-----------------------

* `Create Learning Artifact Phase (Operating Unit) <docs/school_learning_artifact_phase/01-create.html>`_

Learning Artifact Dimension
---------------------------

* `Create Learning Artifact Dimension (Operating Unit) <docs/school_learning_artifact_dimension/01-create.html>`_

Learning Artifact Rubric
------------------------

* `Create Learning Artifact Rubric (Operating Unit) <docs/school_learning_artifact_rubric/01-create.html>`_

Learning Artifact Curation Status
---------------------------------

* `Create Learning Artifact Curation Status (Operating Unit) <docs/school_learning_artifact_curation_status/01-create.html>`_

Learning Artifact Showcase Stage
--------------------------------

* `Create Learning Artifact Showcase Stage (Operating Unit) <docs/school_learning_artifact_showcase_stage/01-create.html>`_

Learning Artifact Showcase Channel
----------------------------------

* `Create Learning Artifact Showcase Channel (Operating Unit) <docs/school_learning_artifact_showcase_channel/01-create.html>`_
