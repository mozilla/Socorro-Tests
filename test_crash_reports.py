#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Crash Tests Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): David Burns
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import unittest2 as unittest
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
        page_title = csp.page_title
        self.assertTrue('Firefox' in page_title)
        self.assertTrue('Mozilla' in page_title)
        crash_adu = csp.select_report("Crashes per User")
        details = csp.current_details
        report_product = crash_adu.product_select
        self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        page_title = csp.page_title
        self.assertTrue('Thunderbird' in page_title)
        self.assertTrue('Mozilla' in page_title)
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_seamonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        page_title = csp.page_title
        self.assertTrue('SeaMonkey' in page_title)
        #Bug 576721 - Needs reenabled when fixed
        #self.assertTrue('Mozilla' not in page_title) 
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        page_title = csp.page_title
        self.assertTrue('Camino' in page_title)
        #Bug 576721 - Needs reenabled when fixed
        #self.assertTrue('Mozilla' not in page_title)
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            self.assertEqual(details['product'],report_product)

    def test_that_reports_form_has_same_product_for_fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        page_title = csp.page_title
        self.assertTrue('Fennec' in page_title)
        #Bug 576721 - Needs reenabled when fixed
        #self.assertTrue('Mozilla' not in page_title)
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            self.assertEqual(details['product'],report_product)

    def test_that_current_version_selected_in_top_crashers_header_for_firefox(self):
        self.skipTest("bug 637636 needs fixing")
        csp = CrashStatsHomePage(self.selenium)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        if not csp.can_find_text('no data'):
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])
    
    def test_that_current_version_selected_in_top_crashers_header_for_thunderbird(self):
        self.skipTest("bug 637636 needs fixing")
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_seamonkey(self):
        self.skipTest("bug 637636 needs fixing")    
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_camino(self):
        self.skipTest("bug 637636 needs fixing")    
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_fennec(self):
        self.skipTest("bug 637636 needs fixing")    
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_firefox(self):
        csp = CrashStatsHomePage(self.selenium)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by URL')
        self.assertEqual(details['product'], cstc.product_header)
        #Bug 611694 - Disabled till bug fixed
        #self.assertTrue(cstc.product_version_header in details['versions'])
    
    def test_that_current_version_selected_in_top_crashers_by_url_header_for_thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_seamonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_firefox(self):
        csp = CrashStatsHomePage(self.selenium)
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])
    
    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_seamonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            self.assertEqual(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #self.assertTrue(cstc.product_version_header in details['versions'])

if __name__ == "__main__":
    unittest.main()
