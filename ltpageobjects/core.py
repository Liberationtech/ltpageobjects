from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

def strip_trailing_slash(url):
    """
    Return given url without any trailing slashes

    """
    if url[-1] == "/":
        return url[:-1]
    else:
        return url

class PageObject:
    base_url = None
    url = None

    def __init__(self, driver, site):
        self.driver = driver
        self.site = site

        if not self.__class__.base_url:
            raise Exception

        if not self.__class__.url:
            raise Exception

        #self.url = self.__class__.base_url + self.__class__.url

    def get(self):
        self.driver.get(self.url)

    def wait(self, locator, timeout=10000):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))


    def dump_source(self, filename):
        """ put the source of the page on file """
        fh = open(filename, 'w')
        fh.write(self.driver.page_source.encode("UTF-8"))
        fh.close()

    def full_url(self):
        return self.__class__.base_url + self.__class__.url

    def find_element_by_link(self,link):
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

    def click(self, link):
        """
        link is a bound callable that returns an element
        click a link and return a new page object
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


    def assert_element_exists(self, testcase, element):
        """
        testcase is the testcast we're calling from
        element is a bound method that should return an element
        """
        testcase.assertTrue(element() != None)

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

        #Loop through pages in site
        for page_class in self.__class__.pages:

            #Construct a new page for each page class
            newpage = page_class(oldpage.driver, self)

            #If the url of this new page corresponds to the url
            #of the driver of the old page return the new page object
            #this will be the case when we have clicked a link on the old page pointing
            #to the url of the new page
            if strip_trailing_slash(newpage.full_url()) == strip_trailing_slash(oldpage.driver.current_url):
                return newpage

        #if we get here our tests are broken
        #TODO make a custom exception here and raise it
        assert False
