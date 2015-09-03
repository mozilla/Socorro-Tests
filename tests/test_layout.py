#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.home_page import CrashStatsHomePage


class TestLayout:

    @pytest.mark.nondestructive
    @pytest.mark.xfail("'mozilla.com' in config.getvalue('base_url')",
                       reason="https://bugzilla.mozilla.org/show_bug.cgi?id=1201622")
    def test_that_products_are_sorted_correctly(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        product_list = ['Firefox',
                        'Thunderbird',
                        'Fennec',
                        'FennecAndroid',
                        'SeaMonkey',
                        'WebappRuntime',
                        'B2G',
                        'WebappRuntimeMobile']
        products = csp.header.product_list

        assert product_list == products, \
            'Failed: Expected to find these products in the dropdown: %s, but found: %s' % (product_list, products)


class TestSuperSearchLayout:

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
            Assert.true(current_column in
                        cs_super.search_results_table_header.table_column_names
                        )

            number_of_columns = len(cs_super.columns)
            column.delete_column()
            cs_super.wait_for_column_deleted(number_of_columns - 1)
            Assert.false(cs_super.is_column_in_list(current_column))

            cs_super.click_search()
            if len(cs_super.columns) > 1:
                cs_super.click_crash_reports_tab()
                Assert.true(cs_super.are_search_results_found)
                Assert.true(cs_super.search_results_table_header.
                            is_column_not_present(current_column))

        Assert.true(cs_super.columns[0].column_name in
                    cs_super.search_results_table_header.table_column_names)

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
        # The facet in the results does not update immediately,
        # so wait for it to be the value we expect
        cs_super.wait_for_facet_in_results(cs_super.facet)
