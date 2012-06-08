#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

from pages.base_page import CrashStatsBasePage
from pages.page import Page


class CrashStatsSignatureReport(CrashStatsBasePage):

    # https://crash-stats.allizom.org/report/list?

    _total_items_locator = (By.CSS_SELECTOR, 'span.totalItems')
    _reports_page_locator = (By.CSS_SELECTOR, '.ui-state-default.ui-corner-top:nth-of-type(4) > a > span')

    def click_reports(self):
        self.selenium.find_element(*self._reports_page_locator).click()

    @property
    def total_items_label(self):
        return self.selenium.find_element(*self._total_items_locator).text.replace(",", "")


class CrashStatsPerActiveDailyUser(CrashStatsBasePage):

    _page_title = 'Crashes per Active Daily User for Firefox'

    _product_select_locator = (By.ID, 'daily_search_version_form_products')
    _date_start_locator = (By.CSS_SELECTOR, '.daily_search_body .date[name="date_start"]')
    _generate_button_locator = (By.ID, 'daily_search_version_form_submit')
    _table_locator = (By.ID, 'crash_data')
    _row_table_locator = (By.CSS_SELECTOR, '#crash_data > tbody > tr')
    _last_row_date_locator = (By.CSS_SELECTOR, '#crash_data > tbody > tr > td:nth-child(1):not(:last):last')

    @property
    def product_select(self):
        element = self.selenium.find_element(*self._product_select_locator)
        select = Select(element)
        return select.first_selected_option.text

    def type_start_date(self, date):
        date_element = self.selenium.find_element(*self._date_start_locator)
        date_element.clear()
        date_element.send_keys(date)

    def click_generate_button(self):
        self.selenium.find_element(*self._generate_button_locator).click()

    @property
    def is_mixed_content_warning_shown(self):
        return self.is_alert_present()

    @property
    def is_table_visible(self):
        return self.is_element_visible(None, *self._table_locator)

    @property
    def table_row_count(self):
        return len(self.selenium.find_elements(self._row_table_locator))

    @property
    def last_row_date_value(self):
        return self.selenium.find_element(*self._last_row_date_locator).text


class CrashStatsTopCrashers(CrashStatsBasePage):

    _page_heading_product_locator = (By.ID, 'current-product')
    _page_heading_version_locator = (By.ID, 'current-version')

    _filter_by_locator = (By.CSS_SELECTOR, '.tc-duration-type.tc-filter > li > a')
    _filter_days_by_locator = (By.CSS_SELECTOR, '.tc-duration-days.tc-filter > li > a')
    _current_days_filter_locator = (By.CSS_SELECTOR, 'ul.tc-duration-days li a.selected')
    _current_filter_type_locator = (By.CSS_SELECTOR, 'ul.tc-duration-type li a.selected')

    _signature_table_row_locator = (By.CSS_SELECTOR, '#signatureList tbody tr')

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
    def signature_items(self):
        return [self.SignatureItem(self.testsetup, i) for i in self.selenium.find_elements(*self._signature_table_row_locator)]

    @property
    def valid_signature_items(self):
        return [self.SignatureItem(self.testsetup, i) for i in self.selenium.find_elements(*self._signature_table_row_locator) if i.text != 'empty signature']

    def click_first_valid_signature(self):
        return self.valid_signature_items[0].click()

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


class CrashStatsTopCrashersBySite(CrashStatsBasePage):

    _product_header_locator = (By.ID, 'tcburl-product')
    _product_version_header_locator = (By.ID, 'tcburl-version')

    @property
    def product_header(self):
        return self.selenium.find_element(*self._product_header_locator).text

    @property
    def product_version_header(self):
        return self.selenium.find_element(self._product_version_header_locator).text


class CrashStatsNightlyBuilds(CrashStatsBasePage):

    _link_to_ftp_locator = (By.CSS_SELECTOR, '.notitle > p > a')

    @property
    def link_to_ftp(self):
        return self.selenium.find_element(*self._link_to_ftp_locator).get_attribute('href')

    def click_link_to_ftp(self):
        self.selenium.find_element(*self._link_to_ftp_locator).click()


class CrashStatsTopChangers(CrashStatsBasePage):

    pass
