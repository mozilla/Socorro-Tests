#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import CrashStatsBasePage
from pages.page import Page


class CrashStatsSuperSearch(CrashStatsBasePage):

    _page_title = 'Search - Mozilla Crash Reports'

    # Search parameters section
    _field_text_locator = (By.CSS_SELECTOR, 'fieldset[id = "%s"] > div:nth-child(2) span')
    _operator_text_locator = (By.CSS_SELECTOR, 'fieldset[id = "%s"] > div:nth-child(4) span')
    _match_select_locator = (By.CSS_SELECTOR, 'fieldset[id="%s"] .select2-input')
    _match_text_locator = (By.CSS_SELECTOR, 'fieldset[id="%s"] > div:nth-child(6) div')
    _search_button_locator = (By.ID, 'search-button')
    _new_line_locator = (By.CSS_SELECTOR, '.new-line')
    _operator_test_locator = (By.CSS_SELECTOR, 'li[class*="highlighted"] > div')
    _input_locator = (By.CSS_SELECTOR, '#s2id_autogen6')
    _second_input_locator = (By.CSS_SELECTOR, '#s2id_autogen8')

    # More options section
    _more_options_locator = (By.CSS_SELECTOR, '.options h4')
    _facet_text_locator = (By.CSS_SELECTOR, '#s2id_autogen1 ul div')
    _delete_facet_locator = (By.CSS_SELECTOR, '#s2id_autogen1 ul a')
    _input_facet_locator = (By.CSS_SELECTOR, '#s2id_autogen1 ul input')
    _facet_name_suggestion_locator = (By.CSS_SELECTOR, '.select2-result-label')

    # Search results section
    _error_text_locator = (By.CSS_SELECTOR, '.errorlist li li')
    _results_facet_locator = (By.CSS_SELECTOR, '#search_results-nav li:nth-child(2) span')
    _column_list_locator = (By.CSS_SELECTOR, '#s2id_autogen3 ul li.select2-search-choice')
    _table_row_locator = (By.CSS_SELECTOR, '#reports-list tbody tr')
    _loader_locator = (By.CLASS_NAME, 'loader')
    _crash_reports_tab_locator = (By.CSS_SELECTOR, '#search_results-nav [href="#crash-reports"] span')

    def __init__(self, base_url, selenium):
        Page.__init__(self, base_url, selenium)
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.is_element_visible(None, *self._input_locator))

    def select_field(self, field):
        self.selenium.find_element(*self._input_locator).send_keys(field)
        self.selenium.find_element(*self._operator_test_locator).click()

    def select_operator(self, operator):
        self.selenium.find_element(*self._second_input_locator).send_keys(operator)
        self.selenium.find_element(*self._operator_test_locator).click()

    def select_match(self, line_id, match):
        _match_locator = (self._match_select_locator[0], self._match_select_locator[1] % line_id)
        self.selenium.find_element(*_match_locator).send_keys(match)
        self.selenium.find_element(*self._operator_test_locator).click()

    def field(self, line_id):
        return self.selenium.find_element(self._field_text_locator[0], self._field_text_locator[1] % line_id).text

    def operator(self, line_id):
        return self.selenium.find_element(self._operator_text_locator[0], self._operator_text_locator[1] % line_id).text

    def match(self, line_id):
        return self.selenium.find_element(self._match_text_locator[0], self._match_text_locator[1] % line_id).text

    def open_url(self, url):
        self.selenium.get(self.base_url + url)

    @property
    def error(self):
        return self.selenium.find_element(*self._error_text_locator).text

    def click_search(self):
        self.selenium.find_element(*self._search_button_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._loader_locator))

    def click_new_line(self):
        self.selenium.find_element(*self._new_line_locator).click()

    def click_more_options(self):
        self.selenium.find_element(*self._more_options_locator).click()

    def click_crash_reports_tab(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.find_element(*self._crash_reports_tab_locator).is_displayed())
        self.selenium.find_element(*self._crash_reports_tab_locator).click()

    @property
    def facet(self):
        return self.selenium.find_element(*self._facet_text_locator).text

    def type_facet(self, facet):
        self.selenium.find_element(*self._input_facet_locator).click()
        self.selenium.find_element(*self._input_facet_locator).send_keys(facet)
        self.selenium.find_element(*self._facet_name_suggestion_locator).click()

    def delete_facet(self):
        self.selenium.find_element(*self._delete_facet_locator).click()
        WebDriverWait(self.selenium, self.timeout).until(lambda s: not self.is_element_present(*self._delete_facet_locator))

    @property
    def search_results_table_header(self):
        return self.SearchResultHeader(self.base_url, self.selenium)

    @property
    def columns(self):
        return[self.Column(self.base_url, self.selenium, column) for column in self.selenium.find_elements(*self._column_list_locator)]

    @property
    def search_results(self):
        return [self.SearchResult(self.base_url, self.selenium, row) for row in self.selenium.find_elements(*self._table_row_locator)]

    @property
    def are_search_results_found(self):
        return len(self.search_results) > 0

    def wait_for_column_deleted(self, number_of_expected_columns):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: number_of_expected_columns == len(self.columns))

    def wait_for_facet_in_results(self, facet):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: facet.lower() in self.results_facet.lower())

    @property
    def results_facet(self):
        return self.selenium.find_element(*self._results_facet_locator).text

    def is_column_in_list(self, column_name):
        return column_name in [column.column_name for column in self.columns]

    class SearchResultHeader(Page):

        _table_header_name_locator = (By.CSS_SELECTOR, '#reports-list thead th')

        @property
        def table_column_names(self):
            return [table_column.text.lower() for table_column in self.selenium.find_elements(*self._table_header_name_locator)]

        def is_column_not_present(self, column_name):
            WebDriverWait(self.selenium, self.timeout).until(
                lambda s: column_name not in self.table_column_names, message='Column %s found in table header.' % column_name)
            return True

    class Column(Page):

        _column_name_locator = (By.CSS_SELECTOR, 'div')
        _column_delete_locator = (By.CSS_SELECTOR, 'a')

        def __init__(self, base_url, selenium, column):
            Page.__init__(self, base_url, selenium)
            self._root_element = column

        @property
        def column_name(self):
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self._root_element.find_element(*self._column_name_locator).is_displayed())
            return self._root_element.find_element(*self._column_name_locator).text

        def delete_column(self):
            self._root_element.find_element(*self._column_delete_locator).click()

    class SearchResult(Page):

        _columns_locator = (By.CSS_SELECTOR, 'td')

        def __init__(self, base_url, selenium, row):
            Page.__init__(self, base_url, selenium)
            self._root_element = row

        @property
        def _columns(self):
            return self._root_element.find_elements(*self._columns_locator)
