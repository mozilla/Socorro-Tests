#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import requests

from unittestzero import Assert


class TestDownload(object):

    _csv_urls = [
        '/topcrasher/products/Firefox/versions/25.0a1/crash_type/report/os_name/browser?format=csv'
    ]

    @pytest.mark.nondestructive
    @pytest.mark.skip_selenium
    @pytest.mark.parametrize(('url'), _csv_urls)
    def test_that_csv_urls_are_valid(self, mozwebqa, url):
        url = mozwebqa.base_url + url
        request = requests.head(url)
        Assert.equal(requests.codes.ok, request.status_code,
                     'Error downloading the file at %s. Status code: %s.' %
                     (url, request.status_code))
        Assert.equal('text/csv', request.headers['content-type'])
        Assert.greater(request.headers['content-length'], '1000',
                       'The content length of the file, %s, is less than 1000 bytes.' %
                       request.headers['content-length'])
