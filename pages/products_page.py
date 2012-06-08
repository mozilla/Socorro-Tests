#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By

from pages.base_page import CrashStatsBasePage


class ProductsLinksPage(CrashStatsBasePage):

    _heading_locator = (By.CSS_SELECTOR, '.title h2')

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.selenium.get(self.base_url + '/products/')

    @property
    def page_heading(self):
        return self.selenium.find_element(*self._heading_locator).text

    def click_product(self, product):
        self.selenium.find_element(By.LINK_TEXT, product).click()
        from pages.home_page import CrashStatsHomePage
        return CrashStatsHomePage(self.testsetup, product)
