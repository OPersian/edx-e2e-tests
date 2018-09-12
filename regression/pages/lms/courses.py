from bok_choy.page_object import PageObject

from regression.pages.lms import LOGIN_BASE_URL


class Courses(PageObject):

    url = LOGIN_BASE_URL + '/courses'

    def is_browser_on_page(self):
        return self.q(css='.find-courses').present

    def search_course(self, name):
        self.q(css='#discovery-input').fill(name)
        self.q(css="button.discovery-submit").click()

    @property
    def search_results(self):
        return self.q(css='.courses-listing-item')
