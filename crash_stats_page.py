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
# Contributor(s): David Burns
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
import re
import time
import base64
from page import Page


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

    def wait_for_element_present(self, element):
        count = 0
        while not self.sel.is_element_present(element):
            time.sleep(1)
            count += 1
            if count == 20:
                self.record_error()
                raise Exception(element + ' has not loaded')

    def wait_for_element_visible(self, element):
        self.wait_for_element_present(element)
        count = 0
        while not self.sel.is_visible(element):
            time.sleep(1)
            count += 1
            if count == 20:
                self.record_error()
                raise Exception(element + " is still visible")

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

    def record_error(self):
        '''

        '''
        print '-------------------'
        print 'Error at ' + self.sel.get_location()
        print 'Page title ' + self.sel.get_title()
        print '-------------------'
        filename = 'socorro_' + str(time.time()).split('.')[0] + '.png'

        print 'Screenshot of error in file ' + filename
        f = open(filename, 'wb')
        f.write(base64.decodestring(
            self.sel.capture_entire_page_screenshot_to_string('')))
        f.close()


class CrashStatsHomePage(CrashStatsBasePage):
    '''
        Page Object for Socorro
    '''
    _find_crash_id_or_signature = 'id=q'
    _product_select = 'id=products_select'
    _product_version_select = 'id=product_version_select'
    _report_select = 'id=report_select'
    _first_product_top_crashers_link_locator = 'css=#release_channels .release_channel:first li:first a'
    _first_signature_locator = 'css=div.crash > p > a'
    _second_signature_locator = 'css=.crash:nth(2) > p > a'
    _right_column_locator = 'css=div.product_topcrasher > h4'
    _centre_column_locator = 'css=div.product_topcrasher + div > h4'
    _left_column_locator = 'css=div.product_topcrasher + div + div > h4'
    _top_crashers = 'css=a:contains("Top Crashers")'
    _top_changers = 'css=a:contains("Top Changers")'
    _top_crashers_selected = _top_crashers + '.selected'
    _top_changers_selected = _top_changers + '.selected'


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
                self.record_error()
                raise Exception("Home Page has not loaded")

        if not self.sel.get_title() == 'Crash Data for Firefox':
            self.sel.select(self.product_select, 'Firefox')
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
        #self.sel.submit('//form')
        self.sel.wait_for_page_to_load(self.timeout)
        return CrashStatsSearchResults(self.testsetup)

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

    def get_report(self, index):
        return CrashReport(self.testsetup, count)

    @property
    def first_non_null_signature(self):
        count = 1
        while CrashReport(self.testsetup, count).has_empty_signature:
            count += 1
        return CrashReport(self.testsetup, count).signature

    @property
    def get_product_list(self):
        return self.sel.get_select_options(self._product_select)

    @property
    def first_signature(self):
        return self.sel.get_text(self._first_signature_locator)

    @property
    def second_signature(self):
        return self.sel.get_text(self._second_signature_locator)

    @property
    def right_column_heading(self):
        return self.sel.get_text(self._right_column_locator)[:-9]

    @property
    def centre_column_heading(self):
        return self.sel.get_text(self._centre_column_locator)[:-9]

    @property
    def left_column_heading(self):
        return self.sel.get_text(self._left_column_locator)[:-9]


class CrashReport(CrashStatsBasePage):

    _crash_report_locator = "css=#signatureList tbody tr:nth-of-type(%s)"
    _signature_locator =  _crash_report_locator + " td:nth-of-type(5) a.signature"
    _index = 0

    def __init__(self, testsetup, index):
        CrashStatsBasePage.__init__(self, testsetup)
        self._index = index

    @property
    def signature(self):
        return self.sel.get_text(self._signature_locator % self._index)

    @property
    def has_empty_signature(self):
        if(self.signature == "empty signature"):
            return True
        return False


class CrashStatsAdvancedSearch(CrashStatsBasePage):

    _product_multiple_select = 'id=product'
    _filter_crash_reports_button = 'id=query_submit'
    _data_table = 'id=signatureList'
    _data_table_first_signature = 'css=table#signatureList > tbody > tr > td > a'

    def __init__(self, testsetup):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)
        count = 0
        self.wait_for_element_present(self._product_multiple_select)

    def filter_reports(self):
        self.sel.click(self._filter_crash_reports_button)
        self.sel.wait_for_page_to_load(self.timeout)
#        self.wait_for_element_present('css=div.page-heading > h2')

    def click_first_signature(self):
        self.wait_for_element_present(self._data_table_first_signature)
        signature = self.sel.get_text(self._data_table_first_signature)
        self.sel.click(self._data_table_first_signature)
        self.sel.wait_for_page_to_load(self.timeout)
        return signature

    @property
    def currently_selected_product(self):
        return self.sel.get_selected_value(self._product_multiple_select)

    @property
    def product_list(self):
        return self.sel.get_select_options(self._product_multiple_select)


class CrashStatsSearchResults(CrashStatsBasePage):

    _product_select = 'id=product'
    _version_select = 'id=version'
    _os_select = 'id=platform'
    _filter_crash_reports_button = 'id=query_submit'

    def __init__(self, testsetup):
        self.sel = testsetup.selenium
        self.wait_for_element_present(self._product_select)


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

    def __init__(self, testsetup):
        self.sel = testsetup.selenium

    @property
    def product_header(self):
        return self.sel.get_text(self._product_header)

    @property
    def product_version_header(self):
        return self.sel.get_text(self._product_version_header)


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
