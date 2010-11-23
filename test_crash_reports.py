#!/usr/bin/env python
import unittest
from selenium import selenium
from crash_stats_page import CrashStatsHomePage
from crash_stats_page import CrashStatsSearchResults
from crash_stats_page import CrashStatsPerActiveDailyUser
from vars import ConnectionParameters

class TestCrashReports(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                    ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()

    def tearDown(self):
        self.selenium.stop()
    
    def test_that_reports_form_has_same_product_for_firefox(self):
        csp = CrashStatsHomePage(self.selenium)
        crash_adu = csp.select_report("Crashes per User")
        page_title = csp.page_title
        self.assertTrue('Firefox' in page_title)
        self.assertTrue('Mozilla' in page_title)
        details = csp.current_details
        report_product = crash_adu.product_select
        self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        page_title = csp.page_title
        self.assertTrue('Thunderbird' in page_title)
        self.assertTrue('Mozilla' in page_title)
        crash_adu = csp.select_report("Crashes per User")
        details = csp.current_details
        report_product = crash_adu.product_select
        self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_seamonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        page_title = csp.page_title
        self.assertTrue('SeaMonkey' in page_title)
        self.assertTrue('Mozilla' not in page_title)
        crash_adu = csp.select_report("Crashes per User")
        details = csp.current_details
        report_product = crash_adu.product_select
        self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        page_title = csp.page_title
        self.assertTrue('Camino' in page_title)
        self.assertTrue('Mozilla' not in page_title)
        crash_adu = csp.select_report("Crashes per User")
        details = csp.current_details
        report_product = crash_adu.product_select
        self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        page_title = csp.page_title
        self.assertTrue('Fennec' in page_title)
        self.assertTrue('Mozilla' not in page_title)
        crash_adu = csp.select_report("Crashes per User")
        details = csp.current_details
        report_product = crash_adu.product_select
        self.assertEqual(details['product'],report_product)

    def test_that_current_version_selected_in_top_crashers_header_for_firefox(self):
        csp = CrashStatsHomePage(self.selenium)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])
    
    def test_that_current_version_selected_in_top_crashers_header_for_thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_seamonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_firefox(self):
        csp = CrashStatsHomePage(self.selenium)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by URL')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])
    
    def test_that_current_version_selected_in_top_crashers_by_url_header_for_thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by URL')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_seamonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by URL')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by URL')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by URL')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_firefox(self):
        csp = CrashStatsHomePage(self.selenium)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by Domain')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])
    
    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by Domain')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_seamonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by Domain')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by Domain')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by Domain')
        self.assertEqual(details['product'], cstc.product_header)
        self.assertTrue(cstc.product_version_header in details['versions'])

if __name__ == "__main__":
    unittest.main()
