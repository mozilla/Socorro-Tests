#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.page import Page


class CrashReport(Page):

    _reports_tab_locator = (By.ID, 'reports')
    _reports_loading_locator = (By.CSS_SELECTOR, '#reports p.loading-placeholder')
    _reports_row_locator = (By.CSS_SELECTOR, '#reportsList tbody tr')
    _report_tab_button_locator = (By.CSS_SELECTOR, '#report-list-nav li:nth-of-type(4) > a')

    @property
    def reports(self):
        return [self.Report(self.testsetup, element) for element in self.selenium.find_elements(*self._reports_row_locator)]

    def click_reports(self):
        self.selenium.find_element(*self._report_tab_button_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(None, *self._reports_tab_locator) and self.is_element_visible(None, *self._reports_loading_locator))

    class Report(Page):
        _product_locator = (By.CSS_SELECTOR, 'td:nth-of-type(3)')
        _version_locator = (By.CSS_SELECTOR, 'td:nth-of-type(4)')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def product(self):
            return self._root_element.find_element(*self._product_locator).text

        @property
        def version(self):
            return self._root_element.find_element(*self._version_locator).text
