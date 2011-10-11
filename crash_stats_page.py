#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Crash Tests Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   David Burns
#   Teodosia Pop <teodosia.pop@softvision.ro>
#   Bebe <florin.strugariu@softvision.ro>
#   Dave Hunt <dhunt@mozilla.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from selenium import selenium
from selenium.common.exceptions import NoSuchElementException
import re
import time
import base64
from page import Page
from version import FirefoxVersion


class CrashStatsBasePage(Page):

    _page_heading = 'css=div.page-heading > h2'

    def __init__(self, testsetup):
        Page.__init__(self, testsetup)
        self.sel = self.selenium

    @property
    def page_title(self):
        return self.sel.get_title()

    @property
    def page_heading(self):
        self.wait_for_element_present(self._page_heading)
        return self.sel.get_text(self._page_heading)

    def get_attribute(self, element, attribute):
        return self.sel.get_attribute(element + '@' + attribute)

    def get_url_path(self, path):
        self.sel.open(path)

    def select_product(self, application):
        '''
            Select the Mozilla Product you want to report on
        '''
        self.sel.select(self._product_select, application)
        self.sel.wait_for_page_to_load(self.timeout)

    def select_version(self, version):
        '''
            Select the version of the application you want to report on
        '''
        self.sel.select(self._product_version_select, version)
        self.sel.wait_for_page_to_load(self.timeout)

    def select_report(self, report_name):
        '''
            Select the report type from the drop down
            and wait for the page to reload
        '''
        self.sel.select(self._report_select, report_name)
        self.sel.wait_for_page_to_load(self.timeout)
        if 'Top Crashers' == report_name:
            return CrashStatsTopCrashers(self.testsetup)
        elif 'Top Crashers by Domain' == report_name:
            return CrashStatsTopCrashersByDomain(self.testsetup)
        elif 'Top Crashers by URL' == report_name:
            return CrashStatsTopCrashersByUrl(self.testsetup)
        elif 'Top Crashers by TopSite' == report_name:
            return CrashStatsTopCrashersBySite(self.testsetup)
        elif 'Crashes per User' == report_name:
            return CrashStatsPerActiveDailyUser(self.testsetup)
        elif 'Top Changers' == report_name:
            return CrashStatsTopChangers(self.testsetup)

    def click_server_status(self):
        self.sel.click('link=Server Status')
        self.sel.wait_for_page_to_load(self.timeout)
        return CrashStatsStatus(self.testsetup)

    def click_advanced_search(self):
        self.sel.click('link=Advanced Search')
        return CrashStatsAdvancedSearch(self.testsetup)

    def can_find_text(self, text_to_search):
        '''
            finds if text is available on a page.
        '''
        return self.sel.is_text_present(text_to_search)

    @property
    def current_details(self):
        details = {}
        details['product'] = self.sel.get_selected_value(self._product_select)
        try:
            details['versions'] = self.sel.get_text(
                'xpath=//select[@id="product_version_select"]/optgroup[2]').split(' ')
        except:
            details['versions'] = []
        return details


class CrashStatsHomePage(CrashStatsBasePage):
    '''
        Page Object for Socorro
        https://crash-stats.allizom.org/
    '''
    _find_crash_id_or_signature = 'id=q'
    _product_select = 'id=products_select'
    _product_version_select = 'id=product_version_select'
    _current_versions_locator = "css=#product_version_select optgroup:nth(1) option"
    _other_versions_locator = "css=#product_version_select optgroup:nth(2) option"
    _report_select = 'id=report_select'
    _first_product_top_crashers_link_locator = 'css=#release_channels .release_channel:first li:first a'
    _first_signature_locator = 'css=div.crash > p > a'
    _second_signature_locator = 'css=.crash:nth(2) > p > a'
    _top_crashers = 'css=a:contains("Top Crashers")'
    _top_changers = 'css=a:contains("Top Changers")'
    _top_crashers_selected = _top_crashers + '.selected'
    _top_changers_selected = _top_changers + '.selected'
    _results_table_rows = 'css=div.body table.tablesorter tbody > tr'

    def __init__(self, testsetup):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)
        self.sel.open('/')
        count = 0
        while not re.search(r'http?\w://.*/products/.*', self.sel.get_location(), re.U):
            time.sleep(1)
            count += 1
            if count == 20:
                raise Exception("Home Page has not loaded")

        if not self.sel.get_title() == 'Crash Data for Firefox':
            self.sel.select(self._product_select, 'Firefox')
            self.sel.wait_for_page_to_load(self.timeout)
        self.sel.window_maximize()

    def report_length(self, days):
        '''
            Click on the link with the amount of days you want the report to be
        '''
        self.sel.click('link=' + days + ' days')
        self.sel.wait_for_page_to_load(self.timeout)
        self.wait_for_element_present('xpath=//a[text()="'
                                                + days + ' days" and @class="selected"]')

    def search_for_crash(self, crash_id_or_signature):
        '''
            Type the signature or the id of a bug into the search bar and submit the form
        '''
        self.sel.type(self._find_crash_id_or_signature, crash_id_or_signature)
        self.sel.key_press(self._find_crash_id_or_signature, "\\13")
        self.sel.wait_for_page_to_load(self.timeout)
        return CrashStatsAdvancedSearch(self.testsetup)

    def click_on_top_(self, element):
        topElement = 'link=Top ' + element
        self.sel.click(topElement)
        if element == 'Changers':
            self.wait_for_element_visible(self._top_changers_selected)
        else:
            self.wait_for_element_visible(self._top_crashers_selected)

    def click_first_product_top_crashers_link(self):
        self.sel.click(self._first_product_top_crashers_link_locator)
        self.sel.wait_for_page_to_load(self.timeout)
        return CrashReportList(self.testsetup)

    @property
    def product_list(self):
        return self.sel.get_select_options(self._product_select)

    @property
    def current_versions(self):
        current_versions = []
        for i in range(self.selenium.get_css_count(self._current_versions_locator)):
            current_versions.append(FirefoxVersion(self.selenium.get_text('%s:nth(%i)' % (self._current_versions_locator, i))))
        return current_versions

    @property
    def other_versions(self):
        other_versions = []
        for i in range(self.selenium.get_css_count(self._other_versions_locator)):
            other_versions.append(FirefoxVersion(self.selenium.get_text('%s:nth(%i)' % (self._other_versions_locator, i))))
        return other_versions

    @property
    def first_signature(self):
        return self.sel.get_text(self._first_signature_locator)

    @property
    def top_crashers_count(self):
        return self.sel.get_css_count(self._top_crashers)

    @property
    def top_crashers(self):
        return [self.CrashReportsRegion(self.testsetup, i) for i in range(self.top_crashers_count)]

    @property
    def top_crasher(self):
        return self.CrashReportsRegion(self.testsetup)

    def results_found(self):
        try:
            return self.sel.get_css_count(self._results_table_rows) > 0
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

        @property
        def version_name(self):
            return self.sel.get_text("%s:nth(%s)" % (self._header_release_channel_locator, self.lookup))

        def click_top_crasher(self):
            self.selenium.click(self.absolute_locator(self._top_crashers))
            self.selenium.wait_for_page_to_load(self.timeout)
            return CrashStatsTopCrashers(self.testsetup)


class CrashReportList(CrashStatsBasePage):
    # https://crash-stats.allizom.org/topcrasher/byversion/Firefox/7.0a2/7/plugin

    _reports_list_locator = 'css=#signatureList tbody tr'
    _signature_locator = _reports_list_locator + ":nth-of-type(%s) td:nth-of-type(5) a"
    _signature_text_locator = _signature_locator + " span"

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self._reports = [self.set_report(count) for count in range(1, self.reports_count)]

    def get_report(self, index):
        return self.reports[index]

    def set_report(self, index):
        signature = self.get_signature(index)
        return CrashReport(self.testsetup, index, signature)

    def get_signature(self, index):
        return self.sel.get_text(self._signature_text_locator % index)

    def click_signature(self, index):
        report = self.reports[index]
        self.sel.click(self._signature_locator % index)
        self.sel.wait_for_page_to_load(self.timeout)
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
        return self.sel.get_css_count(self._reports_list_locator)

    @property
    def first_report_with_valid_signature(self):
        return [report for report in self.reports if report.has_valid_signature][0]


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
        return self.sel.get_css_count(self._row_locator)

    def get_row(self, index):
        self._current_row_index = index
        return self

    @property
    def signature(self):
        return self._signature

    @property
    def product(self):
        return self.sel.get_text(self.absolute_locator(self._product_locator))

    @property
    def version(self):
        return self.sel.get_text(self.absolute_locator(self._version_locator))

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

    _query_results_text = "css=.body.notitle > p:nth(0)"

    _build_id_field = "css=#build_id"

    def __init__(self, testsetup):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)
        self.wait_for_element_present(self._product_multiple_select)

    def adv_select_product(self, product):
        self.sel.select(self._product_multiple_select, product)

    def adv_select_version(self, version):
        self.sel.select(self._version_multiple_select, version)

    def adv_select_os(self, os):
        self.sel.select(self._os_multiple_select, os)

    def filter_reports(self):
        self.sel.click(self._filter_crash_reports_button)
        self.sel.wait_for_page_to_load(self.timeout)

    def click_first_signature(self):
        self.wait_for_element_present(self._data_table_first_signature)
        self.sel.click(self._data_table_first_signature)
        self.sel.wait_for_page_to_load(self.timeout)
        return CrashStatsSignatureReport(self.testsetup)

    def build_id_field_input(self, var):
        return self.sel.type(self._build_id_field, var)

    @property
    def first_signature_name(self):
        return self.sel.get_text(self._data_table_first_signature)

    @property
    def first_signature_number_of_results(self):
        return self.sel.get_text(self._data_table_first_signature_results)

    @property
    def currently_selected_product(self):
        return self.sel.get_selected_value(self._product_multiple_select)

    @property
    def product_list(self):
        return self.sel.get_select_options(self._product_multiple_select)

    @property
    def results_found(self):
        try:
            return self.sel.get_css_count("%s > tbody > tr" % self._data_table) > 0
        except NoSuchElementException:
            return False

    @property
    def query_results_text(self):
        return self.sel.get_text(self._query_results_text)


class CrashStatsSignatureReport(CrashStatsBasePage):

    # https://crash-stats.allizom.org/report/list?

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.sel = testsetup.selenium
        CrashStatsBasePage.__init__(self, testsetup)

    _total_items = "css=span.totalItems"

    @property
    def total_items_label(self):
        return self.sel.get_text(self._total_items).replace(",", "")


class CrashStatsPerActiveDailyUser(CrashStatsBasePage):

    _product_select = 'id=daily_search_version_form_products'

    def __init__(self, testsetup):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        self.sel = testsetup.selenium

    @property
    def product_select(self):
        return self.sel.get_selected_value(self._product_select)


class CrashStatsTopCrashers(CrashStatsBasePage):

    _product_header = 'css=h2 > span.current-product'
    _product_version_header = 'css=h2 > span.current-version'

    _filter_all = "link=All"
    _filter_browser = "link=Browser"
    _filter_plugin = "link=Plugin"

    _result_rows = "css=table#signatureList > tbody > tr"

    def __init__(self, testsetup):
        self.sel = testsetup.selenium
        CrashStatsBasePage.__init__(self, testsetup)

    @property
    def product_header(self):
        return self.sel.get_text(self._product_header)

    @property
    def product_version_header(self):
        return self.sel.get_text(self._product_version_header)

    @property
    def count_results(self):
        return self.sel.get_css_count(self._result_rows)

    def click_filter_all(self):
        self.sel.click(self._filter_all)
        self.sel.wait_for_page_to_load(self.timeout)

    def click_filter_browser(self):
        self.sel.click(self._filter_browser)
        self.sel.wait_for_page_to_load(self.timeout)

    def click_filter_plugin(self):
        self.sel.click(self._filter_plugin)
        self.sel.wait_for_page_to_load(self.timeout)


class CrashStatsTopCrashersByUrl(CrashStatsBasePage):

    _product_header = 'id=tcburl-product'
    _product_version_header = 'id=tcburl-version'

    def __init__(self, testsetup):
        self.sel = testsetup.selenium

    @property
    def product_header(self):
        return self.sel.get_text(self._product_header)

    @property
    def product_version_header(self):
        return self.sel.get_text(self._product_version_header)


class CrashStatsTopCrashersByDomain(CrashStatsBasePage):

    _product_header = 'id=tcburl-product'
    _product_version_header = 'id=tcburl-version'

    def __init__(self, testsetup):
        self.sel = testsetup.selenium

    @property
    def product_header(self):
        return self.sel.get_text(self._product_header)

    @property
    def product_version_header(self):
        return self.sel.get_text(self._product_version_header)


class CrashStatsTopCrashersBySite(CrashStatsBasePage):

    _product_header = 'id=tcburl-product'
    _product_version_header = 'id=tcburl-version'

    def __init__(self, testsetup):
        self.sel = testsetup.selenium

    @property
    def product_header(self):
        return self.sel.get_text(self._product_header)

    @property
    def product_version_header(self):
        return self.sel.get_text(self._product_version_header)


class CrashStatsStatus(CrashStatsBasePage):

    _page_header = 'css=h2:contains("Server Status")'
    _at_a_glance_locator = 'css=div.title:contains("At a Glance")'
    _graphs_locator = 'css=div.title:contains("Graphs")'
    _latest_raw_stats = 'css=div.title:contains("Latest Raw Stats")'

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.sel = testsetup.selenium
        self.wait_for_element_present(self._page_header)

    def at_a_glance(self):
        if not self.sel.is_element_present(self._at_a_glance_locator):
            raise Exception(self._at_a_glance_locator + ' is not available')

    def graphs(self):
        if not self.sel.is_element_present(self._graphs_locator):
            raise Exception(self._graphs_locator + ' is not available')

    def latest_raw_stats(self):
        if not self.sel.is_element_present(self._graphs_locator):
            raise Exception(self._latest_raw_stats + ' is not available')


class CrashStatsTopChangers(CrashStatsBasePage):

    _report_locator = 'id=report_select'

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.sel = testsetup.selenium

    @property
    def is_top_changers_highlighted(self):
        selected_report = self.sel.get_selected_label(self._report_locator)
        return (selected_report == 'Top Changers')
