#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait as Wait

from pages.base_page import CrashStatsBasePage


class CrashStatsHomePage(CrashStatsBasePage):
    """
        Page Object for Socorro
        https://crash-stats.allizom.org/
    """

    _graph_loading_locator = (By.CSS_SELECTOR, '#homepage-graph .loading')
    _release_channels_locator = (By.CSS_SELECTOR, '.release_channel')
    _last_release_channel_locator = (By.CSS_SELECTOR, '#release_channels .release_channel:last-child')

    def __init__(self, testsetup, product=None):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)

        if product is None:
            self.selenium.get(self.base_url)
        self.wait_for_page_to_load()

    def wait_for_page_to_load(self):
        Wait(self.selenium, self.timeout).until(
            lambda s: not self.is_element_present(*self._graph_loading_locator))
        return self

    def click_last_product_top_crashers_link(self):
        return self.ReleaseChannels(
            self.testsetup, self.selenium.find_element(*self._last_release_channel_locator)
        ).click_top_crasher()

    @property
    def release_channels(self):
        return [self.ReleaseChannels(self.testsetup, element) for element in self.selenium.find_elements(*self._release_channels_locator)]

    class ReleaseChannels(CrashStatsBasePage):

        _release_channel_header_locator = (By.TAG_NAME, 'h4')
        _top_crashers_link_locator = (By.LINK_TEXT, 'Top Crashers')

        def __init__(self, testsetup, element):
            CrashStatsBasePage.__init__(self, testsetup)
            self._root_element = element

        @property
        def product_version_label(self):
            return self._root_element.find_element(*self._release_channel_header_locator).text

        def click_top_crasher(self):
            self._root_element.find_element(*self._top_crashers_link_locator).click()
            from pages.crash_stats_top_crashers_page import CrashStatsTopCrashers
            return CrashStatsTopCrashers(self.testsetup)
