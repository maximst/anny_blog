from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from django.http import HttpResponse
from social import exceptions as social_exceptions     

class MySocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        raise exception
