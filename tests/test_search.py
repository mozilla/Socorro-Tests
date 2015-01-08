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
        csp = CrashStatsHomePage(mozwebqa)
        report_list = csp.click_last_product_top_crashers_link()
        signature = report_list.first_signature_title
        result = csp.header.search_for_crash(signature)

        Assert.true(result.are_search_results_found)

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

        cs_super.click_search()
        Assert.true(cs_super.are_search_results_found)
        cs_super.click_more_options()

        # Delete all columns except the last one
        for column in cs_super.columns[:-1]:
            cs_super.click_crash_reports_tab()
            current_column = column.column_name
            Assert.true(current_column in cs_super.search_results_table_header.table_column_names)

            number_of_columns = len(cs_super.columns)
            column.delete_column()
            cs_super.wait_for_column_deleted(number_of_columns - 1)
            Assert.false(cs_super.is_column_in_list(current_column))

            cs_super.click_search()
            if len(cs_super.columns) > 1:
                cs_super.click_crash_reports_tab()
                Assert.true(cs_super.are_search_results_found)
                Assert.true(cs_super.search_results_table_header.is_column_not_present(current_column))

        Assert.true(cs_super.columns[0].column_name in cs_super.search_results_table_header.table_column_names)

    @pytest.mark.nondestructive
    def test_search_change_facet(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')
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
        cs_super.click_new_line()
        cs_super.select_field('release channel')
        cs_super.select_operator('has terms')
        # select the 2nd line
        cs_super.select_match('1', 'nightly')
        cs_super.click_search()

        Assert.true(cs_super.are_search_results_found)
