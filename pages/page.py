#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException

http_regex = re.compile('https?://((\w+\.)+\w+\.\w+)')


class Page(object):
    '''
    Base class for all Pages
    '''

    def __init__(self, testsetup):
        '''
        Constructor
        '''
        self.testsetup = testsetup
        self.selenium = testsetup.selenium
        self.base_url = testsetup.base_url
        self.timeout = testsetup.timeout

    @property
    def is_the_current_page(self):
        if self._page_title:
            WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)

        assert self.selenium.title == self._page_title
        return True

    def get_url_current_page(self):
        WebDriverWait(self.selenium, self.timeout).until(lambda s: self.selenium.title)
        return self.selenium.current_url

    def is_element_present(self, *locator):
        self.selenium.implicitly_wait(0)
        try:
            self.selenium.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def is_element_visible(self, parent_element, *locator):
        self.selenium.implicitly_wait(0)
        try:
            if parent_element is not None:
                element = parent_element.find_element(*locator)
                return element.is_displayed()
            else:
                element = self.selenium.find_element(*locator)
                return element.is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False
        finally:
            # set back to where you once belonged
            self.selenium.implicitly_wait(self.testsetup.default_implicit_wait)

    def return_to_previous_page(self):
        self.selenium.back()
