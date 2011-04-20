import pytest
import py
from selenium import selenium

def pytest_runtest_setup(item):
    item.host = item.config.option.hub
    item.browser = item.config.option.browser
    item.port = item.config.option.port
    SeleniumSetup.base_url = item.config.option.site

    if not 'skip_selenium' in item.keywords:
        SeleniumSetup.selenium = selenium(item.host, item.port,
            item.browser, SeleniumSetup.base_url)
    
        SeleniumSetup.selenium.start()

def pytest_runtest_teardown(item):
    if not 'skip_selenium' in item.keywords:
        SeleniumSetup.selenium.stop()

def pytest_funcarg__seleniumsetup(request):
    return SeleniumSetup(request)


def pytest_addoption(parser):
    parser.addoption("--hub", action="store", default="localhost",
        help="specify where to run")
    parser.addoption("--port", action="store", default="4444",
        help="specify where to run")
    parser.addoption("--browser", action="store", default="*firefox",
        help="specify the browser")
    parser.addoption("--site", action="store", default=None,
        help="specify the AUT")

class SeleniumSetup:
    def __init__(self, request):
        self.request = request

