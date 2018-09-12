"""
Course about page
"""
from selenium.common.exceptions import NoSuchElementException

from edxapp_acceptance.pages.lms.course_about import CourseAboutPage
from regression.pages.lms import LOGIN_BASE_URL


class CourseAboutPageExtended(CourseAboutPage):
    """
    This class is an extended class of CourseAboutPage,

    """

    def is_browser_on_page(self):
        return self.q(css='.about').present

    @property
    def url(self):
        return "{}/courses/{}/{}".format(
            LOGIN_BASE_URL, self.course_id, self.url_path)

    def course_enrollment(self):
        return self.q(css='.theme-about_btn-holder')
    
    @property
    def enroll_button(self):
        selector = None
        try:
            selector = self.browser.find_element_by_css_selector(css_selector='.theme-about_btn-holder a')
        except NoSuchElementException:
            selector = self.browser.find_element_by_css_selector(css_selector='.main-cta a')
        return selector

    def view_course_button(self):
        return self.q(css='a[class^="theme-btn-2"]')

    def register(self):
        """
        Get the enroll button and lick on it
        """
        self.q(css='a.register').first.click()
