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
from vars import ConnectionParameters


class TestSmokeTests(unittest.TestCase):

    def setUp(self):
        self.selenium = selenium(ConnectionParameters.server, ConnectionParameters.port,
                    ConnectionParameters.browser, ConnectionParameters.baseurl)
        self.selenium.start()

    def tearDown(self):
        self.selenium.stop()

    def test_that_option_group_matches_visible_columns_for_firefox(self):
        csp = CrashStatsHomePage(self.selenium)
        self.assertTrue('Firefox' in csp.page_title)
        details = csp.current_details
        headers = []
        for i in details['versions']:
            headers.append(details['product'] + ' ' + i)

        if len(headers) > 0:
            self.assertEqual(headers[0], csp.right_column_heading)
        
            #Check the centre column
            centre = ''
            try:
                centre = csp.centre_column_heading
                self.assertEqual(centre, headers[1])
            except Exception, e:
                if len(headers) > 1:
                    self.fail(str(e))
                    
            #Check the right hand column
            right = ''
            try:
                right = csp.left_column_heading
                self.assertEqual(right, headers[2])
            except Exception, e:
                if len(headers) > 2:
                    self.fail(str(e))
            
    def test_that_option_group_matches_visible_columns_for_Thunderbird(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        self.assertTrue('Thunderbird' in csp.page_title)
        details = csp.current_details
        headers = []
        for i in details['versions']:
            headers.append(details['product'] + ' ' + i)

        if len(headers) > 0:
            self.assertEqual(headers[0], csp.right_column_heading)
    
            #Check the centre column
            centre = ''
            try:
                centre = csp.centre_column_heading
                self.assertEqual(centre, headers[1])
            except Exception, e:
                if len(headers) > 1:
                    self.fail(str(e))

            #Check the right hand column
            right = ''
            try:
                right = csp.left_column_heading
                self.assertEqual(right, headers[2])
            except Exception, e:
                if len(headers) > 2:
                    self.fail(str(e))

    def test_that_option_group_matches_visible_columns_for_Camino(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        self.assertTrue('Camino' in csp.page_title)
        details = csp.current_details
        headers = []
        for i in details['versions']:
            headers.append(details['product'] + ' ' + i)
        
        if len(headers) > 0:
            self.assertEqual(headers[0], csp.right_column_heading)
        
            #Check the centre column
            centre = ''
            try:
                centre = csp.centre_column_heading
                self.assertEqual(centre, headers[1])
            except Exception, e:
                if len(headers) > 1:
                    self.fail(str(e))
                
            #Check the right hand column
            right = ''
            try:
                right = csp.left_column_heading
                self.assertEqual(right, headers[2])
            except Exception, e:
                if len(headers) > 2:
                    self.fail(str(e))

    def test_that_option_group_matches_visible_columns_for_SeaMonkey(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        self.assertTrue('SeaMonkey' in csp.page_title)
        details = csp.current_details
        headers = []
        for i in details['versions']:
            headers.append(details['product'] + ' ' + i)

        if len(headers) > 0:
            self.assertEqual(headers[0], csp.right_column_heading)
    
            #Check the centre column
            centre = ''
            try:
                centre = csp.centre_column_heading
                self.assertEqual(centre, headers[1])
            except Exception, e:
                if len(headers) > 1:
                    self.fail(str(e))
                
            #Check the right hand column
            right = ''
            try:
                right = csp.left_column_heading
                self.assertEqual(right, headers[2])
            except Exception, e:
                if len(headers) > 2:
                    self.fail(str(e))

    def test_that_option_group_matches_visible_columns_for_Fennec(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        self.assertTrue('Fennec' in csp.page_title)
        details = csp.current_details
        headers = []
        for i in details['versions']:
            headers.append(details['product'] + ' ' + i)

        if len(headers) > 0:
            self.assertEqual(headers[0], csp.right_column_heading)
        
            #Check the centre column
            centre = ''
            try:
                centre = csp.centre_column_heading
                self.assertEqual(centre, headers[1])
            except Exception, e:
                if len(headers) > 1:
                    self.fail(str(e))
                
            #Check the right hand column
            right = ''
            try:
                right = csp.left_column_heading
                self.assertEqual(centre, headers[2])
            except Exception, e:
                if len(headers) > 2:
                    self.fail(str(e))

    def test_that_clicking_on_top_changers_updates(self):
        csp = CrashStatsHomePage(self.selenium)
        try:
            csp.click_on_top_('Changers')
        except Exception,e:
            self.fail(str(e))
        class_attr = csp.get_attribute('link=Top Changers','class')
        self.assertEqual("selected", class_attr)

    def test_that_server_status_page_loads(self):
        csp = CrashStatsHomePage(self.selenium)
        csstat = csp.click_server_status()
        try:
            csstat.at_a_glance()
        except Exception, e:
            self.fail(str(e))

        try:
            csstat.graphs()
        except Exception, e:
            self.fail(str(e))

        try:
            csstat.latest_raw_stats()
        except Exception, e:
            self.fail(str(e))

    def test_that_options_are_sorted_the_same(self):
        self.skipTest(" Bug 612679 - Disabled till bug fixed ")
        csp = CrashStatsHomePage(self.selenium)
        cssearch = csp.click_advanced_search()
        nav_product_list = csp.get_product_list
        search_product_list = cssearch.product_list
        self.assertEqual(len(nav_product_list),len(search_product_list))
        for i, prod_item in enumerate(nav_product_list):
            self.assertEqual(prod_item, search_product_list[i])

    def test_that_advanced_search_has_firefox_highlighted_in_multiselect(self):
        csp = CrashStatsHomePage(self.selenium)
        cs_advanced = csp.click_advanced_search()
        self.assertEqual('Firefox', cs_advanced.currently_selected_product)

    def test_that_advanced_search_has_thunderbird_highlighted_in_multiselect(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        cs_advanced = csp.click_advanced_search()
        self.assertEqual('Thunderbird', cs_advanced.currently_selected_product)
    
    def test_that_advanced_search_has_fennec_highlighted_in_multiselect(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        cs_advanced = csp.click_advanced_search()
        self.assertEqual('Fennec', cs_advanced.currently_selected_product)
    
    def test_that_advanced_search_has_camino_highlighted_in_multiselect(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        cs_advanced = csp.click_advanced_search()
        self.assertEqual('Camino', cs_advanced.currently_selected_product)

    def test_that_advanced_search_has_seamonkey_highlighted_in_multiselect(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        cs_advanced = csp.click_advanced_search()
        self.assertEqual('SeaMonkey', cs_advanced.currently_selected_product)

    def test_that_advanced_search_view_signature_for_firefox_crash(self):
        csp = CrashStatsHomePage(self.selenium)
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        if not cs_advanced.can_find_text('no data'):
            signature = cs_advanced.click_first_signature()
            self.assertTrue(signature in cs_advanced.page_heading)

    def test_that_advanced_search_view_signature_for_thunderbird_crash(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Thunderbird')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        if not cs_advanced.can_find_text('no data'):
            signature = cs_advanced.click_first_signature()
            self.assertTrue(signature in cs_advanced.page_heading)

    def test_that_advanced_search_view_signature_for_fennec_crash(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Fennec')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        if not cs_advanced.can_find_text('no data'):
            signature = cs_advanced.click_first_signature()
            self.assertTrue(signature in cs_advanced.page_heading)

    def test_that_advanced_search_view_signature_for_camino_crash(self):
        self.skipTest("Bug 630948 needs fixing")
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('Camino')
        cs_advanced = csp.click_advanced_search()
        cs_advanced.filter_reports()
        if not cs_advanced.can_find_text('no data'):
            signature = cs_advanced.click_first_signature()
            self.assertTrue(signature in cs_advanced.page_heading)

    def test_that_advanced_search_view_signature_for_seamonkey_crash(self):
        csp = CrashStatsHomePage(self.selenium)
        csp.select_product('SeaMonkey')
        if not csp.can_find_text('no data'):
            cs_advanced = csp.click_advanced_search()
            cs_advanced.filter_reports()
            if not cs_advanced.can_find_text('No Data'): 
                signature = cs_advanced.click_first_signature()
                self.assertTrue(signature in cs_advanced.page_heading)

    def test_that_simple_querystring_doesnt_return_500(self):
        csp = CrashStatsHomePage(self.selenium)
        try:
            csp.get_url_path('/query/simple')
            self.fail('Exception should have been thrown')
        except Exception, e:
            self.assertTrue('Response_Code = 404' in str(e))



if __name__ == "__main__":
    unittest.main()
