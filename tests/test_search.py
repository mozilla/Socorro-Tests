# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from pages.home_page import CrashStatsHomePage


class TestSuperSearch:

    @pytest.mark.nondestructive
    def test_search_for_unrealistic_data(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.open_url('/search/?date=>2000:01:01 00-00')

        assert 'Enter a valid date/time.' == cs_super.error

    @pytest.mark.nondestructive
    def test_search_with_one_line(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cs_super = csp.header.click_super_search()
        cs_super.select_field('product')
        cs_super.select_operator('has terms')
        cs_super.click_search()

        assert cs_super.are_search_results_found
        assert 'product' == cs_super.field('0')
        assert 'has terms' == cs_super.operator('0')
        assert 'Firefox' == cs_super.match('0')

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

        assert cs_super.are_search_results_found


class TestSearchForSpecificResults:

    @pytest.mark.nondestructive
    def test_search_for_valid_signature(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        report_list = csp.click_last_product_top_crashers_link()
        signature = report_list.first_signature_title
        result = csp.header.search_for_crash(signature)

        assert result.are_search_results_found

    @pytest.mark.nondestructive
    def test_selecting_one_version_doesnt_show_other_versions(self, mozwebqa):
        maximum_checks = 20  # limits the number of reports to check
        csp = CrashStatsHomePage(mozwebqa)
        product = csp.header.current_product
        versions = csp.header.current_versions
        version = str(versions[1])
        csp.header.select_version(version)
        report_list = csp.click_last_product_top_crashers_link()
        crash_report_page = report_list.click_first_signature()
        crash_report_page.click_reports_tab()
        reports = crash_report_page.reports

        assert len(reports) > 0, 'reports not found for signature'

        random_indexes = csp.get_random_indexes(reports, maximum_checks)
        for index in random_indexes:
            report = reports[index]
            assert product == report.product
