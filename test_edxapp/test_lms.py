"""
E2E tests for the LMS.
"""


from e2e_framework.web_app_test import WebAppTest
from credentials import TestCredentials
from fixtures import UserFixture
from pages.lms.login import LoginPage
from pages.lms.find_courses import FindCoursesPage
from pages.lms.info import InfoPage
from pages.lms.course_about import CourseAboutPage
from pages.lms.register import RegisterPage
from pages.lms.dashboard import DashboardPage
from pages.lms.course_info import CourseInfoPage
from pages.lms.tab_nav import TabNavPage
from pages.lms.progress import ProgressPage


# The demo course is installed by default in the CI environment
DEMO_COURSE_ID = 'edX/Open_DemoX/edx_demo_course'
DEMO_COURSE_TITLE = 'Open_DemoX edX Demonstration Course'


class LoggedOutTest(WebAppTest):
    """
    Smoke test for pages in the LMS
    that are visible when logged out.
    """


    @property
    def page_object_classes(self):
        return [
            InfoPage, FindCoursesPage, LoginPage,
            CourseAboutPage, RegisterPage, DashboardPage
        ]

    def test_find_courses(self):
        self.ui.visit('lms.find_courses')

    def test_info(self):

        for section_name in InfoPage.sections():
            self.ui.visit('lms.info', section=section_name)

    def test_register(self):

        # Visit the main page with the list of courses
        self.ui.visit('lms.find_courses')

        # Expect that the demo course exists
        course_ids = self.ui['lms.find_courses'].course_id_list()
        self.assertIn(DEMO_COURSE_ID, course_ids)

        # Go to the course about page
        self.ui['lms.find_courses'].go_to_course(DEMO_COURSE_ID)

        # Click the register button
        self.ui['lms.course_about'].register()

        # Fill in registration info and submit
        self.ui['lms.register'].provide_info(TestCredentials())
        self.ui['lms.register'].submit()

        # We should end up at the dashboard
        # Check that we're registered for the course
        course_names = self.ui['lms.dashboard'].available_courses()
        self.assertIn(DEMO_COURSE_TITLE, course_names)


class LoggedInTest(WebAppTest):
    """
    Tests that log in as a user.
    """

    @property
    def page_object_classes(self):
        return [LoginPage, DashboardPage, CourseInfoPage, TabNavPage, ProgressPage]

    @property
    def fixtures(self):
        """
        Create a user account so we can log in.
        The user account is automatically registered for the demo course.
        """
        self.username = 'test_' + self.unique_id
        self.email = '{0}@example.com'.format(self.username)
        self.password = 'password'

        return [UserFixture(self.username, self.email, self.password, course=DEMO_COURSE_ID)]

    def setUp(self):
        """
        Each test begins after registering for the demo course and logging in.
        """
        super(LoggedInTest, self).setUp()
        self._login()

    def test_course_info(self):
        """
        Navigate to the course info page.
        """
        self.ui['lms.dashboard'].view_course(DEMO_COURSE_ID)

        # Expect just one update
        num_updates = self.ui['lms.course_info'].num_updates()
        self.assertEqual(num_updates, 1)

        # Expect a link to the demo handout pdf
        handout_links = self.ui['lms.course_info'].handout_links()
        self.assertEqual(len(handout_links), 1)
        self.assertIn('demoPDF.pdf', handout_links[0])

    def test_progress(self):
        """
        Navigate to the progress page.
        """
        self.ui['lms.dashboard'].view_course(DEMO_COURSE_ID)
        self.ui['lms.tab_nav'].go_to_tab('Progress')

        # We haven't answered any problems yet, so assume scores are zero
        CHAPTER = 'Example Week 1: Getting Started'
        SECTION = 'Homework - Question Styles'
        EXPECTED_SCORES = [(0, 1), (0, 1), (0, 3), (0, 1), (0, 1), (0, 3), (0, 1)]

        actual_scores = self.ui['lms.progress'].scores(CHAPTER, SECTION)
        self.assertEqual(actual_scores, EXPECTED_SCORES)

    def _login(self):
        """
        Log in as the test user and navigate to the dashboard,
        where we should see the demo course.
        """
        self.ui.visit('lms.login')
        self.ui['lms.login'].login(self.email, self.password)
        course_names = self.ui['lms.dashboard'].available_courses()
        self.assertIn(DEMO_COURSE_TITLE, course_names)
