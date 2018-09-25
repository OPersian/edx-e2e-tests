"""
Import course page
"""
from edxapp_acceptance.pages.studio.import_export import (
    ImportMixin
)
from edxapp_acceptance.pages.common.utils import click_css

from regression.pages.studio.course_page_studio import CoursePageExtended
from regression.pages import UPLOAD_FILE_DIR
from regression.tests.helpers.utils import get_url


class ImportCoursePageExtended(ImportMixin, CoursePageExtended):
    """
    Extended course import page.
    """

    url_path = 'import'

    @property
    def url(self):
        """
        Construct a URL to the page within the course.
        """
        return get_url(self.url_path, self.course_info)


    def upload_tarball(self, tarball_filename):
        """
        Upload a tarball to be imported.
        """
        asset_file_path = UPLOAD_FILE_DIR + "/" + tarball_filename
        # Make the upload elements visible to the WebDriver.
        self.browser.execute_script(
            '$(".file-name-block").show();$(".file-input").show()'
        )
        # Upload the file.
        self.q(css='input[type="file"]')[0].send_keys(asset_file_path)
        # Upload the same file again. Reason behind this is to decrease the
        # probability or fraction of times the failure occur. Please be
        # noted this doesn't eradicate the root cause of the error, it
        # just decreases to failure rate to minimal.
        # Jira ticket reference: TNL-4191.
        self.q(css='input[type="file"]')[0].send_keys(asset_file_path)
        # Some of the tests need these lines to pass so don't remove them.
        self._wait_for_button()
        click_css(self, '.submit-button', require_notification=False)
