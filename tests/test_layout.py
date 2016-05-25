# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import CrashStatsHomePage


class TestLayout:

    @pytest.mark.nondestructive
    def test_that_products_are_sorted_correctly(self, base_url, selenium):
        csp = CrashStatsHomePage(base_url, selenium)
        product_list = ['Firefox',
                        'Thunderbird',
                        'Fennec',
                        'FennecAndroid',
                        'SeaMonkey']
        products = csp.header.product_list

        assert product_list == products, 'Expected products not in the product dropdown'


class TestSuperSearchLayout:

    @pytest.mark.nondestructive
    def test_super_search_page_is_loaded(self, base_url, selenium):
        csp = CrashStatsHomePage(base_url, selenium)
        cs_super = csp.header.click_super_search()

        assert cs_super.is_the_current_page

    @pytest.mark.nondestructive
    def test_default_fields_for_firefox(self, base_url, selenium):
        csp = CrashStatsHomePage(base_url, selenium)
        cs_super = csp.header.click_super_search()
        cs_super.open_url('/search/?product=Firefox')

        assert 'product' == cs_super.field('0')
        assert 'has terms' == cs_super.operator('0')
        assert 'Firefox' == cs_super.match('0')

    @pytest.mark.nondestructive
    def test_search_change_column(self, base_url, selenium):
        csp = CrashStatsHomePage(base_url, selenium)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')

        cs_super.click_search()
        assert cs_super.are_search_results_found
        cs_super.click_more_options()

        # Delete all columns except the last one
        for column in cs_super.columns[:-1]:
            cs_super.click_crash_reports_tab()
            current_column = column.column_name
            assert current_column in cs_super.search_results_table_header.table_column_names

            number_of_columns = len(cs_super.columns)
            column.delete_column()
            cs_super.wait_for_column_deleted(number_of_columns - 1)
            assert cs_super.is_column_in_list(current_column) is not True

            cs_super.click_search()
            if len(cs_super.columns) > 1:
                cs_super.click_crash_reports_tab()
                assert cs_super.are_search_results_found
                assert cs_super.search_results_table_header.is_column_not_present(current_column)

        assert cs_super.columns[0].column_name in cs_super.search_results_table_header.table_column_names

    @pytest.mark.nondestructive
    def test_search_change_facet(self, base_url, selenium):
        csp = CrashStatsHomePage(base_url, selenium)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')
        cs_super.click_search()
        assert cs_super.facet in cs_super.results_facet.lower()

        cs_super.click_more_options()
        cs_super.delete_facet()
        cs_super.type_facet('address')
        assert 'address' == cs_super.facet

        cs_super.click_search()
        # The facet in the results does not update immediately,
        # so wait for it to be the value we expect
        cs_super.wait_for_facet_in_results(cs_super.facet)
