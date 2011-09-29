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
#                 Teodosia Pop <teodosia.pop@softvision.ro>
#                 Alin Trif <alin.trif@softvision.ro>
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

from crash_stats_page import CrashStatsHomePage
from crash_stats_page import CrashStatsAdvancedSearch
from crash_stats_page import CrashStatsPerActiveDailyUser
from crash_stats_page import ProductsLinksPage
from unittestzero import Assert
import pytest
import mozwebqa


xfail = pytest.mark.xfail


class TestCrashReports:

    def test_that_reports_form_has_same_product_for_firefox(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        page_title = csp.page_title
        Assert.true('Firefox' in page_title)
        crash_adu = csp.select_report("Crashes per User")
        details = csp.current_details
        report_product = crash_adu.product_select
        Assert.equal(details['product'], report_product)

    def test_that_reports_form_has_same_product_for_thunderbird(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Thunderbird')
        page_title = csp.page_title
        Assert.true('Thunderbird' in page_title)
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            Assert.equal(details['product'], report_product)

    def test_that_reports_form_has_same_product_for_seamonkey(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('SeaMonkey')
        page_title = csp.page_title
        Assert.true('SeaMonkey' in page_title)
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            Assert.equal(details['product'], report_product)

    def test_that_reports_form_has_same_product_for_camino(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Camino')
        page_title = csp.page_title
        Assert.true('Camino' in page_title)
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            Assert.equal(details['product'], report_product)

    def test_that_reports_form_has_same_product_for_fennec(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Fennec')
        page_title = csp.page_title
        Assert.true('Fennec' in page_title)
        if not csp.can_find_text('no data'):
            crash_adu = csp.select_report("Crashes per User")
            details = csp.current_details
            report_product = crash_adu.product_select
            Assert.equal(details['product'], report_product)

    def test_that_current_version_selected_in_top_crashers_header_for_firefox(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        if not csp.can_find_text('no data'):
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_thunderbird(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Thunderbird')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_seamonkey(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('SeaMonkey')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_camino(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Camino')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_header_for_fennec(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Fennec')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_firefox(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers by URL')
        Assert.equal(details['product'], cstc.product_header)
        #Bug 611694 - Disabled till bug fixed
        #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_thunderbird(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Thunderbird')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_seamonkey(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('SeaMonkey')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_camino(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Camino')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_url_header_for_fennec(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Fennec')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by URL')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_firefox(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_thunderbird(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Thunderbird')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_seamonkey(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('SeaMonkey')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_camino(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Camino')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_current_version_selected_in_top_crashers_by_domain_header_for_fennec(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        csp.select_product('Fennec')
        if not csp.can_find_text('no data'):
            details = csp.current_details
            cstc = csp.select_report('Top Crashers by Domain')
            Assert.equal(details['product'], cstc.product_header)
            #Bug 611694 - Disabled till bug fixed
            #Assert.true(cstc.product_version_header in details['versions'])

    def test_that_top_crasher_filters_return_results(self, mozwebqa):
        # https://bugzilla.mozilla.org/show_bug.cgi?id=678906
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        details = csp.current_details
        cstc = csp.select_report('Top Crashers')
        if not csp.can_find_text('no data'):
            Assert.equal(details['product'], cstc.product_header)

        cstc.click_filter_all()
        results = cstc.count_results
        Assert.true(results > 0, "%s results found, expected >0" % results)

    def test_that_products_page_links_work(self, mozwebqa):
        self.selenium = mozwebqa.selenium
        products_page = ProductsLinksPage(mozwebqa)
        #An extra check that products page is loaded
        Assert.equal(products_page.get_products_page_name, 'Mozilla Products in Crash Reporter')
        products = ['Firefox', 'Thunderbird', 'Camino', 'SeaMonkey', 'Fennec']

        for product in products:
            csp = products_page.click_product(product)
            Assert.true(csp.get_url_current_page().endswith(product))
            Assert.contains(product, csp.get_page_name)
            products_page = ProductsLinksPage(mozwebqa)

    @xfail(reason="Disabled until Bug 603561 is fixed")
    def test_that_top_changers_is_highlighted_when_chosen(self, mozwebqa):
        """ Test for https://bugzilla.mozilla.org/show_bug.cgi?id=679229"""
        self.selenium = mozwebqa.selenium
        csp = CrashStatsHomePage(mozwebqa)
        for version in csp.current_details['versions']:
            if not csp.can_find_text('no data'):
                csp.select_version(version)
                cstc = csp.select_report('Top Changers')
                Assert.true(cstc.is_top_changers_highlighted)
