"""
Utility functions for lms page objects.
"""
from opaque_keys.edx.locator import CourseLocator


def get_course_key(course_info, module_store='split'):
    """
    Returns the course key based upon course info passed.
    Course key depends upon the module store passed. The default
    module store is 'split'.
    """
    course_key = CourseLocator(
        course_info['org'],
        course_info['number'],
        course_info['run'],
        deprecated=(module_store == 'split') #'draft'
    )
    return unicode(course_key)
