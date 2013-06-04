#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

from pages.base_page import CrashStatsBasePage
from pages.page import Page


class CrashStatsAdvancedSearch(CrashStatsBasePage):
    """
    https://crash-stats.allizom.org/query/query
    This po covers both initial adv search page and also results
    """

    _page_title = 'Query Results - Mozilla Crash Reports'

    _multiple_product_select_locator = (By.ID, 'product')
    _multiple_version_select_locator = (By.ID, 'version')
    _multiple_os_select_locator = (By.ID, 'platform')
    _filter_crash_reports_button = (By.ID, 'query_submit')
    _query_results_text_locator = (By.CSS_SELECTOR, '.body.notitle > p:nth-child(1)')
    _no_results_text_locator = (By.CSS_SELECTOR, '.body.notitle > p:nth-child(2)')
    _range_value_locator = (By.ID, 'range_value')
    _range_unit_selector_locator = (By.ID, 'range_unit')
    _build_id_locator = (By.ID, 'build_id')
    _report_type_base_locator = (By.CSS_SELECTOR, '.advanced:nth-of-type(6)')
    _pagination_locator = (By.CSS_SELECTOR, 'div.pagination > a[href]')
    _next_locator = (By.CSS_SELECTOR, 'div.pagination a:last-child')
    _table_row_locator = (By.CSS_SELECTOR, '#signatureList > tbody > tr')

    def adv_select_product(self, product):
        element = self.selenium.find_element(*self._multiple_product_select_locator)
        select = Select(element)
        select.select_by_visible_text(product)

    def adv_select_version(self, version):
        element = self.selenium.find_element(*self._multiple_version_select_locator)
        # Before trying to select the option we'll try and find it.
        # If it doesn't exist we'll gladly take an exception. Se issue 3910
        element.find_element(By.XPATH, ".//option[normalize-space(.) = '%s']" % version)
        select = Select(element)
        select.select_by_visible_text(version)

    def adv_select_version_by_index(self, index):
        element = self.selenium.find_element(*self._multiple_version_select_locator)
        select = Select(element)
        select.select_by_index(index)

    def deselect_version(self):
        element = self.selenium.find_element(*self._multiple_version_select_locator)
        select = Select(element)
        select.deselect_all()

    def adv_select_os(self, os):
        element = self.selenium.find_element(*self._multiple_os_select_locator)
        select = Select(element)
        select.select_by_visible_text(os)

    def set_period_value_field_input(self, value):
        self.selenium.find_element(*self._range_value_locator).send_keys(value)

    def select_period_units(self, time_unit):
        element = self.selenium.find_element(*self._range_unit_selector_locator)
        select = Select(element)
        select.select_by_visible_text(time_unit)

    @property
    def product_list(self):
        element = self.selenium.find_element(*self._multiple_product_select_locator)
        return [option.text for option in Select(element).options]

    def click_filter_reports(self):
        self.selenium.find_element(*self._filter_crash_reports_button).click()
        self.wait_for_ajax()

    def click_first_signature(self):
        return self.results[0].click_signature()

    def build_id_field_input(self, value):
        self.selenium.find_element(*self._build_id_locator).send_keys(value)

    @property
    def build_id(self):
        return str(self.selenium.execute_script('return navigator.buildID'))

    @property
    def currently_selected_product(self):
        element = self.selenium.find_element(*self._multiple_product_select_locator)
        select = Select(element)
        return select.first_selected_option.text

    def select_report_process(self, lookup):
        input_element = self.selenium.find_element(By.XPATH, '//input[@name="process_type" and @value="%s"]' % lookup)
        input_element.click()

    def select_report_type(self, lookup):
        base = self.selenium.find_element(*self._report_type_base_locator)
        input_element = base.find_element(By.XPATH, "//label[normalize-space(text())='%s']/input" % lookup)
        input_element.click()

    @property
    def results_lead_in_text(self):
        return self.selenium.find_element(*self._query_results_text_locator).text

    @property
    def are_results_found(self):
        return len(self.results) > 0

    @property
    def no_results_text(self):
        return self.selenium.find_element(*self._no_results_text_locator).text

    def go_to_random_result_page(self):
        if self.is_element_visible(None, *self._pagination_locator):
            random.choice(self.selenium.find_elements(*self._pagination_locator)).click()

    def click_next(self):
        self.selenium.find_element(*self._next_locator).click()

    @property
    def is_next_visible(self):
        return self.is_element_visible(None, *self._next_locator)

    @property
    def results(self):
        return [self.Result(self.testsetup, row) for row in self.selenium.find_elements(*self._table_row_locator)]

    def random_results(self, count):
        results = self.results
        random_results = []
        for i in range(0, min(len(results), count)):
            random_results.append(random.choice(results))
        return random_results

    def top_results(self, count):
        results = self.results
        return results[:min(len(results), count)]

    @property
    def results_table_header(self):
        return self.ResultHeader(self.testsetup)

    class Result(Page):
        _columns_locator = (By.CSS_SELECTOR, 'td')
        _browser_icon_locator = (By.CSS_SELECTOR, 'div.signature-icons > img.browser')
        _plugin_icon_locator = (By.CSS_SELECTOR, 'div.signature-icons > img.plugin')
        _link_locator = (By.TAG_NAME, 'a')

        def __init__(self, testsetup, row):
            Page.__init__(self, testsetup)
            self._root_element = row

        @property
        def _columns(self):
            return self._root_element.find_elements(*self._columns_locator)

        @property
        def signature(self):
            return self._columns[1].text

        def click_signature(self):
            self._columns[1].find_element(*self._link_locator).click()
            from pages.signature_report_page import SignatureReport
            return SignatureReport(self.testsetup)

        @property
        def is_plugin_icon_visible(self):
            return self.is_element_visible(self._columns[1], *self._plugin_icon_locator)

        @property
        def is_browser_icon_visible(self):
            return self.is_element_visible(self._columns[1], *self._browser_icon_locator)

        @property
        def plugin_filename(self):
            return self._columns[2].text

        @property
        def number_of_crashes(self):
            return self._columns[-5].text

    class ResultHeader(Page):

        _root_locator = (By.CSS_SELECTOR, '#signatureList thead')
        _sort_by_filename_locator = (By.CSS_SELECTOR, "th:nth-child(3)")
        _sorted_column_locator = (By.CSS_SELECTOR, "th[class*='headerSort']")

        def __init__(self, testsetup):
            Page.__init__(self, testsetup)
            self._root_element = self.selenium.find_element(*self._root_locator)

        def click_sort_by_plugin_filename(self):
            self._root_element.find_element(*self._sort_by_filename_locator).click()

        @property
        def sort_order(self):
            return self._root_element.find_element(*self._sorted_column_locator).get_attribute('class').split()[1]

        @property
        def sorted_column(self):
            return self._root_element.find_element(*self._sorted_column_locator).text
