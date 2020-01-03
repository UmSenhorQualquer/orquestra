from allauth.account.adapter import DefaultAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.shortcuts import render


class OrquestraAccountAdapter(DefaultAccountAdapter):

	def user_signed_up(self, request, user):
		if hasattr( settings, 'ORQUESTRA_ALLOW_DOMAINS_LOGIN') and settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
			if user.email.split('@')[1] not in settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
				raise ImmediateHttpResponse(render(request, 'error.html'))



class OrquestraSocialAccountAdapter(DefaultSocialAccountAdapter):

	def pre_social_login(self, request, sociallogin):
		if hasattr( settings, 'ORQUESTRA_ALLOW_DOMAINS_LOGIN') and settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
			u = sociallogin.user
			email = u.email
			if email.split('@')[1] not in settings.ORQUESTRA_ALLOW_DOMAINS_LOGIN:
				raise ImmediateHttpResponse(render(request, 'error.html'))