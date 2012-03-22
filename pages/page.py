#!/usr/bin/env python
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
'''
Created on Jun 21, 2010

'''
import re
import time
import base64

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
        page_title = self.selenium.get_title()
        if not page_title == self._page_title:
            try:
                raise Exception("Expected page title to be: '" + self._page_title + "' but it was: '" + page_title + "'")
            except Exception:
                raise Exception('Expected page title does not match actual page title.')
        else:
            return True

    def click_link(self, link, wait_flag=False):
        self.selenium.click('link=%s' % link)
        if(wait_flag):
            self.selenium.wait_for_page_to_load(self.timeout)

    def click(self, locator, wait_flag=False):
        self.selenium.click(locator)
        if(wait_flag):
            self.selenium.wait_for_page_to_load(self.timeout)

    def type(self, locator, str):
        self.selenium.type(locator, str)

    def click_button(self, button, wait_flag=False):
        self.selenium.click(button)
        if(wait_flag):
            self.selenium.wait_for_page_to_load(self.timeout)

    def get_url_current_page(self):
        return(self.selenium.get_location())

    def is_element_present(self, locator):
        return self.selenium.is_element_present(locator)

    def is_element_visible(self, locator):
        return self.selenium.is_visible(locator)

    def is_text_present(self, text):
        return self.selenium.is_text_present(text)

    def refresh(self):
        self.selenium.refresh()
        self.selenium.wait_for_page_to_load(self.timeout)

    def wait_for_element_present(self, element):
        count = 0
        while not self.is_element_present(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                raise Exception(element + ' has not loaded')

    def wait_for_element_visible(self, element):
        self.wait_for_element_present(element)
        count = 0
        while not self.is_element_visible(element):
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                raise Exception(element + ' is not visible')

    def wait_for_element_not_visible(self, element):
        count = 0
        while self.is_element_visible(element):
            time.sleep(1)
            count += 1
            if count == self.timout / 1000:
                raise Exception(element + ' is still visible')

    def wait_for_page(self, url_regex):
        count = 0
        while (re.search(url_regex, self.selenium.get_location(), re.IGNORECASE)) is None:
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                raise Exception('Sites Page has not loaded')
