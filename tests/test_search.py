#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.home_page import CrashStatsHomePage

xfail = pytest.mark.xfail
prod = pytest.mark.prod


class TestSearchForIdOrSignature:

    @pytest.mark.nondestructive
    def test_that_when_item_not_available(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)

        cs_advanced = csp.header.search_for_crash("this won't exist")
        Assert.false(cs_advanced.are_results_found)

    @pytest.mark.nondestructive
    def test_that_search_for_valid_signature(self, mozwebqa):
        """
            This is a test for
                https://bugzilla.mozilla.org/show_bug.cgi?id=609070
        """
        csp = CrashStatsHomePage(mozwebqa)
        report_list = csp.click_first_product_top_crashers_link()
        signature = report_list.first_valid_signature_title

        result = csp.header.search_for_crash(signature)
        Assert.true(result.are_results_found)

    @pytest.mark.xfail(reason='Disabled until bug 768260 is fixed')
    @pytest.mark.nondestructive
    def test_that_advanced_search_for_firefox_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.click_filter_reports()
        Assert.contains('product is one of Firefox', cs_advanced.results_lead_in_text)

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_thunderbird_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Thunderbird')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.click_filter_reports()
        Assert.contains('product is one of Thunderbird', cs_advanced.results_lead_in_text)

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_fennec_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Fennec')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.click_filter_reports()
        Assert.contains('product is one of Fennec', cs_advanced.results_lead_in_text)

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_camino_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('Camino')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.click_filter_reports()
        Assert.contains('product is one of Camino', cs_advanced.results_lead_in_text)

    @pytest.mark.nondestructive
    def test_that_advanced_search_for_seamonkey_can_be_filtered(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product('SeaMonkey')
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.click_filter_reports()
        Assert.contains('product is one of SeaMonkey', cs_advanced.results_lead_in_text)

    @pytest.mark.xfail(reason='Disabled until bug 688256 is fixed')
    @pytest.mark.nondestructive
    def test_that_advanced_search_drilldown_results_are_correct(self, mozwebqa):
        # https://bugzilla.mozilla.org/show_bug.cgi?id=679310
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()

        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('All')
        cs_advanced.click_filter_reports()

        results_page_count = cs_advanced.results[0].number_of_crashes
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
        cs_advanced.click_filter_reports()
        if cs_advanced.are_results_found:
            Assert.true(cs_advanced.results[0].number_of_crashes > 0)
        else:
            Assert.equal(cs_advanced.no_results_text, 'No results were found.')

    @pytest.mark.prod
    @pytest.mark.xfail(reason='Disabled until bug 720037 is fixed')
    @pytest.mark.nondestructive
    def test_that_filter_for_browser_results(self, mozwebqa):
        #https://www.pivotaltracker.com/story/show/17769047
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.deselect_version()
        cs_advanced.adv_select_version('Firefox 16.0a1')
        cs_advanced.adv_select_os('Windows')
        cs_advanced.select_report_process('Browser')

        cs_advanced.click_filter_reports()

        browser_icon = [True]

        while True in browser_icon:
            browser_icon = [result.is_browser_icon_visible for result in cs_advanced.results]
            if False in browser_icon:
                Assert.fail("Browser icon not visible for result")

            if cs_advanced.is_next_visible == False:
                break
            else:
                cs_advanced.click_next()

    @pytest.mark.prod
    @pytest.mark.nondestructive
    def test_that_plugin_filters_result(self, mozwebqa):
        #https://www.pivotaltracker.com/story/show/17769047
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.deselect_version()
        cs_advanced.adv_select_version('Firefox 16.0a1')
        cs_advanced.adv_select_os('Windows')

        cs_advanced.select_report_process('Plugins')

        cs_advanced.click_filter_reports()

        plugin_icon = [True]

        while True in plugin_icon:
            plugin_icon = [result.is_plugin_icon_visible for result in cs_advanced.results]
            if False in plugin_icon:
                Assert.fail("Plugin icon not visible for result")

            if cs_advanced.is_next_visible == False:
                break
            else:
                cs_advanced.click_next()

    @pytest.mark.prod
    @pytest.mark.nondestructive
    def test_that_plugin_filename_column_sorts(self, mozwebqa):
        """
        https://bugzilla.mozilla.org/show_bug.cgi?id=562380
        """
        #Is sort order ok?

        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()

        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('All')
        cs_advanced.select_report_process('Plugins')
        cs_advanced.click_filter_reports()

        cs_advanced.results_table_header.click_sort_by_plugin_filename()

        plugin_filename_results_list = [row.plugin_filename.lower() for row in cs_advanced.results]

        Assert.is_sorted_ascending(plugin_filename_results_list)

        cs_advanced.results_table_header.click_sort_by_plugin_filename()

        plugin_filename_results_list = [row.plugin_filename.lower() for row in cs_advanced.results]
        Assert.is_sorted_descending(plugin_filename_results_list)
