#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pages.base_page import CrashStatsBasePage
from pages.page import Page


class CrashStatsTopCrashers(CrashStatsBasePage):

    _page_heading_product_locator = (By.ID, 'current-product')
    _page_heading_version_locator = (By.ID, 'current-version')

    _filter_by_locator = (By.CSS_SELECTOR, '.tc-duration-type.tc-filter > li > a')
    _filter_days_by_locator = (By.CSS_SELECTOR, '.tc-duration-days.tc-filter > li > a')
    _current_days_filter_locator = (By.CSS_SELECTOR, 'ul.tc-duration-days li a.selected')
    _current_filter_type_locator = (By.CSS_SELECTOR, 'ul.tc-duration-type li a.selected')

    _signature_table_row_locator = (By.CSS_SELECTOR, '#signatureList tbody tr')
    _empty_signature_title = 'empty signature'

    @property
    def page_heading_product(self):
        return self.selenium.find_element(*self._page_heading_product_locator).text

    @property
    def page_heading_version(self):
        return self.selenium.find_element(*self._page_heading_version_locator).text

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._signature_table_row_locator))

    @property
    def results_found(self):
        try:
            return self.results_count > 0
        except NoSuchElementException:
            return False

    def click_filter_by(self, option):
        for element in self.selenium.find_elements(*self._filter_by_locator):
            if element.text == option:
                element.click()
                return CrashStatsTopCrashers(self.testsetup)

    def click_filter_days_by(self, days):
        '''
            Click on the link with the amount of days you want to filter by
        '''
        for element in self.selenium.find_elements(*self._filter_days_by_locator):
            if element.text == days:
                element.click()
                return CrashStatsTopCrashers(self.testsetup)

    @property
    def current_days_filter(self):
        return self.selenium.find_element(*self._current_days_filter_locator).text

    @property
    def current_filter_type(self):
        return self.selenium.find_element(*self._current_filter_type_locator).text

    @property
    def current_days_filter(self):
        return self.selenium.find_element(*self._current_days_filter_locator).text

    @property
    def signature_items(self):
        return [self.SignatureItem(self.testsetup, i)
                    for i in self.selenium.find_elements(*self._signature_table_row_locator)]

    @property
    def valid_signature_items(self):
        return [self.SignatureItem(self.testsetup, i)
                    for i in self.selenium.find_elements(*self._signature_table_row_locator)
                        if i.text != self._empty_signature_title]

    def click_first_valid_signature(self):
        sigs = self.signature_items
        idx = 0
        # find the index of the first valid signature
        while idx < len(sigs) and sigs[idx].title == self._empty_signature_title:
            idx += 1
        # click on the valid signature, if one was found
        if idx < len(sigs) and sigs[idx].title != self._empty_signature_title:
            return sigs[idx].click()

    def click_first_signature(self):
        return self.signature_items[0].click()

    @property
    def first_valid_signature_title(self):
        return self.valid_signature_items[0].title

    class SignatureItem(Page):
        _signature_link_locator = (By.CSS_SELECTOR, 'a.signature')
        _browser_icon_locator = (By.CSS_SELECTOR, 'div img.browser')
        _plugin_icon_locator = (By.CSS_SELECTOR, 'div img.plugin')

        def __init__(self, testsetup, element):
                Page.__init__(self, testsetup)
                self._root_element = element

        def click(self):
            self._root_element.find_element(*self._signature_link_locator).click()
            from pages.crash_report_page import CrashReport
            return CrashReport(self.testsetup)

        @property
        def title(self):
            return self._root_element.find_element(*self._signature_link_locator).get_attribute('title')

        @property
        def is_plugin_icon_visible(self):
            return self.is_element_visible(self._root_element, *self._plugin_icon_locator)

        @property
        def is_browser_icon_visible(self):
            return self.is_element_visible(self._root_element, *self._browser_icon_locator)
