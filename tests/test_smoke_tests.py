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
                          'SeaMonkey',
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

    @pytest.mark.nondestructive
    def test_that_simple_querystring_doesnt_return_500(self, mozwebqa):
        response = urllib.urlopen(mozwebqa.base_url + '/query/simple')

        Assert.equal(404, response.getcode())

    @pytest.mark.nondestructive
    def test_that_bugzilla_link_contain_current_site(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        path = '/invalidpath'
        csp.selenium.get(mozwebqa.base_url + path)

        Assert.contains('bug_file_loc=%s%s' % (mozwebqa.base_url, path), urllib.unquote(csp.link_to_bugzilla))

    @pytest.mark.nondestructive
    def test_that_exploitable_crash_report_not_displayed_for_not_logged_in_users(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)

        Assert.true('Exploitable Crashes' not in csp.header.report_list)
        Assert.false(csp.header.is_exploitable_crash_report_present)

    def test_login_logout(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        Assert.true(csp.footer.is_logged_out)

        csp.footer.login()
        Assert.true(csp.footer.is_logged_in)

        csp.footer.logout()
        Assert.true(csp.footer.is_logged_out)
