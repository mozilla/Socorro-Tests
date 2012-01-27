#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.crash_stats_page import CrashStatsHomePage
from unittestzero import Assert
import pytest
import urllib
xfail = pytest.mark.xfail


class TestSmokeTests:

    def test_that_server_status_page_loads(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csstat = csp.click_server_status()

        Assert.true(csstat.is_at_a_glance_present(), 'Server summary not found')
        Assert.true(csstat.are_graphs_present(), '4 graphs not found')
        Assert.true(csstat.is_latest_raw_stats_present(), 'Raw stats not found')

    @xfail(reason="Disabled till Bug 612679 is fixed")
    def test_that_options_are_sorted_the_same(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cssearch = csp.header.click_advanced_search()
        nav_product_list = csp.header.product_list
        search_product_list = cssearch.product_list
        Assert.equal(len(nav_product_list), len(search_product_list), csp.get_url_current_page())
        for i, prod_item in enumerate(nav_product_list):
            Assert.equal(prod_item, search_product_list[i], csp.get_url_current_page())

    def test_that_advanced_search_has_firefox_highlighted_in_multiselect(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        Assert.equal('Firefox', cs_advanced.currently_selected_product, cs_advanced.get_url_current_page())

    def test_that_advanced_search_has_thunderbird_highlighted_in_multiselect(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Thunderbird')
        cs_advanced = csp.header.click_advanced_search()
        Assert.equal('Thunderbird', cs_advanced.currently_selected_product, cs_advanced.get_url_current_page())

    def test_that_advanced_search_has_fennec_highlighted_in_multiselect(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Fennec')
        cs_advanced = csp.header.click_advanced_search()
        Assert.equal('Fennec', cs_advanced.currently_selected_product, cs_advanced.get_url_current_page())

    def test_that_advanced_search_has_camino_highlighted_in_multiselect(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Camino')
        cs_advanced = csp.header.click_advanced_search()
        Assert.equal('Camino', cs_advanced.currently_selected_product, cs_advanced.get_url_current_page())

    def test_that_advanced_search_has_seamonkey_highlighted_in_multiselect(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('SeaMonkey')
        cs_advanced = csp.header.click_advanced_search()
        Assert.equal('SeaMonkey', cs_advanced.currently_selected_product, cs_advanced.get_url_current_page())

    @xfail(reason="Disabled till Bug 652880 is fixed")
    def test_that_advanced_search_view_signature_for_firefox_crash(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()

        if cs_advanced.results_found:
            signature = cs_advanced.first_signature_name
            cssr = cs_advanced.click_first_signature()
            Assert.contains(signature, cssr.page_heading)

    def test_that_advanced_search_view_signature_for_thunderbird_crash(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Thunderbird')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()

        if cs_advanced.results_found:
            signature = cs_advanced.first_signature_name
            cssr = cs_advanced.click_first_signature()
            Assert.contains(signature, cssr.page_heading)

    def test_that_advanced_search_view_signature_for_fennec_crash(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Fennec')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()

        if cs_advanced.results_found:
            signature = cs_advanced.first_signature_name
            cssr = cs_advanced.click_first_signature()
            Assert.contains(signature, cssr.page_heading)

    def test_that_advanced_search_view_signature_for_camino_crash(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Camino')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()

        if cs_advanced.results_found:
            signature = cs_advanced.first_signature_name
            cssr = cs_advanced.click_first_signature()
            Assert.contains(signature, cssr.page_heading)

    def test_that_advanced_search_view_signature_for_seamonkey_crash(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('SeaMonkey')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()

        if cs_advanced.results_found:
            signature = cs_advanced.first_signature_name
            cssr = cs_advanced.click_first_signature()
            Assert.contains(signature, cssr.page_heading)

    def test_that_simple_querystring_doesnt_return_500(self, mozwebqa):
        response = urllib.urlopen(mozwebqa.base_url + "/query/simple")
        Assert.equal(404, response.getcode())

    @xfail(reason="Bug 631737")
    def test_that_bugzilla_link_contain_current_site(self, mozwebqa):
        ''' Bug 631737 '''
        csp = CrashStatsHomePage(mozwebqa)
        path = '/invaliddomain'
        csp.get_url_path(path)
        Assert.contains('bug_file_loc=%s%s' % (mozwebqa.base_url, path), urllib.unquote(csp.link_to_bugzilla))
