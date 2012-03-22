Socorro Tests
===================

Automated tests for the Socorro web application.

Running Tests
-------------

### Java
You will need a version of the [Java Runtime Environment][JRE] installed

[JRE]: http://www.oracle.com/technetwork/java/javase/downloads/index.html

### Python
Before you're able to run these tests, you'll need to have Python 2.6 installed.

Run:

    easy_install pip

followed by:

    sudo pip install -r requirements.txt

__note__

If you are running on Ubuntu/Debian, you will need to first do:

    sudo apt-get install python-setuptools

to install the required Python libraries.

### Selenium
Once this is all set up, you will need to download and start a Selenium server. You can download the latest Selenium server from [here][Selenium Downloads]. The filename will be something like 'selenium-server-standalone-2.x.x.jar',
where "2.x.x" is the latest shipping version #.

To start the Selenium server run the following command:

    java -jar ~/Downloads/selenium-server-standalone-2.x.x.jar

Change the path/name to the downloaded Selenium-server file.

[Selenium Downloads]: http://code.google.com/p/selenium/downloads/list

### Running tests locally

1. To run tests locally, simply call py.test from the Socorro-tests directory
2. You should specify the following argument for Selenium RC: --api=rc
3. The base URL should be a valid instance of crash-stats-dev: --baseurl=http://crash-stats-dev.allizom.org

    py.test --api=rc --baseurl=http://example.com

For other instructions, type py.test --help.


Writing Tests
-------------

If you want to get involved and add more tests, then there are just a few things
we'd like to ask that you do:

1. Use the [template files][GitHub Templates] for all new tests and page objects
2. Follow our simple [style guide][Style Guide]
3. Fork this project with your own GitHub account
4. Make sure all tests are passing, and submit a pull request with your changes

[GitHub Templates]: https://github.com/mozilla/mozwebqa-test-templates
[Style Guide]: https://wiki.mozilla.org/QA/Execution/Web_Testing/Docs/Automation/StyleGuide

License
-------
This software is licensed under the [MPL] 2.0:

    This Source Code Form is subject to the terms of the Mozilla Public
    License, v. 2.0. If a copy of the MPL was not distributed with this
    file, You can obtain one at http://mozilla.org/MPL/2.0/.

[MPL]: http://www.mozilla.org/MPL/2.0/
