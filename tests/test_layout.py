#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Crash Tests Selenium Tests.
#
# The Initial Developer of the Original Code is
# Mozilla.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Bebe <florin.strugariu@softvision.ro>
#   Dave Hunt <dhunt@mozilla.com>
#   Sergiu Mezei <sergiu.mezei@gmail.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

import pytest
from pages.crash_stats_page import CrashStatsHomePage
from unittestzero import Assert
xfail = pytest.mark.xfail


class TestLayout:

    def test_that_products_are_sorted_correctly(self, mozwebqa):

        csp = CrashStatsHomePage(mozwebqa)

        product_list = ["Firefox", "Thunderbird", "Camino", "SeaMonkey", "Fennec", "FennecAndroid"]
        products = csp.header.product_list
        Assert.equal(product_list, products, csp.get_url_current_page())

    @xfail(reason="Bug 687841 - Versions in Navigation Bar appear in wrong order")
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
