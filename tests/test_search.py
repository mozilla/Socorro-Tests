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

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason='Bug 968476 - crash counts appear to be different')
    def test_that_advanced_search_drilldown_results_are_correct(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.adv_select_version('All')
        cs_advanced.set_period_value_field_input('\b4')
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
    @pytest.mark.nondestructive
    def test_that_plugin_filters_result(self, mozwebqa):
        """
        https://bugzilla.mozilla.org/show_bug.cgi?id=562380
        """
        csp = CrashStatsHomePage(mozwebqa)
        cs_advanced = csp.header.click_advanced_search()
        cs_advanced.adv_select_product('Firefox')
        cs_advanced.deselect_version()
        # Select 2nd Featured Version
        cs_advanced.adv_select_version_by_index(2)
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

    @pytest.mark.nondestructive
    def test_super_search_page_is_loaded(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        Assert.true(cs_super.is_the_current_page)

    @pytest.mark.nondestructive
    def test_default_fields_for_firefox(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.open_url('/search/?product=Firefox')
        Assert.equal(cs_super.field('0'), 'product')
        Assert.equal(cs_super.operator('0'), 'has terms')
        Assert.equal(cs_super.match('0'), 'Firefox')

    @pytest.mark.nondestructive
    def test_search_for_unrealistic_data(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.open_url('/search/?date=>2000:01:01 00-00')
        Assert.equal(cs_super.error, 'Enter a valid date/time.')

    @pytest.mark.nondestructive
    def test_search_change_column(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')
        cs_super.select_match('0', 'Firefox')
        cs_super.click_search()
        Assert.true(cs_super.are_search_results_found)
        cs_super.click_more_options()

        # Delete all columns except the last one
        for column in cs_super.columns[:-1]:
            current_column = column.column_name
            Assert.true(current_column in cs_super.search_results_table_header.table_column_names)
            number_of_columns = len(cs_super.columns)
            column.delete_column()
            cs_super.wait_for_column_deleted(number_of_columns - 1)
            Assert.false(cs_super.is_column_in_list(current_column))
            cs_super.click_search()
            if len(cs_super.columns) > 1:
                Assert.true(cs_super.are_search_results_found)
                Assert.false(current_column in cs_super.search_results_table_header.table_column_names)

        Assert.true(cs_super.columns[0].column_name in cs_super.search_results_table_header.table_column_names)

    @pytest.mark.nondestructive
    def test_search_change_facet(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')
        cs_super.select_match('0', 'Firefox')
        cs_super.click_search()
        Assert.true(cs_super.facet in cs_super.results_facet.lower())
        cs_super.click_more_options()
        cs_super.delete_facet()
        cs_super.type_facet('address')
        Assert.equal(cs_super.facet, 'address')
        cs_super.click_search()
        Assert.true(cs_super.facet in cs_super.results_facet.lower())

    @pytest.mark.nondestructive
    def test_search_with_one_line(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')
        cs_super.select_match('0', 'Firefox')
        cs_super.click_search()
        Assert.true(cs_super.are_search_results_found)
        Assert.equal(cs_super.field('0'), 'product')
        Assert.equal(cs_super.operator('0'), 'has terms')
        Assert.equal(cs_super.match('0'), 'Firefox')

    @pytest.mark.nondestructive
    def test_search_with_multiple_lines(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')
        cs_super.select_match('0', 'Firefox')
        cs_super.click_new_line()
        cs_super.select_field('release channel')
        cs_super.select_operator('has terms')
        cs_super.select_match('1', 'nightly')
        cs_super.click_search()
        Assert.true(cs_super.are_search_results_found)
