#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from pages.crash_stats_page import CrashStatsHomePage
from unittestzero import Assert
import pytest

class TestSpecificVersions:

    @pytest.mark.nondestructive
    def test_that_selecting_exact_version_doesnt_show_other_versions(self, mozwebqa):
        csp = CrashStatsHomePage(mozwebqa)

        product = csp.header.current_product
        versions = csp.header.current_versions

        if len(versions) > 0:
            csp.header.select_version(str(versions[1]))

        report_list = csp.click_first_product_top_crashers_link()
        crash_report_page = report_list.click_first_valid_signature()
        crash_report_page.click_reports()

        for report in crash_report_page.reports:
            Assert.equal(report.product, product)
            Assert.contains(report.version, str(versions[1]))
