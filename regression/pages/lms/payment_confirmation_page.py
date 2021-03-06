"""
Payment confirmation page.
"""
from bok_choy.page_object import PageObject


class PaymentConfirmationPage(PageObject):
    """
    Payment confirmation page
    """
    url = None

    def is_browser_on_page(self):
        return self.q(
            css='.payment-confirmation-step article'
        ).visible
