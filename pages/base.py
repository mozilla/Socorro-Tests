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
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   David Burns
#   Teodosia Pop <teodosia.pop@softvision.ro>
#   Bebe <florin.strugariu@softvision.ro>
#   Dave Hunt <dhunt@mozilla.com>
#   Alin Trif <alin.trif@softvision.ro>
#   Zac Campbell
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

from pages.page import Page

class CrashStatsBasePage(Page):

    _page_heading = 'css=div.page-heading > h2'
    _server_status_locator = 'link=Server Status'

    @property
    def page_title(self):
        return self.selenium.get_title()

    @property
    def page_heading(self):
        self.wait_for_element_present(self._page_heading)
        return self.selenium.get_text(self._page_heading)

    def get_attribute(self, element, attribute):
        return self.selenium.get_attribute(element + '@' + attribute)

    def get_url_path(self, path):
        self.selenium.open(path)
    #
    #def select_product(self, application):
    #    '''
    #        Select the Mozilla Product you want to report on
    #    '''
    #    self.selenium.select(self._product_select, application)
    #    self.selenium.wait_for_page_to_load(self.timeout)
    #
    #def select_version(self, version):
    #    '''
    #        Select the version of the application you want to report on
    #    '''
    #    self.selenium.select(self._product_version_select, version)
    #    self.selenium.wait_for_page_to_load(self.timeout)
    #
    #def select_report(self, report_name):
    #    '''
    #        Select the report type from the drop down
    #        and wait for the page to reload
    #    '''
    #    self.selenium.select(self._report_select, report_name)
    #    self.selenium.wait_for_page_to_load(self.timeout)
    #    if 'Top Crashers' == report_name:
    #        from pages.crash_stats_page import CrashStatsTopCrashers
    #        return CrashStatsTopCrashers(self.testsetup)
    #    elif 'Top Crashers by Domain' == report_name:
    #        from pages.crash_stats_page import CrashStatsTopCrashersByDomain
    #        return CrashStatsTopCrashersByDomain(self.testsetup)
    #    elif 'Top Crashers by URL' == report_name:
    #        from pages.crash_stats_page import CrashStatsTopCrashersByUrl
    #        return CrashStatsTopCrashersByUrl(self.testsetup)
    #    elif 'Top Crashers by TopSite' == report_name:
    #        from pages.crash_stats_page import CrashStatsTopCrashersBySite
    #        return CrashStatsTopCrashersBySite(self.testsetup)
    #    elif 'Crashes per User' == report_name:
    #        from pages.crash_stats_page import CrashStatsPerActiveDailyUser
    #        return CrashStatsPerActiveDailyUser(self.testsetup)
    #    elif 'Nightly Builds' == report_name:
    #        from pages.crash_stats_page import CrashStatsNightlyBuilds
    #        return CrashStatsNightlyBuilds(self.testsetup)
    #    elif 'Top Changers' == report_name:
    #        from pages.crash_stats_page import CrashStatsTopChangers
    #        return CrashStatsTopChangers(self.testsetup)
    
    def click_server_status(self):
        self.selenium.click(self._server_status_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from pages.crash_stats_page import CrashStatsStatus
        return CrashStatsStatus(self.testsetup)
    
    #def click_advanced_search(self):
    #    self.selenium.click('link=Advanced Search')
    #    from pages.crash_stats_page import CrashStatsAdvancedSearch
    #    return CrashStatsAdvancedSearch(self.testsetup)
    #
    #def can_find_text(self, text_to_search):
    #    '''
    #        finds if text is available on a page.
    #    '''
    #    return self.selenium.is_text_present(text_to_search)
    #
    #@property
    #def current_details(self):
    #    details = {}
    #    details['product'] = self.selenium.get_selected_value(self._product_select)
    #    try:
    #        details['versions'] = self.selenium.get_text(
    #            'xpath=//select[@id="product_version_select"]/optgroup[2]').split(' ')
    #    except:
    #        details['versions'] = []
    #    return details
    
    
    @property
    def current_details(self):
        details = {}
        details['product'] = self.header.current_product
        try:
            details['versions'] = self.header.current_versions
        except:
            details['versions'] = []
        return details
    
    @property
    def header(self):
        return self.Header(self)
    
    class Header(Page):
        _find_crash_id_or_signature = 'id=q'
        _product_select = 'id=products_select'
        _product_version_select = 'id=product_version_select'
        _current_versions_locator = "css=#product_version_select optgroup:nth(1) option"
        _other_versions_locator = "css=#product_version_select optgroup:nth(2) option"
        _report_select = 'id=report_select'
        
        _advanced_search_locator = 'link=Advanced Search'
        
        @property
        def current_product(self):
            return self.selenium.get_selected_value(self._product_select)
        
        @property
        def current_versions(self):
            return self.selenium.get_text(self._current_versions_locator).split(' ')

        @property
        def current_versions(self):
            current_versions = []
            for i in range(self.selenium.get_css_count(self._current_versions_locator)):
                current_versions.append(FirefoxVersion(self.selenium.get_text('%s:nth(%i)' % (self._current_versions_locator, i))))
            return current_versions
    
        @property
        def other_versions(self):
            other_versions = []
            for i in range(self.selenium.get_css_count(self._other_versions_locator)):
                other_versions.append(FirefoxVersion(self.selenium.get_text('%s:nth(%i)' % (self._other_versions_locator, i))))
            return other_versions

        @property
        def product_list(self):
            return self.selenium.get_select_options(self._product_select)

        def select_product(self, application):
            '''
                Select the Mozilla Product you want to report on
            '''
            self.selenium.select(self._product_select, application)
            self.selenium.wait_for_page_to_load(self.timeout)
    
        def select_version(self, version):
            '''
                Select the version of the application you want to report on
            '''
            self.selenium.select(self._product_version_select, version)
            self.selenium.wait_for_page_to_load(self.timeout)
    
        def select_report(self, report_name):
            '''
                Select the report type from the drop down
                and wait for the page to reload
            '''
            self.selenium.select(self._report_select, report_name)
            self.selenium.wait_for_page_to_load(self.timeout)
            if 'Top Crashers' == report_name:
                from pages.crash_stats_page import CrashStatsTopCrashers
                return CrashStatsTopCrashers(self.testsetup)
            elif 'Top Crashers by Domain' == report_name:
                from pages.crash_stats_page import CrashStatsTopCrashersByDomain
                return CrashStatsTopCrashersByDomain(self.testsetup)
            elif 'Top Crashers by URL' == report_name:
                from pages.crash_stats_page import CrashStatsTopCrashersByUrl
                return CrashStatsTopCrashersByUrl(self.testsetup)
            elif 'Top Crashers by TopSite' == report_name:
                from pages.crash_stats_page import CrashStatsTopCrashersBySite
                return CrashStatsTopCrashersBySite(self.testsetup)
            elif 'Crashes per User' == report_name:
                from pages.crash_stats_page import CrashStatsPerActiveDailyUser
                return CrashStatsPerActiveDailyUser(self.testsetup)
            elif 'Nightly Builds' == report_name:
                from pages.crash_stats_page import CrashStatsNightlyBuilds
                return CrashStatsNightlyBuilds(self.testsetup)
            elif 'Top Changers' == report_name:
                from pages.crash_stats_page import CrashStatsTopChangers
                return CrashStatsTopChangers(self.testsetup)

        def search_for_crash(self, crash_id_or_signature):
            '''
                Type the signature or the id of a bug into the search bar and submit the form
            '''
            self.selenium.type(self._find_crash_id_or_signature, crash_id_or_signature)
            self.selenium.key_press(self._find_crash_id_or_signature, "\\13")
            self.selenium.wait_for_page_to_load(self.timeout)
            from pages.crash_stats_page import CrashStatsAdvancedSearch
            return CrashStatsAdvancedSearch(self.testsetup)

        def click_advanced_search(self):
            self.selenium.click(self._advanced_search_locator)
            from pages.crash_stats_page import CrashStatsAdvancedSearch
            return CrashStatsAdvancedSearch(self.testsetup)
