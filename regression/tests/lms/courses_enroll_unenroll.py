import os
from time import sleep
from bok_choy.web_app_test import WebAppTest

from regression.pages.lms.login_lms import LmsLogin
from regression.pages.lms.dashboard_lms import DashboardPageExtended
from regression.pages.lms.courses import Courses
from regression.pages.lms.course_about_page import CourseAboutPageExtended

COURSE_DISPLAY_NAME = os.environ.get('COURSE_DISPLAY_NAME', 'edX Demonstration Course')


class EnrollUnenroll(WebAppTest):

    DEMO_COURSE_USER = os.environ.get('USER_LOGIN_EMAIL')
    DEMO_COURSE_PASSWORD = os.environ.get('USER_LOGIN_PASSWORD')

    def setUp(self):
        """
        Initialize the page object
        """
        super(EnrollUnenroll, self).setUp()
        self.browser.maximize_window()
        self.login_page = LmsLogin(self.browser)
        self.dashboard_ext = DashboardPageExtended(self.browser)
        self.courses_page = Courses(self.browser)

    def test_flow(self):
        """
        Test flow for checking enroll/unenroll courses
        """
        # Step 1 - Login
        self.login_page.visit()
        self.login_page.login(self.DEMO_COURSE_USER, self.DEMO_COURSE_PASSWORD)
        self.assertEqual(
            self.login_page.q(
                css='.wrapper-header-courses .header-courses').text[0].lower(),
            'my courses',
            msg='User not logged in as expected.')

        # Step 2 - Go to courses page, search course
        self.courses_page.visit()
        self.courses_page.browser.refresh()
        self.courses_page.is_browser_on_page()
        self.courses_page.wait_for_page()
        self.courses_page.search_course(COURSE_DISPLAY_NAME)
        sleep(1)
        self.assertEquals(self.courses_page.q(css='span.query').text[0][1:-1], COURSE_DISPLAY_NAME)
        self.courses_page.wait_for_page()

        # Step 3 - Learn More
        self.courses_page.q(css='.courses-listing-item').first.click()
        sleep(1)
        course_id = self.browser.current_url.split('/')[-2]
        course_about_page = CourseAboutPageExtended(self.browser, course_id)

        # Step 4 -  Enroll to course
        course_about_page.register()

        # Step 5 - dashboard
        self.dashboard_ext.wait_for_page()

        # Step 6 - Unenrollment
        self.dashboard_ext.unenrollment(course_id)

        # Step 7 - Courses page, search courses again
        self.courses_page.visit()
        self.courses_page.browser.refresh()  # to avoid errors with search courses in future actions
        self.courses_page.wait_for_page()
        self.courses_page.is_browser_on_page()
        self.courses_page.search_course(COURSE_DISPLAY_NAME)
        sleep(1)
        self.assertEquals(self.courses_page.q(css='span.query').text[0][1:-1], COURSE_DISPLAY_NAME)
        self.courses_page.wait_for_page()

        # Step 8 - Learn More
        self.courses_page.q(css='.courses-listing-item').first.click()
        course_id_1 = self.courses_page.browser.current_url.split('/')[-2]
        course_about_page = CourseAboutPageExtended(self.browser, course_id_1)
        course_about_page.visit()
        course_about_page.wait_for_page()
        course_about_page.is_browser_on_page()

        # 9 step - Verify the Enroll button is dispayed again on the /about page of course
        self.assertEquals(course_about_page.browser.find_element_by_css_selector('a.register').text.lower(), 'enroll in demox')
