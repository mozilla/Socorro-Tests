#!/usr/bin/env python
import unittest
from selenium import selenium
from crash_stats_page import CrashStatsHomePage
from crash_stats_page import CrashStatsSearchResults
from vars import ConnectionParameters


class TestSpecificVersions(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                    ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()

    def tearDown(self):
        self.selenium.stop()

    def test_that_selecting_exact_version_doesnt_show_other_versions(self):
        csp = CrashStatsHomePage(self.selenium)
        details = csp.current_details
        if len(details['versions']) > 0:
            csp.select_version(details['versions'][1])
        
        self.assertEqual(details['product'] + ' ' + details['versions'][1],csp.right_column_heading)

        try:
            centre_name = csp.centre_column_heading
            self.fail(centre_name + ' was shown when it shouldnt be there')
        except Exception, e:
            pass

        try:
            right_name = csp.right_column_heading
            self.fail(right_name + ' was shown when it shouldnt be there')
        except Exception, e:
            pass




if __name__ == "__main__":
    unittest.main()
