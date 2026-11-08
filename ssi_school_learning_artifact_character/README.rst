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

A line of the status of an indicator can optionally be limited to some grades
of the grade type, so the status can differ between the grades of one grade
type, for example lower and upper grades of the primary level. A line without
grades applies to every grade of the grade type. For one indicator and one
grade type there is either one line without grades, or several lines whose
grades do not overlap.

The teacher can also select the character indicators of an artifact. The
choice lists the indicators of an active sub-construct, narrowed to the
indicators that are Effective or Partial at the grade of the artifact when a
status line applies to it. Every selected indicator must belong to the
dominant or the secondary tag, and an artifact marked as not clearly evident
has no indicator. The policy field "Can Select Character Indicator" decides
who can fill in the indicators: the user group while the artifact is a draft,
and the validator group while it is waiting for approval or on progress. The
indicators are optional.

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
* `Select Character Indicator of Learning Artifact <docs/school_learning_artifact/13-select-character-indicator.html>`_
