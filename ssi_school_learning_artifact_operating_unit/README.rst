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

Which operating units exist and which user receives which operating unit are
configuration data, not module data.

Work Instruction
================

Learning Artifact
-----------------

* `Create Learning Artifact (Operating Unit) <docs/school_learning_artifact/01-create.html>`_
