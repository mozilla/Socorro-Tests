#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import re

from unittestzero import Assert

from pages.home_page import CrashStatsHomePage
from pages.products_page import ProductsLinksPage


xfail = pytest.mark.xfail


class TestCrashReports:

    _expected_products = ['Firefox', 'Thunderbird', 'SeaMonkey', 'Camino', 'Fennec', 'FennecAndroid']

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
        # https://bugzilla.mozilla.org/show_bug.cgi?id=678906
        csp = CrashStatsHomePage(mozwebqa)
        product = csp.header.current_product
        cstc = csp.header.select_report('Top Crashers')

        if cstc.results_found:
            Assert.equal(product, cstc.page_heading_product)

        cstc.click_filter_by('All')
        Assert.greater(cstc.results_count, 0)

    @pytest.mark.nondestructive
    def test_that_selecting_nightly_builds_loads_page_and_link_to_ftp_works(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        nightly_builds_page = csp.header.select_report('Nightly Builds')
        Assert.equal(nightly_builds_page.page_heading, 'Nightly Builds for Firefox')

        website_link = nightly_builds_page.link_to_ftp
        #check that the link is valid
        Assert.not_none(re.match('(\w+\W+)', website_link))

        #test external link works
        nightly_builds_page.click_link_to_ftp()
        Assert.equal(website_link, nightly_builds_page.get_url_current_page())

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_products_page_links_work(self, mozwebqa, product):
        products_page = ProductsLinksPage(mozwebqa)
        #An extra check that products page is loaded
        Assert.equal(products_page.page_heading, 'Mozilla Products in Crash Reporter')

        csp = products_page.click_product(product)
        Assert.true(csp.get_url_current_page().endswith(product))
        Assert.contains(product, csp.page_heading)

    @pytest.mark.nondestructive
    def test_that_top_crasher_filter_browser_return_results(self, mozwebqa):
        # https://bugzilla.mozilla.org/show_bug.cgi?id=678906
        csp = CrashStatsHomePage(mozwebqa)
        product = csp.header.current_product
        cstc = csp.header.select_report('Top Crashers')

        if cstc.results_found:
            Assert.equal(product, cstc.page_heading_product)

        cstc.click_filter_by('Browser')
        Assert.greater(cstc.results_count, 0)

    @pytest.mark.nondestructive
    def test_that_top_crasher_filter_plugin_return_results(self, mozwebqa):
        # https://bugzilla.mozilla.org/show_bug.cgi?id=678906
        csp = CrashStatsHomePage(mozwebqa)
        product = csp.header.current_product
        cstc = csp.header.select_report('Top Crashers')

        if cstc.results_found:
            Assert.equal(product, cstc.page_heading_product)

        cstc.click_filter_by('Plugin')
        Assert.greater(cstc.results_count, 0)

    @pytest.mark.xfail(reason='Disabled until Bug 603561 is fixed')
    @pytest.mark.nondestructive
    def test_that_top_changers_is_highlighted_when_chosen(self, mozwebqa):
        """
        Test for https://bugzilla.mozilla.org/show_bug.cgi?id=679229
        """
        csp = CrashStatsHomePage(mozwebqa)
        for version in csp.header.current_versions:

            csp.header.select_version(str(version))
            cstc = csp.header.select_report('Top Changers')
            Assert.equal(cstc.header.current_report, 'Top Changers')

    @pytest.mark.xfail(run=False, reason="Bug 721928 - We shouldn't let the user query /daily for dates past for which we don't have data")
    @pytest.mark.nondestructive
    def test_that_filtering_for_a_past_date_returns_results(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/17141439
        """
        csp = CrashStatsHomePage(mozwebqa)
        crash_per_user = csp.header.select_report('Crashes per User')
        crash_per_user.type_start_date('1995-01-01')
        crash_per_user.click_generate_button()
        Assert.true(crash_per_user.is_table_visible)
        Assert.equal('1995-01-01', crash_per_user.last_row_date_value)

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_top_crashers_reports_links_work(self, mozwebqa, product):
        """
        https://www.pivotaltracker.com/story/show/17086667
        """
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
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_the_product_releases_return_results(self, mozwebqa, product):
        """
        https://www.pivotaltracker.com/story/show/20145655
        """

        if product == 'Fennec': pytest.xfail(reason='Lack of data on the staging server')

        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product(product)
        top_crashers = csp.release_channels

        for idx in range(len(top_crashers)):
            top_crasher_page = top_crashers[idx].click_top_crasher()
            Assert.true(top_crasher_page.results_found, 'No results found')
            top_crasher_page.return_to_previous_page()
            top_crashers = csp.release_channels

    @pytest.mark.nondestructive
    def test_that_7_days_is_selected_default_for_nightlies(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/17088605
        """
        csp = CrashStatsHomePage(mozwebqa)
        top_crashers = csp.release_channels
        tc_page = top_crashers[3].click_top_crasher()

        Assert.equal(tc_page.current_days_filter, '7')

    @pytest.mark.nondestructive
    def test_that_only_browser_reports_have_browser_icon(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/17099455
        """
        csp = CrashStatsHomePage(mozwebqa)
        reports_page = csp.click_first_product_top_crashers_link()
        Assert.equal(reports_page.current_filter_type, 'Browser')

        for signature_item in reports_page.signature_items:
            Assert.true(signature_item.is_browser_icon_visible, "Signature %s did not have a browser icon" % signature_item.title)
            Assert.false(signature_item.is_plugin_icon_visible, "Signature %s unexpextedly had a plugin icon" % signature_item.title)

    @pytest.mark.nondestructive
    def test_that_only_plugin_reports_have_plugin_icon(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/17099455
        """
        csp = CrashStatsHomePage(mozwebqa)
        reports_page = csp.click_first_product_top_crashers_link()
        reports_page.click_filter_by('Plugin')
        signature_list_items = reports_page.signature_items

        for signature_item in signature_list_items:
            Assert.true(signature_item.is_plugin_icon_visible, "Signature %s did not have a plugin icon" % signature_item.title)
            Assert.false(signature_item.is_browser_icon_visible, "Signature %s unexpextedly had a browser icon" % signature_item.title)

    @pytest.mark.nondestructive
    @pytest.mark.xfail(reason="haven't found a subtitution for the is_alert_present() method yet")
    def test_that_no_mixed_content_warnings_are_displayed(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/18049001
        https://bugzilla.mozilla.org/show_bug.cgi?id=630991#c0
        """
        csp = CrashStatsHomePage(mozwebqa)
        cpu = csp.header.select_report('Crashes per User')
        cpu.click_generate_button()
        Assert.true(cpu.is_the_current_page)
        Assert.false(cpu.is_mixed_content_warning_shown)

    @pytest.mark.nondestructive
    def test_that_lowest_version_topcrashers_do_not_return_errors(self, mozwebqa):
        """
        https://bugzilla.mozilla.org/show_bug.cgi?id=655506
        """
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_version('3.5.13')
        cstc = csp.header.select_report('Top Crashers')
        cstc.click_filter_days_by('14')
        Assert.not_equal('Unable to load data System error, please retry in a few minutes', cstc.page_heading)
        cstc.click_filter_by('Plugin')
        Assert.not_equal(self, 'Unable to load data System error, please retry in a few minutes', cstc.page_heading)

    @pytest.mark.nondestructive
    def test_that_malformed_urls_on_query_do_not_return_500_error(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/18059001
        https://bugzilla.mozilla.org/show_bug.cgi?id=642580
        """
        csp = CrashStatsHomePage(mozwebqa)
        csas = csp.header.click_advanced_search()
        Assert.true(csas.is_the_current_page)
        csas.build_id_field_input('http://www.google.com')
        csas.click_filter_reports()
        Assert.equal('No results were found.', csas.no_results_text)

    @pytest.mark.nondestructive
    def test_that_top_changers_data_is_available(self, mozwebqa):
        """
        https://www.pivotaltracker.com/story/show/18059119
        """
        csp = CrashStatsHomePage(mozwebqa)
        cstc = csp.header.select_report('Top Changers')
        Assert.not_equal('Top changers currently unavailable', cstc.page_heading)
