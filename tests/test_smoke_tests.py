#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import urllib

from unittestzero import Assert

from pages.home_page import CrashStatsHomePage


class TestSmokeTests:

    _expected_products = ['Firefox',
        'Thunderbird',
        'Camino',
        'SeaMonkey',
        'Fennec',
        'FennecAndroid',
        'WebappRuntime',
        'B2G']

    @pytest.mark.nondestructive
    def test_that_server_status_page_loads(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        csstat = csp.click_server_status()

        Assert.true(csstat.is_at_a_glance_present, 'Server summary not found')
        Assert.true(csstat.are_graphs_present, '4 graphs not found')
        Assert.true(csstat.is_latest_raw_stats_present, 'Raw stats not found')

    @pytest.mark.xfail(reason="bug 772372")
    @pytest.mark.nondestructive
    def test_that_options_are_sorted_the_same(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        cssearch = csp.header.click_advanced_search()
        nav_product_list = csp.header.product_list
        search_product_list = cssearch.product_list
        Assert.equal(len(nav_product_list), len(search_product_list))

        for i, prod_item in enumerate(nav_product_list):
            Assert.equal(prod_item, search_product_list[i])

    @pytest.mark.nondestructive
    @pytest.mark.parametrize(('product'), _expected_products)
    def test_that_advanced_search_has_product_highlighted_in_multiselect(self, mozwebqa, product):
        csp = CrashStatsHomePage(mozwebqa)
        csp.header.select_product(product)
        cs_advanced = csp.header.click_advanced_search()
        Assert.equal(product, cs_advanced.currently_selected_product)

    @pytest.mark.nondestructive
    def test_that_simple_querystring_doesnt_return_500(self, mozwebqa):
        response = urllib.urlopen(mozwebqa.base_url + '/query/simple')
        Assert.equal(404, response.getcode())

    @pytest.mark.nondestructive
    def test_that_bugzilla_link_contain_current_site(self, mozwebqa):
        """
        Bug 631737
        """
        csp = CrashStatsHomePage(mozwebqa)
        path = '/invalidpath'
        csp.selenium.get(mozwebqa.base_url + path)
        Assert.contains('bug_file_loc=%s%s' % (mozwebqa.base_url.replace('https', 'http'), path), urllib.unquote(csp.link_to_bugzilla))
