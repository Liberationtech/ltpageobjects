import unittest
import sys
import ltpageobjects
from mock import MagicMock
from mock import Mock
from mock import patch
from mock import PropertyMock


class TestPageObject(ltpageobjects.PageObject):
    """
    Inherit from PageObject
    """
    base_url = "http://127.0.0.1"
    url = "/hello"

class TestAnotherPageObject(ltpageobjects.PageObject):
    """

    """
    base_url = "http://127.0.0.1"
    url = "/world"

class TestSiteObject(ltpageobjects.SiteObject):
    """
    Inherit from SiteObject
    """
    pages = [TestPageObject, TestAnotherPageObject]


class CreateSiteTest(unittest.TestCase):

    def test_create_site(self):
        """
        Instantiate TestSiteObject
        """
        site = TestSiteObject()
        self.assertIsInstance(site, TestSiteObject)


class CreatePageTest(unittest.TestCase):

    def setUp(self):
        self.site = ltpageobjects.SiteObject()
        #self.mockdriver = ""
        self.mockdriver = Mock(return_value='an_element')
        current_url = PropertyMock(return_value="http://127.0.0.1/world")
        type(self.mockdriver).current_url = current_url
        #self.mockdriver.current_url = "http://127.0.0.1/world"
        print self.mockdriver.current_url

    def test_create_page(self):
        page = TestPageObject(self.mockdriver, self.site)


    def test_find_element(self):
        page = TestPageObject(self.mockdriver, self.site)
        value = page.find_element_by_id("hello")
        print self.mockdriver.method_calls

class ClickTest(unittest.TestCase):
    def setUp(self):
        self.site = TestSiteObject()
        self.mockdriver = Mock()
        type(self.mockdriver).current_url = PropertyMock(return_value="http://127.0.0.1/world")

    def test_click(self):
        """
        When we click the link we get to the other page
        """

        site = TestSiteObject()
        page_hello = TestPageObject(self.mockdriver, self.site)
        page_world = TestAnotherPageObject(self.mockdriver, self.site)

        newpage = page_hello.click(Mock())
        self.assertEqual(page_world.full_url(), newpage.full_url())

if __name__ == '__main__':
    unittest.main()