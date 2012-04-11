#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.crash_stats_page import CrashStatsHomePage
from unittestzero import Assert
import pytest
xfail = pytest.mark.xfail
prod = pytest.mark.prod


class TestSearchForIdOrSignature:

    @pytest.mark.nondestructive
    def test_that_when_item_not_available(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)

        results = csp.header.search_for_crash("this won't exist")
        Assert.false(results.results_found)

    @pytest.mark.nondestructive
    def test_that_search_for_valid_signature(self, mozwebqa):
        """.....
            This is a test for
                https://bugzilla.mozilla.org/show_bug.cgi?id=609070
        """
        csp = CrashStatsHomePage(mozwebqa)
        report_list = csp.click_first_product_top_crashers_link()
        signature = report_list.first_valid_signature_text

        result = csp.header.search_for_crash(signature)
        Assert.true(result.results_found)

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_firefox_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.contains('product is one of Firefox', cs_advanced.query_results_text(0))

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_thunderbird_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Thunderbird')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.contains('product is one of Thunderbird', cs_advanced.query_results_text(0))

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_fennec_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Fennec')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.contains('product is one of Fennec', cs_advanced.query_results_text(0))

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_camino_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Camino')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.contains('product is one of Camino', cs_advanced.query_results_text(0))

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_seamonkey_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('SeaMonkey')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.filter_reports()
        Assert.contains('product is one of SeaMonkey', cs_advanced.query_results_text(0))

    @pytest.mark.xfail(reason='Disabled until bug 688256 is fixed')
    @pytest.mark.nondestructive
    def test_that_advanced_search_drilldown_results_are_correct(self, mozwebqa):
        # https://bugzilla.mozilla.org/show_bug.cgi?id=679310
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()

        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('All')
        cs_advanced.filter_reports()

        results_page_count = cs_advanced.first_signature_number_of_results
        cssr = cs_advanced.click_first_signature()
        cssr.click_reports()
        Assert.equal(results_page_count, cssr.total_items_label)

    @pytest.mark.prod
    @pytest.mark.nondestructive
    def test_that_search_for_a_given_build_id_works(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/17368401
        """
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()

        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('All')
        cs_advanced.build_id_field_input(cs_advanced.build_id)
        cs_advanced.filter_reports()
        if cs_advanced.results_found:
            Assert.true(cs_advanced.first_signature_number_of_results > 0)
        else:
            Assert.equal(cs_advanced.query_results_text(1), 'No results were found.')

    @pytest.mark.prod
    @pytest.mark.xfail(reason='Disabled until bug 720037 is fixed')
    @pytest.mark.nondestructive
    def test_that_filter_for_browser_results(self, mozwebqa):
        #https://www.pivotaltracker.com/story/show/17769047
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('Firefox 13.0a2')
        cs_advanced.adv_select_os('Windows')
        cs_advanced.select_radio_button(1)
        cs_advanced.filter_reports()

        while not cs_advanced.is_browser_icon_visible:
            try:
                cs_advanced.click_next()
            except:
                Assert.fail('reached the last page and no data was found')

        Assert.true(cs_advanced.is_browser_icon_visible)

    @pytest.mark.prod
    @pytest.mark.nondestructive
    def test_that_plugin_filters_result(self, mozwebqa):
        #https://www.pivotaltracker.com/story/show/17769047
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('Firefox 13.0a2')
        cs_advanced.adv_select_os('Windows')

        cs_advanced.select_radio_button(2)

        cs_advanced.filter_reports()

        while not cs_advanced.is_plugin_icon_visible:
            cs_advanced.click_next()

        Assert.true(cs_advanced.is_plugin_icon_visible)

    @pytest.mark.prod
    @pytest.mark.nondestructive
    def test_that_plugin_filename_column_sorts(self, mozwebqa):
        """
        https://bugzilla.mozilla.org/show_bug.cgi?id=562380
        """
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()

        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('All')
        cs_advanced.select_radio_button(2)
        cs_advanced.filter_reports()
        if cs_advanced.results_found:
            cs_advanced.click_plugin_filename_header()
            Assert.is_sorted_ascending(cs_advanced.plugin_filename_results_list())

            cs_advanced.click_plugin_filename_header()
            Assert.is_sorted_descending(cs_advanced.plugin_filename_results_list())
        else:
            Assert.equal(cs_advanced.query_results_text(1), 'No results were found.')
