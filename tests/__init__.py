import unittest
import ltpageobjects
from mock import Mock
from mock import PropertyMock


class TestPageObject(ltpageobjects.PageObject):
    base_url = "http://127.0.0.1"
    url = "/hello"

class TestAnotherPageObject(ltpageobjects.PageObject):
    base_url = "http://127.0.0.1"
    url = "/world"

class TestSiteObject(ltpageobjects.SiteObject):
    pages = [TestPageObject, TestAnotherPageObject]


class TestPageObjectAtOtherSite(ltpageobjects.PageObject):
    base_url = "http://example.com"
    url = "/foo"

class TestAnotherPageObjectAtOtherSite(ltpageobjects.PageObject):
    base_url = "http://example.com"
    url = "/bar"

class TestOtherSiteObject(ltpageobjects.SiteObject):
    pages = [TestPageObjectAtOtherSite, TestAnotherPageObjectAtOtherSite]



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

    def test_create_page(self):
        page = TestPageObject(self.mockdriver, self.site)


    def test_find_element(self):
        page = TestPageObject(self.mockdriver, self.site)
        value = page.find_element_by_id("hello")

class ClickTest(unittest.TestCase):
    def setUp(self):
        self.site = TestSiteObject()
        self.mockdriver = Mock()
        type(self.mockdriver).current_url = PropertyMock(return_value="http://127.0.0.1/world")

    def test_click(self):
        """
        When we click the link we get to the other page
        """

        page_hello = TestPageObject(self.mockdriver, self.site)
        page_world = TestAnotherPageObject(self.mockdriver, self.site)

        newpage = page_hello.click(Mock())
        self.assertEqual(page_world.full_url(), newpage.full_url())


class MultiSiteClickTest(unittest.TestCase):

    def setUp(self):
        self.first_site = TestSiteObject()
        self.second_site = TestOtherSiteObject()
        self.mockdriver = Mock()
        type(self.mockdriver).current_url = PropertyMock(return_value="http://example.com/foo")

    def test_click_outbound(self):
        """
        When we click the outbound link we get back a page that is part of the other site
        """

        page_first_site = TestPageObject(self.mockdriver, self.first_site)
        page_other_site = TestPageObjectAtOtherSite(self.mockdriver, self.second_site)

        newpage = page_first_site.click_outbound(Mock(), self.second_site)

        self.assertEqual(newpage.site, self.second_site)
        self.assertEqual(newpage.full_url(), page_other_site.full_url())


if __name__ == '__main__':
    unittest.main()