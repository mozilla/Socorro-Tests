'''
Acceptance tests for /daily ADU and Crash Count reports
'''
from selenium import selenium
import unittest

import daily_config as config

#1234567890123456789012345678901234567890123456789012345678901234567890123456789
class TestDaily(unittest.TestCase):
    def setUp(self):
        self.selenium = selenium(config.selenium_host, config.selenium_port,
                                 config.selenium_browser_start_command,
                                 config.selenium_browser_url)
        self.selenium.start() 
        self.selenium.set_timeout(config.selenium_timeout)

    def tearDown(self):
        self.selenium.stop()
        pass

    def testDailyReport(self):
        sel = self.selenium
        base_url = sel.browserURL
        sel.open("%s/daily" % base_url)
        
        self.checkPrefill()
        self.checkBadVersion()
        self.check3_0_10_Version()
        
    def checkPrefill(self):
        sel = self.selenium
        self.assertTrue(sel.is_text_present('Crashes per Active Daily User'))
        self.assertTrue(sel.get_value('css=#version1').strip(), "We prefill the form")
        self.assertTrue(sel.get_value('css=#version2').strip())
        
    def checkBadVersion(self):
        sel = self.selenium
        sel.type('css=#version1', "3.0.10")
        sel.type('css=#version2', "12345")
        sel.type('css=#version3', "")
        sel.type('css=#version4', "")
        sel.click('css=#daily_search_version_form_submit')
        sel.wait_for_page_to_load(config.selenium_timeout)
        self.assertFalse(sel.is_text_present("No Active Daily User crash data is available for this report"),
                         "Bug#568322 Ignore 12345")
        
    def check3_0_10_Version(self):
        sel = self.selenium
        sel.type('css=#version1', "3.0.10")
        sel.type('css=#version2', "3.5b4")
        sel.type('css=#version3', "")
        sel.type('css=#version4', "")
        sel.type('css=input[name="hang_type"]', 'any')
        sel.type('css=input[name="date_start"]', "2009-06-01")
        sel.type('css=input[name="date_end"]', "2009-06-20")        
        sel.click('css=#daily_search_version_form_submit')
        sel.wait_for_page_to_load(config.selenium_timeout)
        
        self.assertEquals('Crashes', sel.get_table('crash_data.1.0'))
        self.assertEquals('3.0.10', sel.get_table('crash_data.0.1'))
        all_crash_3_0_10 = self.to_int(sel.get_table('crash_data.3.1'))
        self.assertTrue(8000 < all_crash_3_0_10,
                        "The second row of 3.0.10 crashes should be 10,228 ish, but was %s" % sel.get_table('crash_data.3.1'))
        adu_6_20 = self.to_int(sel.get_table('crash_data.3.2'))
        self.assertTrue(5000000 < adu_6_20,
                        "The second row of 3.0.10 adu should be 6,786,543 ish, but was %s" % sel.get_table('crash_data.3.2'))
        
        # Knock out Windows
        sel.click('os_Windows_check')
        sel.click('css=#daily_search_version_form_submit')
        sel.wait_for_page_to_load(config.selenium_timeout)
        
        self.assertEquals('Crashes', sel.get_table('crash_data.1.0'))
        self.assertEquals('3.0.10', sel.get_table('crash_data.0.1'))
        no_win_crash_3_0_10 = self.to_int(sel.get_table('crash_data.3.1'))
        print "No Windows is %s" % no_win_crash_3_0_10 
        self.assertTrue(all_crash_3_0_10 > no_win_crash_3_0_10,
                        "Searching for Mac and Linux should give us fewer crashes, but all=%s and now=%s" % (all_crash_3_0_10, no_win_crash_3_0_10))
        no_win_adu_6_20 = self.to_int(sel.get_table('crash_data.3.2'))
        self.assertTrue(no_win_adu_6_20 < adu_6_20,
                          "Searching for Mac and Linux should give us lower adu numbers, but all=%s and now=%s" % (no_win_adu_6_20, adu_6_20))
        
        """ TODO: Why doesn't this work? $(el) is undefined
        print sel.get_eval('var c = [];
        $('.crash_data tr td:nth-child(2)', window.document).each(function(i, el){          
          c.push($(el).text());  
        }); c;')"""
        
    def to_int(self, a):
        """ Given a string like '3,120,123; returns an integer 3120123 """
        return int(a.replace(',',''))
        
    def pt(cell):
        """ Useful for exploring a table through selenium's eyes """
        print "%s = %s" % (cell, sel.get_table("crash_data.%s" % cell))
if __name__ == "__main__":
    unittest.main()
