#!/usr/bin/env python
import unittest
from selenium import selenium
from crash_stats_page import CrashStatsHomePage
from crash_stats_page import CrashStatsSearchResults
from vars import ConnectionParameters


class TestSearchForIdOrSignature(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                    ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()

    def tearDown(self):
        self.selenium.stop()

    def test_that_when_item_not_available(self):
        csp = CrashStatsHomePage(self.selenium)
        results = csp.search_for_crash("this won't exist")
        self.assertTrue(results.can_find_text('No results were found.'))

    def test_that_search_for_valid_signature(self):
        '''
            This is a test for 
                https://bugzilla.mozilla.org/show_bug.cgi?id=609070
        '''
        csp = CrashStatsHomePage(self.selenium)
        result = csp.search_for_crash(csp.first_signature)
        self.assertFalse(result.can_find_text('No results were found.'))

    def test_that_advanced_search_for_firefox_can_be_filtered(self):
        csp = CrashStatsHomePage(self.selenium)
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        self.assertTrue(cs_advanced.can_find_text('product is one of Firefox'))

    def test_that_advanced_search_for_thunderbird_can_be_filtered(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        self.assertTrue(cs_advanced.can_find_text('product is one of Thunderbird'))

    def test_that_advanced_search_for_fennec_can_be_filtered(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        self.assertTrue(cs_advanced.can_find_text('product is one of Fennec'))

    def test_that_advanced_search_for_camino_can_be_filtered(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        self.assertTrue(cs_advanced.can_find_text('product is one of Camino'))
    
    def test_that_advanced_search_for_seamonkey_can_be_filtered(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        self.assertTrue(cs_advanced.can_find_text('product is one of SeaMonkey'))  

if __name__ == "__main__":
    unittest.main()
