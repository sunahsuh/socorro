# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from socorro.external.postgresql.crash import Crash
from socorro.lib import datetimeutil
import socorro.unittest.testlib.util as testutil

from unittestbase import PostgreSQLTestCase


#------------------------------------------------------------------------------
def setup_module():
    testutil.nosePrintModule(__file__)


#==============================================================================
class IntegrationTestCrash(PostgreSQLTestCase):
    """Test socorro.external.postgresql.crash.Crash class. """

    #--------------------------------------------------------------------------
    def setUp(self):
        """Set up this test class by populating the reports table with fake
        data. """
        super(IntegrationTestCrash, self).setUp()

        cursor = self.connection.cursor()

        # Insert data
        now = datetimeutil.utc_now()
        uuid = "%%s-%s" % now.strftime("%y%m%d")

        cursor.execute("""
            INSERT INTO reports 
            (id, date_processed, uuid, url, email, success, addons_checked)
            VALUES
            (
                1,
                '%s',
                '%s',
                'http://mywebsite.com',
                'test@something.com',
                TRUE,
                TRUE
            ),
            (
                2,
                '%s',
                '%s',
                'http://myotherwebsite.com',
                'admin@example.com',
                NULL,
                FALSE
            ),
            (
                3,
                '%s',
                '%s',
                'http://myotherwebsite.com',
                'admin@example.com',
                TRUE,
                FALSE
            );
        """ % (now, uuid % "a1", now, uuid % "a2", now, uuid % "b1"))

        cursor.execute("""
            INSERT INTO reports_duplicates
            ( uuid, duplicate_of, date_processed)
            VALUES
            (
                '%s',
                'a2',
                '%s'
            );
        """ % (uuid % "a1", now))

        self.connection.commit()

    #--------------------------------------------------------------------------
    def test_get(self):
        crash = Crash(config=self.config)
        now = datetimeutil.utc_now()
        uuid = "%%s-%s" % now.strftime("%y%m%d")

        #......................................................................
        # Test 1: a valid crash with duplicates
        params = {
            "uuid": uuid % "a1"
        }
        res = crash.get(**params)
        res_expected = {
            "hits": [
                {
                    "email": "test@something.com",
                    "url": "http://mywebsite.com",
                    "addons_checked": True,
                    "duplicate_of": "a2"
                }
            ],
            "total": 1
        }

        self.assertEqual(res, res_expected)

        #......................................................................
        # Test 2: an invalid crash
        params = {
            "uuid": uuid % "a4"
        }
        res = crash.get(**params)
        res_expected = {
            "hits": [],
            "total": 0
        }

        self.assertEqual(res, res_expected)

        #......................................................................
        # Test 3: a valid crash without duplicates
        params = {
            "uuid": uuid % "b1"
        }
        res = crash.get(**params)
        res_expected = {
            "hits": [
                {
                    "email": "admin@example.com",
                    "url": "http://myotherwebsite.com",
                    "addons_checked": False,
                    "duplicate_of": None
                }
            ],
            "total": 1
        }

        self.assertEqual(res, res_expected)

    #--------------------------------------------------------------------------
    def tearDown(self):
        """Clean up the database, delete tables and functions. """
        cursor = self.connection.cursor()
        cursor.execute("""
            TRUNCATE reports_duplicates, reports
            CASCADE
        """)
        self.connection.commit()
        super(IntegrationTestCrash, self).tearDown()
