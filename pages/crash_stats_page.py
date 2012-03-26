#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from pages.page import Page
from pages.base import CrashStatsBasePage
from selenium.webdriver.support.select import Select


class CrashStatsHomePage(CrashStatsBasePage):
    '''
        Page Object for Socorro
        https://crash-stats.allizom.org/
    '''
    _first_product_top_crashers_link_locator = (By.CSS_SELECTOR, '#release_channels .release_channel:first li:first a')
    _first_signature_locator = (By.CSS_SELECTOR, 'div.crash > p > a')
    _second_signature_locator = (By.CSS_SELECTOR, '.crash:nth-of-type(3) > p > a')
    _top_crashers_locator = (By.CSS_SELECTOR, 'a:contains("Top Crashers")')
    _top_changers_locator = (By.CSS_SELECTOR, 'a:contains("Top Changers")')
    _top_selected_locator = (By.CSS_SELECTOR, '.selected')
    _heading_locator = (By.CSS_SELECTOR, '.page-heading h2')
    _results_table_rows = (By.CSS_SELECTOR, 'div.body table.tablesorter tbody > tr')

    def __init__(self, testsetup, product=None):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)

        if product is None:
            #self.selenium.open(self.base_url)
            self.selenium.get(self.base_url)

    def report_length(self, days):
        '''
            Click on the link with the amount of days you want the report to be
        '''
        self.selenium.find_element(*getattr(self, 'link= %s days') % days).click()

    def click_on_top_(self, element):
        topElement = self.selenium.find_element(*getattr(self, 'link=Top %s' % element))
        topElement.click()
        if element == 'Changers':
            self.find_element(*self._top_changers_locator).find_element(*self._top_selected_locator).is_displayed()
        else:
            self.find_element(*self._top_crashers_locator).find_element(*self._top_selected_locator).is_displayed()

    def click_first_product_top_crashers_link(self):
        self.selenium.find_element(*self._first_product_top_crashers_link_locator).click()
        return CrashReportList(self.testsetup)

    @property
    def first_signature(self):
        return self.selenium.find_element(*self._first_signature_locator).text

    @property
    def get_page_name(self):
        return self.selenium.find_element(*self._heading_locator).text

    @property
    def top_crashers_count(self):
        return len(self.selenium.find_elements(*self._top_crashers))

    @property
    def top_crashers(self):
        return [self.CrashReportsRegion(self.testsetup, i) for i in range(self.top_crashers_count)]

    @property
    def top_crasher(self):
        return self.CrashReportsRegion(self.testsetup)

    def results_found(self):
        try:
            return len(self.selenium.find_elements(*self._results_table_rows)) > 0
        except NoSuchElementException:
            return False

    class CrashReportsRegion(CrashStatsBasePage):

        _top_crashers_locator = (By.CSS_SELECTOR, 'a:contains("Top Crashers")')
        _header_release_channel_locator = (By.CSS_SELECTOR, '.release_channel h4')

        def __init__(self, testsetup, element):
            CrashStatsBasePage.__init__(self, testsetup)
            self._root_element = element

        @property
        def version_name(self):
            return self._root_element.find_element(*self._header_release_channel_locator).text

        def click_top_crasher(self):
            self._root_element.find_element(*self._top_crashers_locator).click()
            return CrashStatsTopCrashers(self.testsetup)


class CrashReportList(CrashStatsBasePage):
    # https://crash-stats.allizom.org/topcrasher/byversion/Firefox/7.0a2/7/plugin

    _reports_list_locator = (By.CSS_SELECTOR, '#signatureList tbody tr')
    _signature_locator = (By.CSS_SELECTOR, 'td:nth-of-type(4) a')
    _signature_text_locator = (By.CSS_SELECTOR, '.signature')

    _default_filter_type_locator = (By.CSS_SELECTOR, 'ul.tc-duration-type li a.selected')
    _plugin_filter_locator = (By.CSS_SELECTOR, 'ul.tc-duration-type li a:contains("Plugin")')

    _signature_table_locator = (By.CSS_SELECTOR, '#signatureList .signature')
    _first_signature_table_locator = (By.CSS_SELECTOR, 'tr:nth-child(1) a.signature')
    _data_table = (By.CSS_SELECTOR, '#signatureList')

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self._reports = [self.set_report(count) for count in range(1, self.reports_count)]

    def get_report(self, index):
        return self.reports[index]

    def set_report(self, index):
        signature = self.get_signature(index)
        return CrashReport(self.testsetup, index, signature)

    def get_signature(self, index):
        return self.selenium.find_element(self._signature_locator[0],
                        ':nth-of-type(%s) ' % (self._signature_text_locator[1], index + 1)).text

    def click_signature(self, index):
        report = self.reports[index]
        return self.selenium.find_element(self._signature_locator[0],
                        ':nth-of-type(%s) ' % (self._signature_text_locator[1], index + 1)).click
        return report

    def click_first_valid_signature(self):
        return self.click_signature(self.first_report_with_valid_signature.row_index)

    @property
    def first_valid_signature(self):
        return self.get_signature(self.first_report_with_valid_signature.row_index)

    @property
    def reports(self):
        return self._reports

    @property
    def reports_count(self):
        return len(self.selenium.find_elements(*self._reports_list_locator))

    @property
    def first_report_with_valid_signature(self):
        return [report for report in self.reports if report.has_valid_signature][0]

    @property
    def get_default_filter_text(self):
        return self.selenium.find_element(*self._default_filter_type_locator).text

    def click_plugin_filter(self):
        self.selenium.find_element(*self._plugin_filter_locator).click

    @property
    def signature_list_count(self):
        return len(self.selenium.find_elements(self._signature_table_locator))

    @property
    def signature_list_items(self):
        return [self.TableRegion(self.testsetup, i) for i in range(self.signature_list_count)]

    class TableRegion(Page):
        _data_table_signature_locator = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr > td:nth-child(4)')
        _data_table_browser_icon_locator = (By.CSS_SELECTOR, ' > div > img.browser')
        _data_table_plugin_icon_locator = (By.CSS_SELECTOR, ' > div > img.plugin')

        def __init__(self, testsetup, element):
                Page.__init__(self, testsetup)
                self.element = element

        @property
        def is_plugin_icon_visible(self):
            return self.selenium.find_element(*self._data_table_signature_locator).find_element(*self._data_table_plugin_icon_locator).is_displayed()

        @property
        def is_browser_icon_visible(self):
            return self.selenium.find_element(*self._data_table_signature_locator).find_element(*self._data_table_browser_icon_locator).is_displayed()


#class CrashReport(CrashStatsBasePage):
#
#    _product_locator = (By.CSS_SELECTOR, ' td:nth-of-type(3)')
#    _version_locator = (By.CSS_SELECTOR, ' td:nth-of-type(4)')
#    _row_locator = (By.CSS_SELECTOR, 'reportsList tbody tr')
#
#    def __init__(self, testsetup, index, signature=None):
#        CrashStatsBasePage.__init__(self, testsetup)
#        self.index = index
#        self._signature = signature
#
#    def absolute_locator(self, relative_locator):
#        return self.root_locator + relative_locator
#
#    @property
#    def root_locator(self):
#        return self.selenium.
#        return self._row_locator + ':nth-of-type(%s)' % (self._current_row_index)
#
#    @property
#    def row_index(self):
#        return self.index
#
#    @property
#    def row_count(self):
#        return len(self.selenium.find_elements(*self._row_locator))
#
#    def get_row(self, index):
#        self._current_row_index = index
#        return self
#
#    @property
#    def signature(self):
#        return self._signature
#
#    @property
#    def product(self):
#        return self.selenium.get_text(self.absolute_locator(self._product_locator))
#
#    @property
#    def version(self):
#        return self.selenium.get_text(self.absolute_locator(self._version_locator))
#
#    @property
#    def has_valid_signature(self):
#        if self.signature == '(empty signature)':
#            return False
#        return True


class CrashStatsAdvancedSearch(CrashStatsBasePage):
    #https://crash-stats.allizom.org/query/query
    # This po covers both initial adv search page and also results
    _page_title = 'Query Results - Mozilla Crash Reports'

    _product_multiple_select = (By.ID, 'product')
    _version_multiple_select = (By.ID, 'version')
    _os_multiple_select = (By.ID, 'platform')
    _filter_crash_reports_button = (By.ID, 'query_submit')
    _data_table = (By.CSS_SELECTOR, '#signatureList')
    _data_table_first_signature = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr > td > a')
    _data_table_first_signature_results = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr > td:nth-child(3)')

    _query_results_text = (By.CSS_SELECTOR, '.body.notitle')

    _query_results_text_no_results_locator = (By.CSS_SELECTOR, '.body.notitle > p:nth-of-type(2)')

    _build_id_locator = (By.ID, 'build_id')

    _radio_items_locator = (By.CSS_SELECTOR, 'radio-item > label > input')

    _data_table_signature_column_locator = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr > td:nth-child(2)')
    _data_table_signature_browser_icon_locator = (By.CSS_SELECTOR, ' > div > img.browser')
    _data_table_signature_plugin_icon_locator = (By.CSS_SELECTOR, ' > div > img.plugin')
    _next_locator = (By.CSS_SELECTOR, '.pagination>a:contains("Next")')
    _plugin_filename_header_locator = (By.CSS_SELECTOR, 'table#signatureList > thead th:contains("Plugin Filename")')

    def __init__(self, testsetup):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)

    def adv_select_product(self, product):
        self.selenium.find_element(*self._product_multiple_select).select(product)

    def adv_select_version(self, version):
        self.selenium.find_element(*self._version_multiple_select).select(version)

    def adv_select_os(self, os):
        self.selenium.find_element(*self._os_multiple_select).select(os)

    def filter_reports(self):
        self.selenium.find_element(*self._filter_crash_reports_button).click()

    def click_first_signature(self):
        WebDriverWait(self.selenium, 10).until(lambda s: not self.is_element_present(*self._data_table_first_signature))
        self.selenium.find_element(*self._data_table_first_signature).click()
        return CrashStatsSignatureReport(self.testsetup)

    def build_id_field_input(self, value):
        self.selenium.find_element(*self._build_id_locator).send_keys(value)

    @property
    def build_id(self):
        return self.selenium.execute_script('navigator.buildID')

    @property
    def first_signature_name(self):
        return self.selenium.find_element(*self._data_table_first_signature).text

    @property
    def first_signature_number_of_results(self):
        return self.selenium.find_element(*self._data_table_first_signature_results).text

    @property
    def currently_selected_product(self):
        element = self.selenium.find_element(*self._product_multiple_select)
        select = Select(element)
        return select.all_selected_options

    @property
    def product_list(self):
        return [element.text for element in self.selenium.find_elements(*self._product_multiple_select)]

    @property
    def results_found(self):
        try:
            return len(self.selenium.find_element(self._data_table).find_elements(By.CSS_SELECTOR, '> tbody > tr')) > 0
        except NoSuchElementException:
            return False

    @property
    def results_count(self):
        try:
            return len(self.selenium.find_element(self._data_table).find_elements(By.CSS_SELECTOR, '> tbody > tr'))
        except NoSuchElementException:
            return 0

    def query_results_text(self, lookup):
        return self.selenium.get_text(self._query_results_text + ':nth(%s)' % lookup)

    @property
    def query_results_text_no_results(self):
        return self.selenium.find_element(*self._query_results_text_no_results_locator).text

    def select_radio_button(self, lookup):
        self.selenium.check(self._radio_items_locator + ':nth(%s)' % lookup)

    @property
    def is_plugin_icon_visible(self):
        return self.selenium.find_element(*self._data_table_signature_column_locator).find_element(*self._data_table_signature_plugin_icon_locator)

    @property
    def is_browser_icon_visible(self):
        return self.selenium.find_element(*self._data_table_signature_column_locator).find_element(*self._data_table_signature_browser_icon_locator)

    def click_next(self):
        self.selenium.find_element(*self._next_locator).click()

    def click_plugin_filename_header(self):
        self.selenium.find_element(*self._plugin_filename_header_locator).click()

    def plugin_filename_results_list(self):
        # TODO remove lower() pending resolution of: https://github.com/AutomatedTester/unittest-zero/issues/9
        return [(self.selenium.get_text('%s tr:nth(%s) > td:nth-child(3)' % (self._data_table, (i + 1)))).lower() for i in range(0, self.results_count)]


class CrashStatsSignatureReport(CrashStatsBasePage):

    # https://crash-stats.allizom.org/report/list?

    _total_items = (By.CSS_SELECTOR, 'span.totalItems')

    @property
    def total_items_label(self):
        return self.selenium.find_element(*self._total_items).text.replace(",", "")


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
        return select.all_selected_options

    def type_start_date(self, date):
        self.selenium.find_element(*self._date_start_locator).send_keys(date)

    def click_generate_button(self):
        self.selenium.find_element(self._generate_button_locator).click()

    @property
    def is_mixed_content_warning_shown(self):
        return self.selenium.is_alert_present()

    @property
    def is_table_visible(self):
        return self.selenium.find_element(*self._table_locator).is_diplayed

    @property
    def table_row_count(self):
        return len(self.selenium.find_elements(self._row_table_locator))

    @property
    def last_row_date_value(self):
        return self.selenium.find_element(*self._last_row_date_locator).text


class CrashStatsTopCrashers(CrashStatsBasePage):

    _product_header_locator = (By.ID, 'current-product')
    _product_version_header_locator = (By.ID, 'current-version')

    _filter_all_locator = (By.LINK_TEXT, 'All')
    _filter_browser_locator = (By.LINK_TEXT, 'Browser')
    _filter_plugin_locator = (By.LINK_TEXT, 'Plugin')

    _result_rows_locator = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr')
    _current_days_filter_locator = (By.CSS_SELECTOR, 'ul.tc-duration-days li a.selected')

    @property
    def product_header(self):
        return self.selenium.find_element(*self._product_header_locator).text

    @property
    def product_version_header(self):
        return self.selenium.find_element(*self._product_version_header_locator)

    @property
    def count_results(self):
        return len(self.selenium.find_elements(*self._result_rows_locator))

    def click_filter_all(self):
        self.selenium.find_element(*self._filter_all_locator).click()

    def click_filter_browser(self):
        self.selenium.find_element(self._filter_browser_locator).click()

    def click_filter_plugin(self):
        self.selenium.find_element(*self._filter_plugin_locator).click()

    def click_filter_days(self, days):
        '''
            Click on the link with the amount of days you want to filter by
        '''
        self.selenium.find_element(By.LINK_TEXT, days)


    @property
    def table_results_found(self):
        try:
            return len(self.selenium.find_elements(self._result_rows)) > 0
        except NoSuchElementException:
            return False

    @property
    def current_days_filter(self):
        return self.selenium.find_element(self._current_days_filter_locator).text


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
    def product_header(self):
        return self.selenium.find_element(*self._page_heading).text

    @property
    def link_to_ftp(self):
        return self.selenium.find_element(*self._link_to_ftp_locator).get_attribute('href')

    def click_link_to_ftp(self):
        self.selenium.find_element(*self._link_to_ftp_locator).click()


class CrashStatsStatus(CrashStatsBasePage):

    _at_a_glance_locator = (By.CSS_SELECTOR, 'div.panel > div > table.server_status')
    _graphs_locator = (By.CSS_SELECTOR, 'div.panel > div > div.server-status-graph')
    _latest_raw_stats_locator = (By.CSS_SELECTOR, 'div.panel > div > table#server-stats-table')

    def is_at_a_glance_present(self):
        return self.is_element_present(*self._at_a_glance_locator)

    def are_graphs_present(self):
        return len(self.selenium.find_elements(self._graphs_locator)) == 4

    def is_latest_raw_stats_present(self):
        return self.is_element_present(*self._latest_raw_stats_locator)


class ProductsLinksPage(CrashStatsBasePage):

    _root_locator = (By.CSS_SELECTOR, '.body li')
    _name_page_locator = (By.CSS_SELECTOR, '#mainbody h2')

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.selenium.get('/products/')

    @property
    def get_products_page_name(self):
        return self.selenium.find_element(self._name_page_locator).text

    def click_product(self, product):
        self.selenium.find_element(self._root_locator[0], '%s:contains(%s) a' % (self._root_locator, product)).click()
        return CrashStatsHomePage(self.testsetup, product)


class CrashStatsTopChangers(CrashStatsBasePage):

    _report_locator = (By.ID, 'report_select')

    @property
    def is_top_changers_highlighted(self):
        report = self.selenium.find_element(*self._report_locator)
        selected_report = Select(report)
        return (selected_report.all_selected_options == 'Top Changers')
