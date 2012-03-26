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

    _page_heading = (By.CSS_SELECTOR, 'div.page-heading > h2')
    _server_status_locator = (By.LINK_TEXT, ' Server Status')
    _link_to_bugzilla_locator = (By.CSS_SELECTOR, '.panel a')

    @property
    def page_title(self):
        WebDriverWait(self.selenium, 10).until(lambda s: self.selenium.title)
        return self.selenium.title

    @property
    def page_heading(self):
        return self.selenium.find_element(*self._page_heading).get_attribute('title')

    def get_attribute(self, element, attribute):
        return self.selenium.find_element(*element).get_attribute(attribute)

    def get_url_path(self, path):
        self.selenium.open(path)

    def click_server_status(self):
        self.selenium.find_element(*self._server_status_locator).click()
        from pages.crash_stats_page import CrashStatsStatus
        return CrashStatsStatus(self.testsetup)

    @property
    def link_to_bugzilla(self):
        return self.selenium.find_element(*self._link_to_bugzilla_locator).get_attribute('href')

    @property
    def header(self):
        return self.Header(self)

    class Header(Page):
        _find_crash_id_or_signature = (By.ID, 'q')
        _product_select_locator = (By.ID, 'products_select')
        _product_version_select = (By.ID, 'product_version_select')
        _current_versions_locator = (By.CSS_SELECTOR, '#product_version_select optgroup:nth-of-type(2) option')
        _other_versions_locator = (By.CSS_SELECTOR, '#product_version_select optgroup:nth-of-type(3) option')
        _report_select = (By.ID, 'report_select')

        _advanced_search_locator = (By.LINK_TEXT, 'Advanced Search')

        @property
        def current_product(self):
            element = self.selenium.find_element(*self._product_select_locator)
            select = Select(element)
            return select.first_selected_option.text

        @property
        def current_versions(self):
            from pages.version import FirefoxVersion
            current_versions = []
            for element in self.selenium.find_elements(*self._current_versions_locator):
                current_versions.append(FirefoxVersion(element.text))
            return current_versions

        @property
        def product_list(self):
            return self.selenium.find_elements(*self._product_select_locator)

        def select_product(self, application):
            '''
                Select the Mozilla Product you want to report on
            '''
            self.selenium.find_element(*self._product_select_locator).select_by_value(application)

        def select_version(self, version):
            '''
                Select the version of the application you want to report on
            '''
            version_dropdown = self.selenium.find_element(*self._product_version_select)
            select = Select(version_dropdown)
            select.select_by_visible_text(version)

        def select_report(self, report_name):
            '''
                Select the report type from the drop down
                and wait for the page to reload
            '''
            self.selenium.find_element(*self._report_select).select(report_name)
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
            serch_box = self.selenium.find_element(*self._find_crash_id_or_signature)
            serch_box.send_keys(crash_id_or_signature)
            serch_box.send_keys(Keys.RETURN)
            from pages.crash_stats_page import CrashStatsAdvancedSearch
            return CrashStatsAdvancedSearch(self.testsetup)
