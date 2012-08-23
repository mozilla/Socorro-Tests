#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from pages.page import Page


class CrashStatsBasePage(Page):

    _page_heading_locator = (By.CSS_SELECTOR, 'div.page-heading > h2')
    _server_status_locator = (By.LINK_TEXT, 'Server Status')
    _link_to_bugzilla_locator = (By.CSS_SELECTOR, '.panel a')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def page_heading(self):
        return self.selenium.find_element(*self._page_heading_locator).text

    def click_server_status(self):
        self.selenium.find_element(*self._server_status_locator).click()
        from pages.status_page import CrashStatsStatus
        return CrashStatsStatus(self.testsetup)

    def get_random_indexes(self, item_list, max_indexes, start=0, end=-1):
        """
            Return a list of random indexes for a list of items
            max_indexes is maximum # of indexes to return
            'start' is start of index range, defaults to zero
            'end' is end of index range, as used by range( ), defaults to length of item_list
        """
        import random
        if end < 0:
            end = len(item_list)
        return [ random.randrange(start, end) for _ in range(0, min(max_indexes, len(item_list))) ]

    @property
    def link_to_bugzilla(self):
        return self.selenium.find_element(*self._link_to_bugzilla_locator).get_attribute('href')

    @property
    def header(self):
        return self.Header(self.testsetup)

    class Header(Page):
        _find_crash_id_or_signature = (By.ID, 'q')
        _product_select_locator = (By.ID, 'products_select')
        _report_select_locator = (By.ID, 'report_select')
        _all_versions_locator = (By.ID, 'product_version_select')
        _current_versions_locator = (By.CSS_SELECTOR, 'optgroup:nth-of-type(2) option')
        _other_versions_locator = (By.CSS_SELECTOR, 'optgroup:nth-of-type(3) option')

        _advanced_search_locator = (By.LINK_TEXT, 'Advanced Search')

        @property
        def current_product(self):
            element = self.selenium.find_element(*self._product_select_locator)
            select = Select(element)
            return select.first_selected_option.text

        @property
        def current_version(self):
            element = self.selenium.find_element(*self._all_versions_locator)
            select = Select(element)
            return select.first_selected_option.text

        @property
        def current_versions(self):
            from pages.version import FirefoxVersion
            current_versions = []
            for element in self.selenium.find_element(*self._all_versions_locator).find_elements(*self._current_versions_locator):
                str(current_versions.append(FirefoxVersion(element.text)))
            return current_versions

        @property
        def other_versions(self):
            from pages.version import FirefoxVersion
            other_versions = []
            for element in self.selenium.find_element(*self._all_versions_locator).find_elements(*self._other_versions_locator):
                str(other_versions.append(FirefoxVersion(element.text)))
            return other_versions

        @property
        def current_report(self):
            element = self.selenium.find_element(*self._report_select_locator)
            select = Select(element)
            return select.first_selected_option.text

        @property
        def product_list(self):
            element = self.selenium.find_element(*self._product_select_locator)
            return [option.text for option in Select(element).options]

        def select_product(self, application):
            '''
                Select the Mozilla Product you want to report on
            '''
            element = self.selenium.find_element(*self._product_select_locator)
            select = Select(element)
            return select.select_by_visible_text(application)

        def select_version(self, version):
            '''
                Select the version of the application you want to report on
            '''
            version_dropdown = self.selenium.find_element(*self._all_versions_locator)
            select = Select(version_dropdown)
            select.select_by_visible_text(str(version))

        def select_report(self, report_name):
            '''
                Select the report type from the drop down
                and wait for the page to reload
            '''
            report_dropdown = self.selenium.find_element(*self._report_select_locator)
            select = Select(report_dropdown)
            select.select_by_visible_text(report_name)

            if 'Top Crashers' == report_name:
                self.wait_for_ajax()
                from pages.crash_stats_top_crashers_page import CrashStatsTopCrashers
                return CrashStatsTopCrashers(self.testsetup)
            elif 'Top Crashers by TopSite' == report_name:
                from pages.crash_stats_top_crashers_by_site_page import CrashStatsTopCrashersBySite
                return CrashStatsTopCrashersBySite(self.testsetup)
            elif 'Crashes per User' == report_name:
                from pages.crash_stats_per_active_daily_user_page import CrashStatsPerActiveDailyUser
                return CrashStatsPerActiveDailyUser(self.testsetup)
            elif 'Nightly Builds' == report_name:
                from pages.crash_stats_nightly_builds_page import CrashStatsNightlyBuilds
                return CrashStatsNightlyBuilds(self.testsetup)
            elif 'Top Changers' == report_name:
                from pages.crash_stats_top_changers_page import CrashStatsTopChangers
                return CrashStatsTopChangers(self.testsetup)

        def search_for_crash(self, crash_id_or_signature):
            '''
                Type the signature or the id of a bug into the search bar and submit the form
            '''
            search_box = self.selenium.find_element(*self._find_crash_id_or_signature)
            # explicitly only testing search and not the onfocus event which clears the
            # search field
            search_box.clear()
            search_box.send_keys(crash_id_or_signature)
            search_box.send_keys(Keys.RETURN)
            from pages.advanced_search_page import CrashStatsAdvancedSearch
            return CrashStatsAdvancedSearch(self.testsetup)

        def click_advanced_search(self):
            self.selenium.find_element(*self._advanced_search_locator).click()
            from pages.advanced_search_page import CrashStatsAdvancedSearch
            return CrashStatsAdvancedSearch(self.testsetup)
