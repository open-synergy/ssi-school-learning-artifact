.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
School Learning Artifact - Character Tag
==========================================

Adds a character tag to a learning artifact, taken from the character
sub-constructs of the character learning module. An artifact can carry a
dominant and a secondary tag, or be marked as not clearly evident, in which
case the dominant tag must stay empty. The tag only marks the activity; it is
not evidence of the character achievement of a student, so it does not depend
on the character observations and it is not blocked when the assessment
consent of a student is refused.

Only the users allowed by the policy field "Can Tag Character" can fill in the
tags. The standard policy template grants it to the validator group while the
artifact is a draft, waiting for approval or on progress; the mapping to the
real roles of a school is policy configuration.

A school can optionally filter the choice of tags per grade type. The status
(Effective, Partial or Not Effective) of an indicator is set per grade type
on the indicator itself. When the grade type of an artifact has statuses,
only the sub-constructs with an Effective or Partial indicator at that grade
type can be tagged; a grade type without any status keeps every active
sub-construct available.

The character domains, sub-constructs, indicators and statuses of a school are
configuration data, not module data.


Work Instruction
================

Character Indicator
-------------------

* `Set Grade Status of Character Indicator <docs/school_character_indicator/01-set-grade-status.html>`_

Learning Artifact
-----------------

* `Tag Character of Learning Artifact <docs/school_learning_artifact/11-tag-character.html>`_
