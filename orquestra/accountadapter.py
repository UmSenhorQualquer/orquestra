from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

class OrquestraAccountAdapter(DefaultAccountAdapter):

	def user_signed_up(self, request, user):
		print(request, user)
		print('--------------------------')
		if hasattr( settings, 'ORQUESTRA_ALLOW_DOMAINS_LOGIN') and settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
			if user.email.split('@')[1] not in settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
				raise ImmediateHttpResponse(render_to_response('error.html'))



class OrquestraSocialAccountAdapter(DefaultSocialAccountAdapter):

	def pre_social_login(self, request, sociallogin):
		if hasattr( settings, 'ORQUESTRA_ALLOW_DOMAINS_LOGIN') and settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
			u = sociallogin.account.user
			if u.email.split('@')[1] not in settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
				raise ImmediateHttpResponse(render_to_response('error.html'))