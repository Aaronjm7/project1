from celery import shared_task
import logging
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
logger = logging.getLogger(__name__)

@shared_task
def send_welcome_email(user_id):
    User=get_user_model()
    try:
        user=User.objects.get(id=user_id)
        send_mail(
            subject='Welcome to Our App!',
            message='If you get this get me icecream',
            from_email='chicken_fry@biryani.com',  
            recipient_list=[user.email],       
            fail_silently=False,
        )
    except User.DoesNotExist:
        pass
        