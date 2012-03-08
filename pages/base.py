#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.page import Page


class CrashStatsBasePage(Page):

    _page_heading = 'css=div.page-heading > h2'
    _server_status_locator = 'link=Server Status'
    _link_to_bugzilla = 'css=.panel a'

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

    def click_server_status(self):
        self.selenium.click(self._server_status_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        from pages.crash_stats_page import CrashStatsStatus
        return CrashStatsStatus(self.testsetup)

    @property
    def link_to_bugzilla(self):
        return self.selenium.get_attribute("%s@href" % self._link_to_bugzilla)

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
            from pages.version import FirefoxVersion
            current_versions = []
            for i in range(self.selenium.get_css_count(self._current_versions_locator)):
                current_versions.append(FirefoxVersion(self.selenium.get_text('%s:nth(%i)' % (self._current_versions_locator, i))))
            return current_versions

        @property
        def other_versions(self):
            from pages.version import FirefoxVersion
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
