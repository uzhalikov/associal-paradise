from django import template
from mysite.models import *

#register = template.Library()
#
#@register.simple_tag()
#def session(request):
#    userid = request.session.get('is_auth', False)
#    return userid