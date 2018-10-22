# available since 2.26.0
from selenium.webdriver.support import expected_conditions as EC
# available since 2.4.0
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import re

# TODO Move to incorporating urls.py from current project
# pick up url NAMES and also use the pattern matching from there
# on top of that allow users to define new sites using the same mechanism


class PageNotFoundException(Exception):
    pass


class MissingBaseUrlException(Exception):
    pass


class MissingUrlException(Exception):
    pass


def strip_trailing_slash(url):
    """
    Return given url without any trailing slashes
    """
    if url[-1] == "/":
        return url[:-1]
    else:
        return url


class PageObject:
    url = None
    url_pattern = None

    def __init__(self, driver, site, base_url=None):
        self.driver = driver
        self.site = site

        # If we have not set the base_url class attribute, then use
        # value passed in to the constructor

        if not hasattr(self.__class__, "base_url"):
            self.__class__.base_url = base_url

    def __getattr__(self, name):
        if name == "full_url":
            full_url = self.__class__.base_url + self.__class__.url
            return full_url

    def get(self):
        print "self.url: {}".format(self.url)
        print "self.full_url: {}".format(self.full_url)
        # self.driver.get(self.url)
        self.driver.get(self.full_url)

    def wait(self, locator, timeout=10000):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator))

    def dump_source(self, filename):
        """ put the source of the page on file """
        fh = open(filename, 'w')
        fh.write(self.driver.page_source.encode("UTF-8"))
        fh.close()

    def find_element_by_link(self, link):
        return self.find_elements_by_xpath("//a[@href='{0}']".format(link))[0]

    def find_elements_by_class_name(self, clsname):
        return self.driver.find_elements_by_class_name(clsname)

    def find_elements_by_xpath(self, xpath):
        return self.driver.find_elements_by_xpath(xpath)

    def find_element_by_id(self, theid):
        return self.driver.find_element_by_id(theid)

    def find_element_by_css_selector(self, selector):
        return self.driver.find_element_by_css_selector(selector)

    def find_elements(self, byby, argument):
        return self.driver.find_elements(byby, argument)

    def fill_field(self, field, value, clear=True):
        """
        field is a callable on our PageObject that returns a field
        value is a string to put in that field
        """
        element = field()
        if clear:
            element.clear()
        element.send_keys(value)

    def select_by_visible_text(self, field, text):
        """
        field is a callable on our PageObject that returns a field
        text is the

        """
        select = Select(field())
        select.select_by_visible_text(text)

    def select_by_value(self, field, value):
        """
        field is a callable on our PageObject that returns a field
        text is the

        """
        select = Select(field())
        select.select_by_value(value)

    def click(self, link):
        """
        link is a bound callable that returns an element
        click a link and return a new page object

        if url_pattern is None, we require strict url matching
        if url_pattern is set to a regexp string we require a match of that
        """
        link().click()
        return self.site.newpage(self)

    def click_outbound(self, link, site):
        """
        link is a bound callable that returns an element

        click a link that points to a different site and return a new page object
        """
        link().click()
        return site.newpage(self)


    def click_outbound_wait_for_id(self, link, site, wait_for_id):
        """
        link is a bound callable that returns an element

        click a link that points to a different site and return a new page object
        
        do not return until <wait_for_id> is available on page

        """
        link().click()
        newpage = site.newpage(self)
        newpage.wait(wait_for_id)
        return newpage

    
    def assert_element_exists(self, testcase, element):
        """
        testcase is the testcast we're calling from
        element is a bound method that should return an element
        """

        print "in assert_element"

        the_element = element()
        print the_element
        testcase.assertTrue(element() != None)
        print "leaving assert element"

    def page_source(self):
        return self.driver.page_source


class SiteObject:
    pages = []

    def newpage(self, oldpage):
        """
        given an old page,
        look through the urls in the pages collection, if anyone matches thats where
        we're at now. Return a new page object instantiated with that class
        """

        url_of_page_we_just_navigated_to = oldpage.driver.current_url
        print "uopwjnt: ", url_of_page_we_just_navigated_to

        # import pdb
        # pdb.set_trace()
        site_class = self.__class__

        # Loop through pages in site

        for page_class in site_class.pages:

            # Construct a new page for each page class
            newpage_candidate = page_class(
                oldpage.driver, self, base_url=oldpage.__class__.base_url)
            if newpage_candidate.__class__.url != None:

                # If the url of this new page corresponds to the url
                # of the driver of the old page return the new page object
                # this will be the case when we have clicked a link on the old page pointing
                # to the url of the new page
                if strip_trailing_slash(newpage_candidate.full_url) == strip_trailing_slash(url_of_page_we_just_navigated_to):
                    return newpage_candidate
        # Loop through the pages in the site again, this time looking for
        # pattern matches
        for page_class in site_class.pages:
            newpage_candidate = page_class(oldpage.driver, self)
            if newpage_candidate.__class__.url_pattern:
                print newpage_candidate.__class__.url_pattern

                compiled_regexp = re.compile(
                    newpage_candidate.__class__.url_pattern)
                match = compiled_regexp.search(
                    url_of_page_we_just_navigated_to)
                if match:
                    newpage_candidate.full_url = url_of_page_we_just_navigated_to
                    return newpage_candidate

        # if we get here our tests are broken
        # TODO make a custom exception here and raise it

        raise PageNotFoundException({"message": "The requested page we and url of [{0}] could not be found within the supplied site object".format(
            url_of_page_we_just_navigated_to)})
