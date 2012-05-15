#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from pages.page import Page
from pages.base import CrashStatsBasePage
from selenium.webdriver.support.select import Select


class CrashStatsHomePage(CrashStatsBasePage):
    '''
        Page Object for Socorro
        https://crash-stats.allizom.org/
    '''
    _release_channels_locator = (By.CSS_SELECTOR, '.release_channel')

    def __init__(self, testsetup, product=None):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)

        if product is None:
            self.selenium.get(self.base_url)

    def click_first_product_top_crashers_link(self):
        return self.release_channels[0].click_top_crasher()

    @property
    def release_channels(self):
        return [self.ReleaseChannels(self.testsetup, element) for element in self.selenium.find_elements(*self._release_channels_locator)]

    class ReleaseChannels(CrashStatsBasePage):

        _release_channel_header_locator = (By.TAG_NAME, 'h4')
        _top_crashers_link_locator = (By.LINK_TEXT, 'Top Crashers')

        def __init__(self, testsetup, element):
            CrashStatsBasePage.__init__(self, testsetup)
            self._root_element = element

        @property
        def product_version_label(self):
            return self._root_element.find_element(*self._release_channel_header_locator).text

        def click_top_crasher(self):
            self._root_element.find_element(*self._top_crashers_link_locator).click()
            return CrashStatsTopCrashers(self.testsetup)


class CrashReport(Page):

    _reports_tab_locator = (By.ID, 'reports')
    _reports_row_locator = (By.CSS_SELECTOR, '#reportsList tbody tr')
    _report_tab_button_locator = (By.CSS_SELECTOR, '#report-list-nav li:nth-of-type(4) > a')

    @property
    def reports(self):
        return [self.Report(self.testsetup, element) for element in self.selenium.find_elements(*self._reports_row_locator)]

    def click_reports(self):
        self.selenium.find_element(*self._report_tab_button_locator).click()
        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_visible(None, *self._reports_tab_locator))

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


class CrashStatsAdvancedSearch(CrashStatsBasePage):
    #https://crash-stats.allizom.org/query/query
    # This po covers both initial adv search page and also results
    _page_title = 'Query Results - Mozilla Crash Reports'

    _product_multiple_select = (By.ID, 'product')
    _version_multiple_select = (By.ID, 'version')
    _os_multiple_select = (By.ID, 'platform')
    _filter_crash_reports_button = (By.ID, 'query_submit')
    _query_results_text = (By.CSS_SELECTOR, '.body.notitle > p:nth-child(1)')
    _no_results_text = (By.CSS_SELECTOR, '.body.notitle > p:nth-child(2)')
    _build_id_locator = (By.ID, 'build_id')
    _report_process_base_locator = (By.XPATH, "//p[span[preceding-sibling::span[text()='Report Process:']]]")
    _report_type_base_locator = (By.XPATH, "//p[span[preceding-sibling::span[text()='Report Type:']]]")

    _next_locator = (By.XPATH, "//div[@class='pagination']/a[contains(text(), 'Next')]")
    _table_row_locator = (By.CSS_SELECTOR, '#signatureList > tbody > tr')

    def adv_select_product(self, product):
        element = self.selenium.find_element(*self._product_multiple_select)
        select = Select(element)
        select.select_by_visible_text(product)

    def adv_select_version(self, version):
        element = self.selenium.find_element(*self._version_multiple_select)
        select = Select(element)
        select.select_by_value(version.replace(' ',':'))

    def deselect_version(self):
        element = self.selenium.find_element(*self._version_multiple_select)
        select = Select(element)
        select.deselect_all()

    def adv_select_os(self, os):
        element = self.selenium.find_element(*self._os_multiple_select)
        select = Select(element)
        select.select_by_visible_text(os)

    @property
    def product_list(self):
        element = self.selenium.find_element(*self._product_multiple_select)
        return [option.text for option in Select(element).options]

    def click_filter_reports(self):
        self.selenium.find_element(*self._filter_crash_reports_button).click()

    def click_first_signature(self):
        return self.results[0].click_signature()

    def build_id_field_input(self, value):
        self.selenium.find_element(*self._build_id_locator).send_keys(value)

    @property
    def build_id(self):
        return str(self.selenium.execute_script('navigator.buildID'))

    @property
    def currently_selected_product(self):
        element = self.selenium.find_element(*self._product_multiple_select)
        select = Select(element)
        return select.first_selected_option.text

    def select_report_process(self, lookup):
        base = self.selenium.find_element(*self._report_process_base_locator)
        input_element = base.find_element(By.XPATH, "//label[normalize-space(text())='%s']/input" % lookup)
        input_element.click()

    def select_report_type(self, lookup):
        base = self.selenium.find_element(*self._report_type_base_locator)
        input_element = base.find_element(By.XPATH, "//label[normalize-space(text())='%s']/input" % lookup)
        input_element.click()

    @property
    def results_lead_in_text(self):
        return self.selenium.find_element(*self._query_results_text).text

    @property
    def results_found(self):
        try:
            self.selenium.find_element(*self._table_row_locator)
            return True
        except NoSuchElementException:
            return False

    @property
    def no_results_text(self):
        return self.selenium.find_element(*self._no_results_text).text

    def click_next(self):
        self.selenium.find_element(*self._next_locator).click()

    @property
    def is_next_visible(self):
        return self.is_element_visible(None, *self._next_locator)

    @property
    def results(self):
        return [self.Result(self.testsetup, row) for row in self.selenium.find_elements(*self._table_row_locator)]

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
            return CrashStatsSignatureReport(self.testsetup)

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
            return self._columns[-4].text

    class ResultHeader(Page):

        _root_locator = (By.CSS_SELECTOR, '#signatureList thead')
        _sort_by_filename_locator = (By.XPATH, "//th[text()='Plugin Filename']")
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


class CrashStatsSignatureReport(CrashStatsBasePage):

    # https://crash-stats.allizom.org/report/list?

    _total_items = (By.CSS_SELECTOR, 'span.totalItems')
    _reports_page_locator = (By.CSS_SELECTOR, '.ui-state-default.ui-corner-top:nth-of-type(4) > a > span')

    def click_reports(self):
        self.selenium.find_element(*self._reports_page_locator).click()

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

    _data_table = (By.ID, 'signatureList')
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


class CrashStatsStatus(CrashStatsBasePage):

    _at_a_glance_locator = (By.CSS_SELECTOR, 'div.panel > div > table.server_status')
    _graphs_locator = (By.CSS_SELECTOR, 'div.panel > div > div.server-status-graph')
    _latest_raw_stats_locator = (By.CSS_SELECTOR, 'div.panel > div > table#server-stats-table')

    @property
    def is_at_a_glance_present(self):
        return self.is_element_visible(None, *self._at_a_glance_locator)

    @property
    def are_graphs_present(self):
        return len(self.selenium.find_elements(*self._graphs_locator)) == 4

    @property
    def is_latest_raw_stats_present(self):
        return self.is_element_visible(None, *self._latest_raw_stats_locator)


class ProductsLinksPage(CrashStatsBasePage):

    _heading_locator = (By.CSS_SELECTOR, '.title h2')

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.selenium.get(self.base_url + '/products/')

    @property
    def page_heading(self):
        return self.selenium.find_element(*self._heading_locator).text

    def click_product(self, product):
        self.selenium.find_element(By.LINK_TEXT, product).click()
        return CrashStatsHomePage(self.testsetup, product)


class CrashStatsTopChangers(CrashStatsBasePage):

    pass
