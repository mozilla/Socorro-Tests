#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
from pages.crash_stats_page import CrashStatsHomePage
from unittestzero import Assert
xfail = pytest.mark.xfail


class TestLayout:

    def test_that_products_are_sorted_correctly(self, mozwebqa):

        csp = CrashStatsHomePage(mozwebqa)

        product_list = ['Firefox', 'Thunderbird', 'Camino', 'SeaMonkey', 'Fennec', 'FennecAndroid']
        products = csp.header.product_list
        Assert.equal(product_list, products, csp.get_url_current_page())

    @xfail(reason='Bug 687841 - Versions in Navigation Bar appear in wrong order')
    def test_that_product_versions_are_ordered_correctly(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)

        Assert.is_sorted_descending(csp.header.current_versions, csp.get_url_current_page())
        Assert.is_sorted_descending(csp.header.other_versions, csp.get_url_current_page())

    def test_that_topcrasher_is_not_returning_http500(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.get_url_path(csp.base_url + '/topcrasher')
        Assert.contains('Top Crashers', csp.get_page_name)
        Assert.true(csp.results_found(), 'No results found!')

    def test_that_report_is_not_returning_http500(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.get_url_path(csp.base_url + '/report')
        Assert.contains('Page not Found', csp.get_page_name)

    def test_that_correlation_is_not_returning_http500(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csp.get_url_path(csp.base_url + '/correlation')
        Assert.contains('Page not Found', csp.get_page_name)
