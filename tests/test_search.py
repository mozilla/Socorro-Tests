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

    _expected_products = ['Firefox',
                          'Thunderbird',
                          'SeaMonkey',
                          'Fennec',
                          'FennecAndroid',
                          'WebappRuntime',
                          'B2G']

    @pytest.mark.nondestructive
    def test_that_search_for_valid_signature(self, mozwebqa):
        """
            This is a test for
                https://bugzilla.mozilla.org/show_bug.cgi?id=609070
        """
        csp = CrashStatsHomePage(mozwebqa)
        report_list = csp.click_last_product_top_crashers_link()
        signature = report_list.first_signature_title

        result = csp.header.search_for_crash(signature)
        Assert.true(result.are_results_found)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_advanced_search_for_product_can_be_filtered(self, mozwebqa, product):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product(product)
        cs_advanced = csp.header.click_advanced_search()
        # filter on 3 days worth of data
        cs_advanced.set_period_value_field_input('\b3')
        cs_advanced.select_period_units('Days')
        cs_advanced.click_filter_reports()
        Assert.contains('product is one of %s' % product, cs_advanced.results_lead_in_text)

    @pytest.mark.nondestructive
    def test_that_selecting_exact_version_doesnt_show_other_versions(self, mozwebqa):
        maximum_checks = 20  # limits the number of reports to check
        csp = CrashStatsHomePage(mozwebqa)

        product = csp.header.current_product
        versions = csp.header.current_versions
        version = str(versions[1])
        csp.header.select_version(version)

        report_list = csp.click_last_product_top_crashers_link()
        crash_report_page = report_list.click_first_signature()
        crash_report_page.click_reports()
        reports = crash_report_page.reports
        Assert.true(len(reports) > 0, "reports not found for signature")

        random_indexes = csp.get_random_indexes(reports, maximum_checks)
        for index in random_indexes:
            report = reports[index]
            Assert.equal(report.product, product)
            Assert.contains(report.version, version)

    @pytest.mark.xfail(reason='Disabled until bug 788601 is fixed')
    @pytest.mark.nondestructive
    def test_that_advanced_search_drilldown_results_are_correct(self, mozwebqa):
        # https://bugzilla.mozilla.org/show_bug.cgi?id=788601
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('All')
        cs_advanced.set_period_value_field_input('\b3')
        cs_advanced.select_period_units('Days')
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
        # Select 2nd Featured Version (3rd selection in dropdown)
        cs_advanced.adv_select_version_by_index(2)
        cs_advanced.adv_select_os('Windows')
        cs_advanced.select_report_process('browser')

        cs_advanced.click_filter_reports()
        cs_advanced.go_to_random_result_page()

        for result in cs_advanced.results:
            Assert.true(result.is_browser_icon_visible)

    @pytest.mark.prod
    #xfailed - Bug 913126 - Advanced Search: No results returned for 24.0b
    @pytest.mark.xfail("'crash-stats.mozilla.com' in config.getvalue('base_url')")
    @pytest.mark.nondestructive
    def test_that_plugin_filters_result(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/17769047
        https://bugzilla.mozilla.org/show_bug.cgi?id=562380
        """
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.deselect_version()
        # Select 3rd Featured Version (3rd selection in dropdown)
        cs_advanced.adv_select_version_by_index(3)
        cs_advanced.adv_select_os('Windows')
        cs_advanced.select_report_process('plugin')

        cs_advanced.click_filter_reports()

        # verify the plugin icon is visible
        for result in cs_advanced.random_results(19):
            Assert.true(result.is_plugin_icon_visible)

        # verify ascending & descending sort
        cs_advanced.results_table_header.click_sort_by_plugin_filename()
        plugin_filename_results_list = [row.plugin_filename.lower() for row in cs_advanced.top_results(19)]
        Assert.is_sorted_ascending(plugin_filename_results_list)

        cs_advanced.results_table_header.click_sort_by_plugin_filename()
        plugin_filename_results_list = [row.plugin_filename.lower() for row in cs_advanced.top_results(19)]
        Assert.is_sorted_descending(plugin_filename_results_list)
