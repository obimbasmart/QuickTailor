""" @given: a flask app running
    @then: validate that email service is working properly
"""

from email_service.sendgrid import send_email

def test_email(new_user):
    res_status_code = send_email(
        "Testing email service",
        'This is a dummy test for testing email service',
        [new_user.email]
    )

    assert res_status_code == 202