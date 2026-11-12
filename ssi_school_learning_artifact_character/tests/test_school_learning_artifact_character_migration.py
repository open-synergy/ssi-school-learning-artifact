# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import importlib.util
import os

from odoo_yaml_test import YamlTransactionCase
from openupgradelib import openupgrade

from odoo.modules.module import get_module_path
from odoo.tests import tagged

MODULE = "ssi_school_learning_artifact_character"
MIGRATION_DIR = os.path.join("migrations", "14.0.1.2.0")
ARTIFACT_TABLE = "school_learning_artifact"
OLD_INDICATOR_TABLE = "school_learning_artifact_character_indicator_rel"


@tagged("post_install", "-at_install")
class TestSchoolLearningArtifactCharacterMigration(YamlTransactionCase):
    """Test the migration of the character tags to many tags.

    Covers the pre and post scripts of ``migrations/14.0.1.2.0``,
    which YAML scenarios cannot load from their files.
    """

    def setUp(self):
        """Create the school data, the character master and the artifacts.

        Three artifacts are created: one with a dominant and a
        secondary tag, one whose secondary tag equals the dominant
        tag, and one without any tag. The legacy columns and the
        legacy table are prepared by ``_prepare_legacy``.

        :return: None
        """
        super().setUp()
        env = self.env
        grade_type = env["school_grade_type"].create(
            {"name": "CM Grade Type", "code": "/", "sequence": 10}
        )
        school = env["school"].create(
            {"name": "CM School", "code": "/", "grade_type_id": grade_type.id}
        )
        grade = env["school_grade"].create(
            {"name": "CM Grade", "code": "/", "sequence": 10, "type_id": grade_type.id}
        )
        grade_class = env["school_grade_class"].create(
            {
                "name": "CM Class",
                "code": "/",
                "school_id": school.id,
                "grade_id": grade.id,
                "capacity": 30,
            }
        )
        year = env["school_academic_year"].create(
            {
                "name": "CM Year",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        area = env["school_learning_artifact_area"].create(
            {
                "name": "CM Area",
                "code": "/",
                "school_id": school.id,
                "area_type": "subject",
            }
        )
        category = env["school_learning_artifact_category"].create(
            {"name": "CM Category", "code": "/"}
        )
        contact = env["res.partner"].create({"name": "CM Contact"})
        student = env["school_student"].create(
            {
                "name": "CM Student",
                "code": "/",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        construct = env["school_character_construct"].create(
            {"name": "CM Construct", "code": "CM-CON"}
        )
        obj_subconstruct = env["school_character_subconstruct"]
        self.sub_a = obj_subconstruct.create(
            {"name": "CM Sub A", "code": "CM-SA", "construct_id": construct.id}
        )
        self.sub_b = obj_subconstruct.create(
            {"name": "CM Sub B", "code": "CM-SB", "construct_id": construct.id}
        )
        obj_indicator = env["school_character_indicator"]
        self.ind_a = obj_indicator.create(
            {
                "name": "CM Indicator A",
                "code": "CM-IA",
                "construct_id": construct.id,
                "subconstruct_id": self.sub_a.id,
            }
        )
        self.ind_b = obj_indicator.create(
            {
                "name": "CM Indicator B",
                "code": "CM-IB",
                "construct_id": construct.id,
                "subconstruct_id": self.sub_b.id,
            }
        )
        self.ind_none = obj_indicator.create(
            {
                "name": "CM Indicator None",
                "code": "CM-IN",
                "construct_id": construct.id,
            }
        )
        values = {
            "school_id": school.id,
            "academic_year_id": year.id,
            "grade_class_id": grade_class.id,
            "media_type": "photo",
            "user_id": env.ref("base.user_admin").id,
            "student_ids": [(6, 0, student.ids)],
            "learning_area_id": area.id,
            "category_id": category.id,
            "description": "one two three",
            "link_url": "https://drive.example.com/file",
        }
        obj_artifact = env["school_learning_artifact"]
        self.art_tags = obj_artifact.create(dict(values, activity_name="CM Tags"))
        self.art_same = obj_artifact.create(dict(values, activity_name="CM Same"))
        self.art_free = obj_artifact.create(dict(values, activity_name="CM Free"))
        self.art_none = obj_artifact.create(dict(values, activity_name="CM None"))

    def _prepare_legacy(self):
        """Create the legacy columns and table holding the old data.

        The columns and the table take the names that the pre script
        gives them. ``art_tags`` has the dominant tag A, the secondary
        tag B and the indicators A and B; ``art_same`` has A as the
        dominant and the secondary tag with indicator A; ``art_free``
        has no tag and the indicators A, B and one without
        sub-construct; ``art_none`` has nothing.

        :return: None
        """
        cr = self.env.cr
        primary = openupgrade.get_legacy_name("primary_subconstruct_id")
        secondary = openupgrade.get_legacy_name("secondary_subconstruct_id")
        legacy_table = openupgrade.get_legacy_name(OLD_INDICATOR_TABLE)
        for column in (primary, secondary):
            cr.execute(
                'ALTER TABLE %s ADD COLUMN "%s" integer' % (ARTIFACT_TABLE, column)
            )
        cr.execute(
            'CREATE TABLE "%s" (artifact_id integer, indicator_id integer)'
            % legacy_table
        )
        for artifact, dominant, other in (
            (self.art_tags, self.sub_a, self.sub_b),
            (self.art_same, self.sub_a, self.sub_a),
        ):
            cr.execute(
                'UPDATE %s SET "%s" = %%s, "%s" = %%s WHERE id = %%s'
                % (ARTIFACT_TABLE, primary, secondary),
                (dominant.id, other.id, artifact.id),
            )
        pairs = [
            (self.art_tags, self.ind_a),
            (self.art_tags, self.ind_b),
            (self.art_same, self.ind_a),
            (self.art_free, self.ind_a),
            (self.art_free, self.ind_b),
            (self.art_free, self.ind_none),
        ]
        for artifact, indicator in pairs:
            cr.execute(
                'INSERT INTO "%s" (artifact_id, indicator_id) VALUES (%%s, %%s)'
                % legacy_table,
                (artifact.id, indicator.id),
            )

    def _load_script(self, name):
        """Load a migration script from its file.

        :param name: file name of the script in the migration directory
        :return: the loaded module
        """
        path = os.path.join(get_module_path(MODULE), MIGRATION_DIR, name)
        spec = importlib.util.spec_from_file_location(
            name.replace("-", "_").replace(".py", ""), path
        )
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        return script

    def _assert_migrated(self):
        """Assert the four new relations hold the migrated data.

        :return: None
        """
        self.env.cache.invalidate()
        tags = self.art_tags
        self.assertEqual(tags.dominant_subconstruct_ids, self.sub_a)
        self.assertEqual(tags.secondary_subconstruct_ids, self.sub_b)
        self.assertEqual(tags.dominant_indicator_ids, self.ind_a)
        self.assertEqual(tags.secondary_indicator_ids, self.ind_b)
        same = self.art_same
        self.assertEqual(same.dominant_subconstruct_ids, self.sub_a)
        self.assertFalse(same.secondary_subconstruct_ids)
        self.assertEqual(same.dominant_indicator_ids, self.ind_a)
        self.assertFalse(same.secondary_indicator_ids)
        free = self.art_free
        self.assertEqual(free.dominant_subconstruct_ids, self.sub_a | self.sub_b)
        self.assertFalse(free.secondary_subconstruct_ids)
        self.assertEqual(free.dominant_indicator_ids, self.ind_a | self.ind_b)
        self.assertFalse(free.secondary_indicator_ids)
        none = self.art_none
        self.assertFalse(none.dominant_subconstruct_ids)
        self.assertFalse(none.secondary_subconstruct_ids)
        self.assertFalse(none.dominant_indicator_ids)
        self.assertFalse(none.secondary_indicator_ids)

    def test_post_migration(self):
        """Fill the four new relations from the legacy data.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.2.0/post-migration.py``, which
        ``EVAL:`` cannot do). Cases: (a) the old dominant tag becomes
        a dominant tag; (b) the old secondary tag becomes a secondary
        tag unless it equals the dominant one; (c) the indicators of
        the old dominant tag become dominant indicators; (d) the
        indicators of the old secondary tag become secondary
        indicators; (e) an artifact without a tag gets the
        sub-construct of each indicator as a dominant tag, and the
        indicators as dominant indicators. A second run changes
        nothing.
        """
        self._prepare_legacy()
        script = self._load_script("post-migration.py")
        script.migrate(self.env.cr, "14.0.1.1.1")
        self._assert_migrated()
        script.migrate(self.env.cr, "14.0.1.1.1")
        self._assert_migrated()

    def test_pre_migration(self):
        """Rename the old columns and table to their legacy names.

        Pure Python -- trigger P10 (L-11: the script is loaded from
        its file ``migrations/14.0.1.2.0/pre-migration.py``, which
        ``EVAL:`` cannot do). The old columns and the old table are
        created, the script renames them, and a second run, when the
        old names are gone, changes nothing.
        """
        cr = self.env.cr
        for column in ("primary_subconstruct_id", "secondary_subconstruct_id"):
            cr.execute(
                'ALTER TABLE %s ADD COLUMN "%s" integer' % (ARTIFACT_TABLE, column)
            )
        cr.execute(
            'CREATE TABLE "%s" (artifact_id integer, indicator_id integer)'
            % OLD_INDICATOR_TABLE
        )
        script = self._load_script("pre-migration.py")
        script.migrate(self.env.cr, "14.0.1.1.1")
        script.migrate(self.env.cr, "14.0.1.1.1")
        for column in ("primary_subconstruct_id", "secondary_subconstruct_id"):
            self.assertFalse(openupgrade.column_exists(cr, ARTIFACT_TABLE, column))
            self.assertTrue(
                openupgrade.column_exists(
                    cr, ARTIFACT_TABLE, openupgrade.get_legacy_name(column)
                )
            )
        self.assertFalse(openupgrade.table_exists(cr, OLD_INDICATOR_TABLE))
        self.assertTrue(
            openupgrade.table_exists(
                cr, openupgrade.get_legacy_name(OLD_INDICATOR_TABLE)
            )
        )
