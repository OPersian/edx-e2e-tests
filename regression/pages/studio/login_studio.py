"""
Studio login page
"""
from edxapp_acceptance.pages.studio.login import LoginPage
from regression.pages.studio import LOGIN_BASE_URL


class StudioLogin(LoginPage):
    """
    This class is an extended class of LoginPage.
    """
    url = LOGIN_BASE_URL + '/signin'

    def is_browser_on_page(self):
        """
        Checks if we are on the correct page
        """
        return self.q(css='#login_form').present

