#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import CrashStatsBasePage


class CrashStatsStatus(CrashStatsBasePage):

    _at_a_glance_locator = (By.CSS_SELECTOR, 'div.panel > div > table.server_status')
    _graphs_locator = (By.CSS_SELECTOR, 'div.panel > div > div.server-status-graph')
    _latest_raw_stats_locator = (By.CSS_SELECTOR, 'div.panel > div > table#server-stats-table')

    @property
    def is_at_a_glance_present(self):
        return self.is_element_visible(None, *self._at_a_glance_locator)

    @property
    def are_graphs_present(self):
        return len(self.selenium.find_elements(*self._graphs_locator)) == 4

    @property
    def is_latest_raw_stats_present(self):
        return self.is_element_visible(None, *self._latest_raw_stats_locator)
