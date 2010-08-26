from django.conf import settings


def base_context(request):
    ''' template variables available to every template'''
    return {'home_page': settings.HOME_PAGE}
