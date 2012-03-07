#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.common.exceptions import NoSuchElementException
from pages.page import Page
from pages.base import CrashStatsBasePage
from version import FirefoxVersion


class CrashStatsHomePage(CrashStatsBasePage):
    '''
        Page Object for Socorro
        https://crash-stats.allizom.org/
    '''
    _first_product_top_crashers_link_locator = 'css=#release_channels .release_channel:first li:first a'
    _first_signature_locator = 'css=div.crash > p > a'
    _second_signature_locator = 'css=.crash:nth(2) > p > a'
    _top_crashers = 'css=a:contains("Top Crashers")'
    _top_changers = 'css=a:contains("Top Changers")'
    _top_crashers_selected = _top_crashers + '.selected'
    _top_changers_selected = _top_changers + '.selected'
    _heading_locator = "css=.page-heading h2"
    _results_table_rows = 'css=div.body table.tablesorter tbody > tr'

    def __init__(self, testsetup, product=None):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)

        if product is None:
            #self.selenium.open(self.base_url)
            self.selenium.open('/')
            self.selenium.wait_for_page_to_load(self.timeout)
            self.selenium.window_maximize()

    def report_length(self, days):
        '''
            Click on the link with the amount of days you want the report to be
        '''
        self.selenium.click('link=' + days + ' days')
        self.selenium.wait_for_page_to_load(self.timeout)
        self.wait_for_element_present('xpath=//a[text()="'
                                                + days + ' days" and @class="selected"]')

    def click_on_top_(self, element):
        topElement = 'link=Top ' + element
        self.selenium.click(topElement)
        if element == 'Changers':
            self.wait_for_element_visible(self._top_changers_selected)
        else:
            self.wait_for_element_visible(self._top_crashers_selected)

    def click_first_product_top_crashers_link(self):
        self.selenium.click(self._first_product_top_crashers_link_locator)
        self.selenium.wait_for_page_to_load(self.timeout)
        return CrashReportList(self.testsetup)

    @property
    def first_signature(self):
        return self.selenium.get_text(self._first_signature_locator)

    @property
    def get_page_name(self):
        return self.selenium.get_text(self._heading_locator)

    @property
    def top_crashers_count(self):
        return self.selenium.get_css_count(self._top_crashers)

    @property
    def top_crashers(self):
        return [self.CrashReportsRegion(self.testsetup, i) for i in range(self.top_crashers_count)]

    @property
    def top_crasher(self):
        return self.CrashReportsRegion(self.testsetup)

    def results_found(self):
        try:
            return self.selenium.get_css_count(self._results_table_rows) > 0
        except NoSuchElementException:
            return False

    class CrashReportsRegion(CrashStatsBasePage):

        _top_crashers = 'css=a:contains("Top Crashers")'
        _header_release_channel_locator = "css=.release_channel h4"

        def __init__(self, testsetup, lookup):
            CrashStatsBasePage.__init__(self, testsetup)
            self.lookup = lookup

        def absolute_locator(self, relative_locator):
            return self._root_locator

        @property
        def _root_locator(self):
            if type(self.lookup) == int:
                # lookup by index
                return "%s:nth(%s) " % (self._top_crashers, self.lookup)
            else:
                # lookup by name
                return "%s:contains(%s) " % (self._top_crashers, self.lookup)

        @property
        def version_name(self):
            return self.selenium.get_text("%s:nth(%s)" % (self._header_release_channel_locator, self.lookup))

        def click_top_crasher(self):
            self.selenium.click(self.absolute_locator(self._top_crashers))
            self.selenium.wait_for_page_to_load(self.timeout)
            return CrashStatsTopCrashers(self.testsetup)


class CrashReportList(CrashStatsBasePage):
    # https://crash-stats.allizom.org/topcrasher/byversion/Firefox/7.0a2/7/plugin

    _reports_list_locator = 'css=#signatureList tbody tr'
    _signature_locator = _reports_list_locator + ":nth-of-type(%s) td:nth-of-type(4) a"
    _signature_text_locator = _signature_locator + ".signature"

    _default_filter_type_locator = "css=ul.tc-duration-type li a.selected"
    _plugin_filter_locator = "css=ul.tc-duration-type li a:contains('Plugin')"

    _signature_table_locator = "css=#signatureList .signature"
    _first_signature_table_locator = "css=#signatureList .signature:nth(0)"
    _data_table = 'css=#signatureList'

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self._reports = [self.set_report(count) for count in range(1, self.reports_count)]

    def get_report(self, index):
        return self.reports[index]

    def set_report(self, index):
        signature = self.get_signature(index)
        return CrashReport(self.testsetup, index, signature)

    def get_signature(self, index):
        return self.selenium.get_text(self._signature_text_locator % index)

    def click_signature(self, index):
        report = self.reports[index]
        self.selenium.click(self._signature_locator % index)
        self.selenium.wait_for_page_to_load(self.timeout)
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
        return self.selenium.get_css_count(self._reports_list_locator)

    @property
    def first_report_with_valid_signature(self):
        return [report for report in self.reports if report.has_valid_signature][0]

    @property
    def get_default_filter_text(self):
        return self.selenium.get_text(self._default_filter_type_locator)

    def click_plugin_filter(self):
        self.selenium.click(self._plugin_filter_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def signature_list_count(self):
        return self.selenium.get_css_count(self._signature_table_locator)

    @property
    def signature_list_items(self):
        return [self.TableRegion(self.testsetup, i) for i in range(self.signature_list_count)]

    class TableRegion(Page):
        _data_table_signature_locator = 'css=table#signatureList > tbody > tr > td:nth-child(4)'
        _data_table_browser_icon_locator = _data_table_signature_locator + ' > div > img.browser'
        _data_table_plugin_icon_locator = _data_table_signature_locator + ' > div > img.plugin'

        def __init__(self, testsetup, lookup):
                Page.__init__(self, testsetup)
                self.lookup = lookup

        @property
        def is_plugin_icon_visible(self):
            return self.selenium.is_visible(self._data_table_plugin_icon_locator)

        @property
        def is_plugin_icon_present(self):
            return self.selenium.is_element_present(self._data_table_plugin_icon_locator)

        @property
        def is_browser_icon_visible(self):
            return self.selenium.is_visible(self._data_table_browser_icon_locator)

        @property
        def is_browser_icon_present(self):
            return self.selenium.is_element_present(self._data_table_browser_icon_locator)


class CrashReport(CrashStatsBasePage):

    _product_locator = " td:nth-of-type(3)"
    _version_locator = " td:nth-of-type(4)"
    _row_locator = "css=#reportsList tbody tr"

    def __init__(self, testsetup, index, signature=None):
        CrashStatsBasePage.__init__(self, testsetup)
        self.index = index
        self._signature = signature

    def absolute_locator(self, relative_locator):
        return self.root_locator + relative_locator

    @property
    def root_locator(self):
        return self._row_locator + ":nth-of-type(%s)" % (self._current_row_index)

    @property
    def row_index(self):
        return self.index

    @property
    def row_count(self):
        return self.selenium.get_css_count(self._row_locator)

    def get_row(self, index):
        self._current_row_index = index
        return self

    @property
    def signature(self):
        return self._signature

    @property
    def product(self):
        return self.selenium.get_text(self.absolute_locator(self._product_locator))

    @property
    def version(self):
        return self.selenium.get_text(self.absolute_locator(self._version_locator))

    @property
    def has_valid_signature(self):
        if self.signature == "(empty signature)":
            return False
        return True


class CrashStatsAdvancedSearch(CrashStatsBasePage):
    #https://crash-stats.allizom.org/query/query
    # This po covers both initial adv search page and also results

    _product_multiple_select = 'id=product'
    _version_multiple_select = 'id=version'
    _os_multiple_select = 'id=platform'
    _filter_crash_reports_button = 'id=query_submit'
    _data_table = 'css=#signatureList'
    _data_table_first_signature = 'css=table#signatureList > tbody > tr > td > a'
    _data_table_first_signature_results = 'css=table#signatureList > tbody > tr > td:nth-child(3)'

    _query_results_text = "css=.body.notitle"

    _query_results_text_no_results_locator = "css=.body.notitle:nth(0) p:nth(1)"

    _build_id_locator = "css=#build_id"

    _radio_items_locator = 'css=.radio-item > label > input'

    _data_table_signature_column_locator = 'css=table#signatureList > tbody > tr > td:nth-child(2)'
    _data_table_signature_browser_icon_locator = _data_table_signature_column_locator + ' > div > img.browser'
    _data_table_signature_plugin_icon_locator = _data_table_signature_column_locator + ' > div > img.plugin'
    _next_locator = 'css=.pagination>a:contains("Next")'
    _plugin_filename_header_locator = "css=table#signatureList > thead th:contains('Plugin Filename')"
    _page_title = 'Query Results - Mozilla Crash Reports'

    def __init__(self, testsetup):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)
        self.wait_for_element_present(self._product_multiple_select)

    def adv_select_product(self, product):
        self.selenium.select(self._product_multiple_select, product)

    def adv_select_version(self, version):
        self.selenium.select(self._version_multiple_select, version)

    def adv_select_os(self, os):
        self.selenium.select(self._os_multiple_select, os)

    def filter_reports(self):
        self.selenium.click(self._filter_crash_reports_button)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_first_signature(self):
        self.wait_for_element_present(self._data_table_first_signature)
        self.selenium.click(self._data_table_first_signature)
        self.selenium.wait_for_page_to_load(self.timeout)
        return CrashStatsSignatureReport(self.testsetup)

    def build_id_field_input(self, value):
        self.selenium.type(self._build_id_locator, value)

    @property
    def build_id(self):
        return self.selenium.get_eval("navigator.buildID")

    @property
    def first_signature_name(self):
        return self.selenium.get_text(self._data_table_first_signature)

    @property
    def first_signature_number_of_results(self):
        return self.selenium.get_text(self._data_table_first_signature_results)

    @property
    def currently_selected_product(self):
        return self.selenium.get_selected_value(self._product_multiple_select)

    @property
    def product_list(self):
        return self.selenium.get_select_options(self._product_multiple_select)

    @property
    def results_found(self):
        try:
            return self.selenium.get_css_count("%s > tbody > tr" % self._data_table) > 0
        except NoSuchElementException:
            return False

    @property
    def results_count(self):
        try:
            return self.selenium.get_css_count("%s > tbody > tr" % self._data_table)
        except NoSuchElementException:
            return 0

    def query_results_text(self, lookup):
        return self.selenium.get_text(self._query_results_text + ":nth(%s)" % lookup)

    @property
    def query_results_text_no_results(self):
        return self.selenium.get_text(self._query_results_text_no_results_locator)

    def select_radio_button(self, lookup):
        self.selenium.check(self._radio_items_locator + ":nth(%s)" % lookup)

    @property
    def is_plugin_icon_visible(self):
        return self.selenium.is_visible(self._data_table_signature_plugin_icon_locator)

    @property
    def is_plugin_icon_present(self):
        return self.selenium.is_element_present(self._data_table_signature_plugin_icon_locator)

    @property
    def is_browser_icon_visible(self):
        return self.selenium.is_visible(self._data_table_signature_browser_icon_locator)

    @property
    def is_browser_icon_present(self):
        return self.selenium.is_element_present(self._data_table_signature_browser_icon_locator)

    def click_next(self):
        self.selenium.click(self._next_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_plugin_filename_header(self):
        self.selenium.click(self._plugin_filename_header_locator)

    def plugin_filename_results_list(self):
        # TODO remove lower() pending resolution of: https://github.com/AutomatedTester/unittest-zero/issues/9
        return [(self.selenium.get_text('%s tr:nth(%s) > td:nth-child(3)' % (self._data_table, (i + 1)))).lower() for i in range(0, self.results_count)]


class CrashStatsSignatureReport(CrashStatsBasePage):

    # https://crash-stats.allizom.org/report/list?

    _total_items = "css=span.totalItems"

    @property
    def total_items_label(self):
        return self.selenium.get_text(self._total_items).replace(",", "")


class CrashStatsPerActiveDailyUser(CrashStatsBasePage):

    _product_select = 'id=daily_search_version_form_products'
    _date_start_locator = 'css=.daily_search_body .date[name="date_start"]'
    _generate_button_locator = "id=daily_search_version_form_submit"
    _table_locator = "id=crash_data"
    _row_table_locator = "css=#crash_data > tbody > tr"
    _page_title = 'Crashes per Active Daily User for Firefox'

    @property
    def product_select(self):
        return self.selenium.get_selected_value(self._product_select)

    def type_start_date(self, date):
        self.selenium.type(self._date_start_locator, date)

    def click_generate_button(self):
        self.selenium.click(self._generate_button_locator)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def is_mixed_content_warning_shown(self):
        return self.selenium.is_alert_present()

    @property
    def is_table_visible(self):
        return self.selenium.is_visible(self._table_locator)

    @property
    def table_row_count(self):
        return self.selenium.get_css_count(self._row_table_locator)

    @property
    def last_row_date_value(self):
        return self.selenium.get_text('css=#crash_data > tbody > tr:nth(%s) > td:nth(0)' % (int(self.table_row_count) - 2))


class CrashStatsTopCrashers(CrashStatsBasePage):

    _product_header = 'id=current-product'
    _product_version_header = 'id=current-version'

    _filter_all = "link=All"
    _filter_browser = "link=Browser"
    _filter_plugin = "link=Plugin"

    _result_rows = "css=table#signatureList > tbody > tr"
    _current_days_filter_locator = "css=ul.tc-duration-days li a.selected"

    @property
    def product_header(self):
        return self.selenium.get_text(self._product_header)

    @property
    def product_version_header(self):
        return self.selenium.get_text(self._product_version_header)

    @property
    def count_results(self):
        return self.selenium.get_css_count(self._result_rows)

    def click_filter_all(self):
        self.selenium.click(self._filter_all)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_filter_browser(self):
        self.selenium.click(self._filter_browser)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_filter_plugin(self):
        self.selenium.click(self._filter_plugin)
        self.selenium.wait_for_page_to_load(self.timeout)

    def click_filter_days(self, days):
        '''
            Click on the link with the amount of days you want to filter by
        '''
        self.selenium.click('link=' + days)
        self.selenium.wait_for_page_to_load(self.timeout)

    @property
    def table_results_found(self):
        try:
            return self.selenium.get_css_count(self._result_rows) > 0
        except NoSuchElementException:
            return False

    @property
    def current_days_filter(self):
        return self.selenium.get_text(self._current_days_filter_locator)


class CrashStatsTopCrashersBySite(CrashStatsBasePage):

    _product_header = 'id=tcburl-product'
    _product_version_header = 'id=tcburl-version'

    @property
    def product_header(self):
        return self.selenium.get_text(self._product_header)

    @property
    def product_version_header(self):
        return self.selenium.get_text(self._product_version_header)


class CrashStatsNightlyBuilds(CrashStatsBasePage):

    _link_to_ftp_locator = 'css=.notitle > p > a'

    @property
    def product_header(self):
        return self.selenium.get_text(self._page_heading)

    @property
    def link_to_ftp(self):
        return self.selenium.get_attribute("%s@href" % self._link_to_ftp_locator)

    def click_link_to_ftp(self):
        self.selenium.click(self._link_to_ftp_locator)
        self.selenium.wait_for_page_to_load(self.timeout)


class CrashStatsStatus(CrashStatsBasePage):

    _at_a_glance_locator = 'css=div.panel > div > table.server_status'
    _graphs_locator = 'css=div.panel > div > div.server-status-graph'
    _latest_raw_stats = 'css=div.panel > div > table#server-stats-table'

    def is_at_a_glance_present(self):
        return self.selenium.is_element_present(self._at_a_glance_locator)

    def are_graphs_present(self):
        return self.selenium.get_css_count(self._graphs_locator) == 4

    def is_latest_raw_stats_present(self):
        return self.selenium.is_element_present(self._latest_raw_stats)


class ProductsLinksPage(CrashStatsBasePage):

    _root_locator = "css=.body li"
    _name_page_locator = 'css=#mainbody h2'

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.selenium.open('/products/')
        self.selenium.wait_for_page_to_load(self.timeout)
        self.selenium.window_maximize()

    @property
    def get_products_page_name(self):
        return self.selenium.get_text(self._name_page_locator)

    def click_product(self, product):
        self.selenium.click('%s:contains(%s) a' % (self._root_locator, product))
        self.selenium.wait_for_page_to_load(self.timeout)
        return CrashStatsHomePage(self.testsetup, product)


class CrashStatsTopChangers(CrashStatsBasePage):

    _report_locator = 'id=report_select'

    @property
    def is_top_changers_highlighted(self):
        selected_report = self.selenium.get_selected_label(self._report_locator)
        return (selected_report == 'Top Changers')
