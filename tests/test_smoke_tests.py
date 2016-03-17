# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import urllib

from pages.home_page import CrashStatsHomePage


class TestSmokeTests:

    _expected_products = ['Firefox',
                          'Thunderbird',
                          'SeaMonkey',
                          'FennecAndroid',
                          'B2G']

    @pytest.mark.nondestructive
    def test_that_bugzilla_link_contain_current_site(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        path = '/invalidpath'
        csp.selenium.get(mozwebqa.base_url + path)

        assert 'bug_file_loc=%s%s' % (mozwebqa.base_url, path) in urllib.unquote(csp.link_to_bugzilla)

    @pytest.mark.nondestructive
    def test_that_exploitable_crash_report_not_displayed_for_not_logged_in_users(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)

        assert 'Exploitable Crashes' not in csp.header.report_list
        assert csp.header.is_exploitable_crash_report_present is not True

    def test_login_logout(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)
        assert csp.footer.is_logged_out

        csp.footer.login()
        assert csp.footer.is_logged_in

        csp.footer.logout()
        assert csp.footer.is_logged_out
