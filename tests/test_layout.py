#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from pages.crash_stats_page import CrashStatsHomePage
from pages.crash_stats_page import CrashStatsTopCrashers
from unittestzero import Assert
xfail = pytest.mark.xfail


class TestLayout:

    @pytest.mark.nondestructive
    def test_that_products_are_sorted_correctly(self, mozwebqa):

        csp = CrashStatsHomePage(mozwebqa)

        product_list = ['Firefox', 'Thunderbird', 'Camino', 'SeaMonkey', 'Fennec', 'FennecAndroid']
        products = csp.header.product_list
        Assert.equal(product_list, products)

    @pytest.mark.xfail(reason='Bug 687841 - Versions in Navigation Bar appear in wrong order')
    @pytest.mark.nondestructive
    def test_that_product_versions_are_ordered_correctly(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)

        Assert.is_sorted_descending(csp.header.current_versions)
        Assert.is_sorted_descending(csp.header.other_versions)

    @pytest.mark.nondestructive
    def test_that_topcrasher_is_not_returning_http500(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.selenium.get(mozwebqa.base_url + '/topcrasher')
        tc = CrashStatsTopCrashers(mozwebqa)
        Assert.contains('Top Crashers', tc.page_heading)
        Assert.true(tc.results_found, 'No results found!')

    @pytest.mark.nondestructive
    def test_that_report_is_not_returning_http500(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.selenium.get(mozwebqa.base_url + '/report')
        Assert.contains('Page not Found', csp.page_heading)

    @pytest.mark.nondestructive
    def test_that_correlation_is_not_returning_http500(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.selenium.get(mozwebqa.base_url + '/correlation')
        Assert.contains('Page not Found', csp.page_heading)
