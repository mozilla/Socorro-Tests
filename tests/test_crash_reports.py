#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from unittestzero import Assert

from pages.home_page import CrashStatsHomePage
from pages.products_page import ProductsLinksPage


class TestCrashReports:

    _expected_products = [
        'Firefox',
        'Thunderbird',
        'SeaMonkey',
        'FennecAndroid',
        'WebappRuntime',
        'B2G']

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_reports_form_has_same_product(self, mozwebqa, product):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product(product)
        Assert.contains(product, csp.page_title)

        crash_adu = csp.header.select_report('Crashes per User')
        Assert.equal(crash_adu.header.current_product, crash_adu.product_select)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_current_version_selected_in_top_crashers_header(self, mozwebqa, product):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product(product)
        cstc = csp.header.select_report('Top Crashers')

        Assert.equal(product, cstc.page_heading_product)
        Assert.equal(cstc.header.current_version, cstc.page_heading_version)

    @pytest.mark.nondestructive
    def test_that_top_crasher_filter_all_return_results(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        product = csp.header.current_product
        cstc = csp.header.select_report('Top Crashers')
        if cstc.results_found:
            Assert.equal(product, cstc.page_heading_product)

        cstc.click_filter_by('All')
        Assert.greater(cstc.results_count, 0)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_products_page_links_work(self, mozwebqa, product):
        products_page = ProductsLinksPage(mozwebqa)
        Assert.equal(products_page.page_heading, 'Mozilla Products in Crash Reporter')

        csp = products_page.click_product(product)
        Assert.true(csp.get_url_current_page().endswith(product))
        Assert.contains(product, csp.page_heading)

    @pytest.mark.nondestructive
    def test_that_top_crasher_filter_browser_return_results(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        product = csp.header.current_product
        cstc = csp.header.select_report('Top Crashers')
        if cstc.results_found:
            Assert.equal(product, cstc.page_heading_product)

        cstc.click_filter_by('Browser')
        Assert.greater(cstc.results_count, 0)

    @pytest.mark.nondestructive
    def test_that_top_crasher_filter_plugin_return_results(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        product = csp.header.current_product
        cstc = csp.header.select_report('Top Crashers')
        if cstc.results_found:
            Assert.equal(product, cstc.page_heading_product)

        cstc.click_filter_by('Plugin')
        Assert.greater(cstc.results_count, 0)

    @pytest.mark.nondestructive
    def test_that_top_changers_is_highlighted_when_chosen(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        for version in csp.header.current_versions:
            csp.header.select_version(str(version))
            cstc = csp.header.select_report('Top Changers')
            Assert.equal(cstc.header.current_report, 'Top Changers')

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_top_crashers_reports_links_work(self, mozwebqa, product):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product(product)
        top_crashers = csp.release_channels

        for idx in range(len(top_crashers)):
            top_crasher_name = top_crashers[idx].product_version_label
            top_crasher_page = top_crashers[idx].click_top_crasher()
            Assert.contains(top_crasher_name, top_crasher_page.page_heading)
            top_crasher_page.return_to_previous_page()
            top_crashers = csp.release_channels

    @pytest.mark.nondestructive
    @pytest.mark.xfail("'allizom.org' in config.getvalue('base_url')",
                       reason="https://bugzilla.mozilla.org/show_bug.cgi?id=1122013")
    # Bug 1122013 - [stage][regression] Signature reports do not load
    def test_top_crasher_reports_tab_has_uuid_report(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        top_crashers = csp.click_last_product_top_crashers_link()
        crash_signature = top_crashers.click_first_signature()
        crash_signature.click_reports_tab()
        reports_table_count = len(crash_signature.reports)

        # verify crash reports table is populated
        Assert.greater(crash_signature.results_count_total, 0)
        Assert.greater(reports_table_count, 0, "No reports found")

        most_recent_report = crash_signature.reports[0]
        uuid_report = most_recent_report.click_report_date()

        # verify the uuid report page
        Assert.not_equal(uuid_report.uuid_in_body, "", "UUID not found in body")
        Assert.not_equal(uuid_report.uuid_in_table, "", "UUID not found in table")
        Assert.not_equal(uuid_report.signature_in_body, "", "Signature not found in body")
        Assert.not_equal(uuid_report.signature_in_table, "", "Signature not found in table")

        Assert.equal(uuid_report.uuid_in_body, uuid_report.uuid_in_table,
                     'UUID in body did not match the UUID in the table: '
                     'body "%s", table "%s"'
                     % (uuid_report.uuid_in_body,
                        uuid_report.uuid_in_table))
        Assert.contains(uuid_report.signature_in_body,
                     uuid_report.signature_in_table,
                     'Signature in body did not match the signature in the '
                     'table: body "%s", table "%s"'
                     % (uuid_report.signature_in_body,
                        uuid_report.signature_in_table))

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_the_product_releases_return_results(self, mozwebqa, product):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product(product)
        top_crashers = csp.release_channels

        for idx in range(len(top_crashers)):
            top_crasher_page = top_crashers[idx].click_top_crasher()
            if top_crasher_page.no_results_text is not False:
                Assert.contains("No crashing signatures found for the period", top_crasher_page.no_results_text)
            else:
                Assert.true(top_crasher_page.results_found, 'No results found')
            top_crasher_page.return_to_previous_page()
            top_crashers = csp.release_channels

    @pytest.mark.nondestructive
    def test_that_7_days_is_selected_default_for_nightlies(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        top_crashers = csp.release_channels
        tc_page = top_crashers[1].click_top_crasher()

        Assert.equal(tc_page.current_days_filter, '7')

    @pytest.mark.nondestructive
    def test_that_only_browser_reports_have_browser_icon(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        reports_page = csp.click_last_product_top_crashers_link()
        type, days, os = 'Browser', '7', 'Windows'
        Assert.equal(reports_page.current_filter_type, type)

        reports_page.click_filter_days_by(days)
        reports_page.click_filter_os_by(os)
        Assert.equal((type, days, os), (reports_page.current_filter_type,
                                        reports_page.current_days_filter,
                                        reports_page.current_os_filter))

        signature_list_items = reports_page.random_signature_items(19)
        Assert.true(len(signature_list_items) > 0, "Signature list items not found")

        for signature_item in signature_list_items:
            Assert.true(signature_item.is_browser_icon_visible,
                        "Signature %s did not have a browser icon" % signature_item.title)
            Assert.false(signature_item.is_plugin_icon_visible,
                         "Signature %s unexpectedly had a plugin icon" % signature_item.title)

    @pytest.mark.nondestructive
    def test_that_only_plugin_reports_have_plugin_icon(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        reports_page = csp.click_last_product_top_crashers_link()
        type, days, os = 'Plugin', '28', 'Windows'
        reports_page.click_filter_by(type)
        reports_page.click_filter_days_by(days)
        reports_page.click_filter_os_by(os)
        Assert.equal((type, days, os), (reports_page.current_filter_type,
                                        reports_page.current_days_filter,
                                        reports_page.current_os_filter))
        signature_list_items = reports_page.signature_items

        Assert.true(len(signature_list_items) > 0, "Signature list items not found")

        for signature_item in signature_list_items[:min(signature_list_items, 24)]:
            Assert.true(signature_item.is_plugin_icon_visible,
                        "Signature %s did not have a plugin icon" % signature_item.title)
            Assert.false(signature_item.is_browser_icon_visible,
                         "Signature %s unexpectedly had a browser icon" % signature_item.title)

    @pytest.mark.nondestructive
    def test_that_lowest_version_topcrashers_do_not_return_errors(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        lowest_version_index = len(csp.header.version_select_text) - 1
        csp.header.select_version_by_index(lowest_version_index)
        cstc = csp.header.select_report('Top Crashers')
        cstc.click_filter_days_by('14')
        Assert.not_equal('Unable to load data System error, please retry in a few minutes', cstc.page_heading)

        cstc.click_filter_by('Plugin')
        Assert.not_equal(self, 'Unable to load data System error, please retry in a few minutes', cstc.page_heading)

    @pytest.mark.nondestructive
    def test_that_top_changers_data_is_available(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cstc = csp.header.select_report('Top Changers')

        Assert.not_equal('Top changers currently unavailable', cstc.page_heading)
