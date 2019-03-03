from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def afterLogin(request):
	# Get user object after login
	user = request.user

	# Redirect to different pages depending on the user role
	if user.hasRole('ROLE_ADMIN'):
		# Redirect to the wealthbot admin page
		redirectUrl = 'rx_admin_homepage'
	else:
		if user.hasRole('ROLE_RIA') or user.hasRole('ROLE_RIA_USER'):
			# Redirect to the RIA page
			if ('wealthbot_ria_view_client_id' in request.session):
				redirectUrl = 'rx_ria_dashboard_show_client'
			else:
				redirectUrl = getRouteForRia(user)
		elif user.hasRole('ROLE_CLIENT'):
			# Redirect to the client page
			redirectUrl = getRouteForClient(user=user, session=request.session)
		elif user.hasRole('ROLE_SLAVE_CLIENT'):
			# Redirect to the client page
			redirectUrl = getSessionRedirectUrl(request.session)
			if redirectUrl is not None:
				removeSessionRedirectUrl(request.session)
			else:
				redirectUrl = 'rx_client_dashboard'
		else:
			# Redirect to the landing page for anonymous user
			redirectUrl = 'rx_user_homepage'

	return redirect(redirectUrl)

def getRouteForRia(user):
	return 'rx_ria_dashboard'

def getRouteForClient(user, session):
	# Check if session has stored redirectUrl
	redirectUrl  = getSessionRedirectUrl(session)
	if redirectUrl is not None:
		removeSessionRedirectUrl(session)
		return redirectUrl

	# Return the redirect label from the given registration_step
	if hasattr(user, 'profile'):
		return {
		    0 : 'rx_client_profile_step_one',
		    1 : 'rx_client_profile_step_two',
		    2 : 'rx_client_profile_step_three',
		    3 : 'rx_client_portfolio',
		    4 : 'rx_client_portfolio',
		    5 : 'rx_client_transfer',
		    6 : 'rx_client_transfer',
		    7 : 'rx_client_dashboard',
		}.get(user.profile.registration_step, 'rx_user_homepage')

	return 'rx_client_profile_step_one'

def getSessionRedirectUrl(session):
	if 'redirect_url' in session:
		return session['redirect_url']

def removeSessionRedirectUrl(session):
	del session['redirect_url']
