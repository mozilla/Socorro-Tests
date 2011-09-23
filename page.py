#!/usr/bin/env python
#
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
# The Original Code is Firefox Input
#
# The Initial Developer of the Original Code is
# Mozilla Corp.
# Portions created by the Initial Developer are Copyright (C) 2010
# the Initial Developer. All Rights Reserved.
#
# Contributor(s): Vishal
#                 Dave Hunt
#                 David Burns
#                 Matt Brandt <mbrandt@mozilla.com>
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
'''
Created on Jun 21, 2010

'''
import re
import time
import base64
from distutils.version import LooseVersion
from types import StringType, IntType

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
        self.selenium.click("link=%s" % link)
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
                raise Exception(element + " is not visible")

    def wait_for_element_not_visible(self, element):
        count = 0
        while self.is_element_visible(element):
            time.sleep(1)
            count += 1
            if count == self.timout / 1000:
                raise Exception(element + " is still visible")

    def wait_for_page(self, url_regex):
        count = 0
        while (re.search(url_regex, self.selenium.get_location(), re.IGNORECASE)) is None:
            time.sleep(1)
            count += 1
            if count == self.timeout / 1000:
                raise Exception("Sites Page has not loaded")

    class Version(LooseVersion):

    #Overrides the LooseVersion class to better use our version numers

        def parse(self, vstring):
            self.vstring = vstring
            components = filter(lambda x: x and x != '.', self.component_re.split(vstring))
            for i in range(len(components)):
                try:
                    components[i] = int(components[i])
                except ValueError:
                    components[i] = components[i]

            self.version = components

        def __cmp__(self, other):
            if isinstance(other, StringType):
                other = LooseVersion(other)

            a = self.version
            b = other.version
            while len(a) < len(b):
                a.append(0)
            while len(b) < len(a):
                b.append(0)

            for i in range(len(a)):

                if not isinstance(a[i], IntType) and isinstance(b[i], IntType):
                    return -1

                if not isinstance(b[i], IntType) and isinstance(a[i], IntType):
                    return 1

            #If the element from list A is greater than B,
            #versionA is greater than versionB and visa versa.
            #If they are equal, go to the next element.
                if a[i] > b[i]:
                    return 1
                elif b[i] > a[i]:
                    return -1
            #If we reach this point, the versions are equal
            return 0
