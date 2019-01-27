from django.http import HttpResponse, Http404, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.urls import reverse
from client.forms import ClientProfileForm, ClientSpouseForm, ClientQuestionsForm
from client.forms import AccountGroupsForm, AccountTypesForm, ClientAccountForm, TypedClientAccountForm
from user.models import Profile
from client.models import ClientQuestionnaireAnswer, AccountGroup, AccountType
from client.models import AccountGroupType, ClientAccount, SystemAccount
from ria.models import RiskQuestion, RiskAnswer
from client.managers.riskToleranceManager import RiskToleranceManager
from client.managers.clientPortfolioManager import ClientPortfolioManager

ACCOUNT_STEP_ACCOUNT_GROUP = 1
ACCOUNT_STEP_ACCOUNT_GROUP_TYPE = 2
ACCOUNT_STEP_ACCOUNT_UPDATE_FORM = 3
ACCOUNT_STEP_ACCOUNT_OWNER_FORM = 4

@login_required
def stepOne(request):
	# Get the user object
	user = request.user

	# Create user profile if it doesn't exist
	if not hasattr(user, 'profile'):
		profile = Profile(user=user, first_name='#')
	else:
		profile = user.profile

	# Create user profile collection form
	if request.method == 'POST':
		form = ClientProfileForm(request.POST, prefix='client', instance=profile)
		subform = ClientSpouseForm(request.POST, prefix='spouse')
		if form.is_valid():
			# print('Form is valid')
			profile = form.save(commit=False)
			spouse = user.getSpouse()

			if profile.marital_status == Profile.CLIENT_MARITAL_STATUS_MARRIED:
				# Link up the spouse if the client marital status is married
				if subform.is_valid():
					spouse = subform.save(commit=False)
					spouse.client = user
				else:
					# if the spouse info form has problem
					# print('Spouse info form is not valid')
					# print(subform.errors)
					# print(subform.non_field_errors)
					context = {
						'form': form,
						'subform': subform,
						'ria_company_information': user.profile.ria_user.riacompanyinformation
					}
					return render(request, 'client/profile_step_one.html', context)
			else:
				# Otherwise remove the contact if any
				user.removeAdditionalContact(spouse)

			# Set Client registration step to 1
			profile.registration_step = 1

			profile.save()
			user.save()
			if spouse is not None:
				spouse.save()

			if profile.client_source == Profile.CLIENT_SOURCE_IN_HOUSE:
				# Redirect to client portfolio page if the source is in-house
				redirectUrl = 'rx_client_portfolio'
			else:
				# Redirect to user profile collection step two page if the source is web
				redirectUrl = 'rx_client_profile_step_two'

			return redirect(redirectUrl)
		else:
			print('Form is not valid')
			print(form.errors)
			print(form.non_field_errors)
	else:
		form = ClientProfileForm(
			prefix='client', 
			instance=profile,
		)
		subform = ClientSpouseForm(prefix='spouse')

	context = {
		'form': form,
		'subform': subform,
		'ria_company_information': user.profile.ria_user.riacompanyinformation
	}
	return render(request, 'client/profile_step_one.html', context)

@login_required
def stepTwo(request):
	# Get the user object
	user = request.user

	# Check if user exists as client role or not
	if (user is None) or (not user.hasRole('ROLE_CLIENT')):
		raise Http404("Ria user does not exist.")

	if request.method == 'POST':
		form = ClientQuestionsForm(request.POST, user=user)
		if form.is_valid():
			# Pre-process by removing all previous userAnswer records
			ClientQuestionnaireAnswer.objects.filter(client_id=user.pk).delete()
			# Get corresponding questions
			riaId = user.profile.ria_user.pk
			riskQuestion = RiskQuestion()
			questions = riskQuestion.getOwnerQuestionsOrAdminIfNotExists(ownerId=riaId)

			withdrawAge = 0
			answers = []

			# Get corresponding answers by the client
			for question in questions:
				data = form.cleaned_data['answer_{}'.format(question.pk)]
				# Construct dict of an answer
				answer = {
					'question': question
				}

				if question.is_withdraw_age_input:
					withdrawAge = int(data) # Suspect problem in original wealthbot code using answer instead of data
					# Roughly estimate ago of client
					diff = datetime.date.today() - user.profile.birth_date
					age = int(diff.days / 365.25)
					# Calc the difference between current age and withdraw age
					ageDiff = withdrawAge - age

					answer['data'] = ageDiff
				else:
					# Get the RiskAnswer object from the data as id
					riskAnswer = get_object_or_404(RiskAnswer, pk=int(data))
					answer['data'] = riskAnswer

				answers.append(answer)

			# Save Client Questionnaire answers to the database
			riskToleranceManager = RiskToleranceManager(user=user, answers=answers)
			riskToleranceManager.saveUserAnswers()

			if (not request.is_ajax()):
				suggestedModel = riskToleranceManager.getSuggestedPortfolio()
				# Process suggest portfolio.
				profile = user.profile
				profile.withdraw_age = withdrawAge
				clientPortfolioManager = ClientPortfolioManager()
				clientPortfolioManager.proposePortfolio(client=user, portfolio=suggestedModel)

				profile.save()

			# Set Client registration step to 2
			profile = user.profile
			profile.registration_step = 2
			profile.save()

			# Redirect to user profile collection step three page
			return redirect('rx_client_profile_step_three')

		else:
			print('Form is not valid')
	else:
		form = ClientQuestionsForm(user=user)

	context = {
		'form': form,
		'ria_company_information': user.profile.ria_user.riacompanyinformation
	}
	return render(request, 'client/profile_step_two.html', context)

@login_required
def stepThree(request):
	removeAccountStep(session=request.session)

	# Get the user object
	user = request.user

	if request.method == 'POST':
		form = AccountGroupsForm(request.POST, user=user)
		if form.is_valid():
			group = form.cleaned_data['groups']
			
			setAccountGroup(session=request.session, group=group)

			setAccountStep(session=request.session, step=ACCOUNT_STEP_ACCOUNT_GROUP)

			# Prepare the JSON response for AJAX request
			data = {
				'status': 'success',
				'form': getAccountFormByGroup(request=request, group=group)
			}
			return JsonResponse(data)
		else:
			return JsonResponse(
				{
					'status': 'error',
				}
			)
	else:
		form = AccountGroupsForm(user=user)

	context = {
		'form': form,
		'client': user,
		'ria_company_information': user.profile.ria_user.riacompanyinformation
	}
	return render(request, 'client/profile_step_three.html', context)

def createAccount(request, group):
	if (request.method != 'POST') or (not request.is_ajax()):
		raise Http404("Page not found.")

	# Get the user object
	client = request.user
	if (client is None) or (not client.hasRole('ROLE_CLIENT')):
		return JsonResponse(
			{
				'status': 'error',
				'message': 'Client does not exist.',
			}
		)

	# Check account group is valid or not
	allowedGroups = AccountGroup.getGroupChoices()
	if (group, group) not in allowedGroups:
		return HttpResponseBadRequest('Invalid group type')
	groupTypeId = None
	groupType = None

	clientAccount = ClientAccount(value=0, is_pre_saved=False)

	if (group == AccountGroup.GROUP_DEPOSIT_MONEY) or (group == AccountGroup.GROUP_FINANCIAL_INSTITUTION):
		groupType = getAccountGroupType(session=request.session)
		clientAccount.groupType = groupType

	# print("Checkpoint 0: groupType is")
	# print(groupType)
	if request.method == 'POST':
		# print("Checkpoint 1a: Enter into request.method POST")
		###############
		# Pre-process form data before validation
		###############
		post = request.POST.copy()
		post['value'] = float(post['value'].replace(',',''))
		post['groupType'] = groupType.pk
		request.POST = post
		# print(request.POST.get('value'))
		form = TypedClientAccountForm(request.POST, user=client, group=group, groupType=groupType)
		if form.is_valid():
			# print("Checkpoint 2a: Successfully validate the form")
			clientAccount = form.save(commit=False)
			clientAccount.client = client
			clientAccount.is_pre_saved = False
			clientAccount.save()
			removeAccountGroup(session=request.session)
			removeAccountType(session=request.session)
			removeAccountGroupType(session=request.session)
			removeAccountOwners(session=request.session)

			if group == 'employer_retirement':
				responseData = processEmployerRetirementAccountForm(clientAccount)
			else:
				responseData = processAccountForm(request=request)
				# Check if the group type is deposit and how many accounts the client has applied
				isType = (clientAccount.groupType.group.name == AccountGroup.GROUP_DEPOSIT_MONEY)
				systemAccounts = SystemAccount.objects.filter(client=client, type=clientAccount.system_type)
				responseData['in_right_box'] = False if (isType or (systemAccounts.count() < 1)) else True
				responseData['transfer_url'] = reverse(
					'rx_client_dashboard_select_system_account',
					kwargs={'account_id': clientAccount.pk},
				)

			removeIsConsolidateAccount(session=request.session)
			removeAccountStep(session=request.session)
			return JsonResponse(responseData)
		else:
			print('Checkpoint 2b: Form is not valid')
			print(form.errors)
			print(form.non_field_errors)
	else:		
		# print("Checkpoint 1b: Cannot enter into request.method POST")
		form = TypedClientAccountForm(user=client, group=group, groupType=groupType)

	message = getTitleMessageForAccountForm(session=request.session, group=group, groupType=groupType)

	template = loader.get_template('client/profile_client_accounts_form.html')
	context = {
		'form': form,
		'group': group,
		'hide_submit_button': True,
		'title_message': message,
	}
	content = template.render(context, request)
	data = {
		'status': 'error',
		'content': content,
	}
	return JsonResponse(data)

def updateAccountForm(request, group):
	# Get the user object
	client = request.user

	form = ClientAccountForm(request.POST, user=client, group=group, validateAdditionalFields=False)

	step = getAccountStep(session=request.session)
	if step == ACCOUNT_STEP_ACCOUNT_UPDATE_FORM:
		setAccountStep(session=request.session, step=ACCOUNT_STEP_ACCOUNT_OWNER_FORM)
	else:
		setAccountStep(session=request.session, step=ACCOUNT_STEP_ACCOUNT_UPDATE_FORM)

	# Prepare the JSON response for AJAX request
	template = loader.get_template('client/profile_client_accounts_form_fields.html')
	context = {
		'form': form,
	}
	content = template.render(context, request)
	data = {
		'status': 'success',
		'content': content,
	}
	return JsonResponse(data)

def stepThreeBack(request):
	pass

def completeStepThree(request):
	# Get the user object
	client = request.user

	# Set Client registration step to 3
	profile = client.profile
	profile.registration_step = 3
	profile.save()

	# Redirect to user portfolio page
	return redirect('rx_client_portfolio')

def checkAccountsSum(request):
	if (not request.is_ajax()):
		raise Http404()

	# Get the user object
	client = request.user
	ria = client.profile.ria_user

	riaMinAssetSize = ria.riacompanyinformation.min_asset_size

	total = ClientAccount.getTotalScoreByClient(client=client)

	if riaMinAssetSize > total['value']:
		message = 'You must invest at least $' + '{0:.2f}'.format(riaMinAssetSize) + ' with us.'
		return JsonResponse(
			{
				'status': 'error',
				'message': message,
			}
		)

	return JsonResponse(
		{
			'status': 'success',
		}
	)

def showAccountsTable(request):
	# Get the user object
	client = request.user
	if (client is None) or (not client.hasRole('ROLE_CLIENT')):
		return JsonResponse(
			{
				'status': 'error',
				'message': 'Client does not exist.',
			}
		)

	total = ClientAccount.getTotalScoreByClient(client=client)

	print(total)
	context = {
		'client': client,
		'total': total,
		'show_action_btn': True,
	}
	return render(request, 'client/profile_accounts_list.html', context)

def showSuccessMessage(request):
	pass

def editAccount(request, id):
	pass

def deleteAccount(request, id):
	pass
	
def processAccountForm(request):
	template = loader.get_template('client/profile_create_account_success.html')
	context = {}
	content = template.render(context, request)
	data = {
		'status': 'success',
		'content': content,
		'show_accounts_table': 1,
		'show_portfolio_button': 1,
	}
	return data

def processEmployerRetirementAccountForm(account):
	pass

# Save account group in the session.
def setAccountGroup(session, group):
	session['client_accounts_account_group'] = group

# Get account group from session.
def getAccountGroup(session):
	return session['client_accounts_account_group']

# Remove account group from session.
def removeAccountGroup(session):
	if 'client_accounts_account_group' in session:
		del session['client_accounts_account_group']

# Save account type in the session.
def setAccountType(session, type):
	session['client_accounts_account_type'] = type.lower()

# Get account type from session.
def getAccountType(session):
	return session['client_accounts_account_type']

# Remove account type from session.
def removeAccountType(session):
	if 'client_accounts_account_type' in session:
		del session['client_accounts_account_type']

# Save account group type in the session.
def setAccountGroupType(session, groupType):
	session['client_accounts_account_group_type_id'] = groupType.pk

# Get account group type from session.
def getAccountGroupType(session):
	groupTypeId = session['client_accounts_account_group_type_id']
	return AccountGroupType.objects.get(pk=groupTypeId)

# Remove account group type from session.
def removeAccountGroupType(session):
	if 'client_accounts_account_group_type_id' in session:
		del session['client_accounts_account_group_type_id']

# Save account owners in the session.
def setAccountOwners(session, owners):
	session['client_accounts_account_owners'] = owners

# Get account owners from session.
def getAccountOwners(session):
	return session['client_accounts_account_owners']

# Remove account owners from session.
def removeAccountOwners(session):
	if 'client_accounts_account_owners' in session:
		del session['client_accounts_account_owners']


# Get is consolidate account from session.
def getIsConsolidateAccount(session):
	return session['client_accounts_is_consolidate_account']

# Remove is consolidate account from session.
def removeIsConsolidateAccount(session):
	if 'client_accounts_is_consolidate_account' in session:
		del session['client_accounts_is_consolidate_account']

def setAccountStep(session, step):
	session['clients_accounts_step'] = step

def getAccountStep(session):
	return session['clients_accounts_step']

def removeAccountStep(session):
	if 'clients_accounts_step' in session:
		del session['clients_accounts_step']

def getAccountFormByGroup(request, group):
	# Get the user object
	user = request.user

	# Create different form w.r.t. different group
	if (group == AccountGroup.GROUP_FINANCIAL_INSTITUTION) or (group == AccountGroup.GROUP_DEPOSIT_MONEY):
		template = loader.get_template('client/profile_select_account_type_form.html')
		context = {
			'form': AccountTypesForm(user=user, group=group),
			'group': group,
		}
		content = template.render(context, request)

	return content

def getAccountOwnerFormView(user, isJoint):
	pass

def getTitleMessageForAccountForm(session, group, groupType=None):
	message = ''
	if groupType is not None:
		message = groupType.type.name
	else:
		message = getAccountType(session=session)

	return {
	    AccountGroup.GROUP_FINANCIAL_INSTITUTION : 'Tell us about the account you will be transferring:',
	    AccountGroup.GROUP_DEPOSIT_MONEY : 'Tell us about the ' + message + ' account you will be opening:',
	    AccountGroup.GROUP_OLD_EMPLOYER_RETIREMENT : 'Tell us about the account you will be rolling over:',
	    AccountGroup.GROUP_EMPLOYER_RETIREMENT : 'Tell us about the account you would like advice for:',
	}.get(group, 'Tell us about the account:')

def getAccountFormByGroupAndGroupType(request, group, groupType):
	# Get the user object
	user = request.user

	# Create different form w.r.t. different group and group type
	if (not user.isMarried()) and (getAccountType(request.session) != 'joint account'):
		form = TypedClientAccountForm(user=user, groupType=groupType, group=group)
		message = getTitleMessageForAccountForm(session=request.session, group=group, groupType=groupType)

		template = loader.get_template('client/profile_client_accounts_form.html')
		context = {
			'form': form,
			'group': group,
			'hide_submit_button': True,
			'title_message': message,
		}
		content = template.render(context, request)
	else:
		content = getAccountOwnerFormView(
			user=user,
			isJoint=(getAccountType(request.session) == 'joint account')
		)

	return content

def showDepositAccountForm(request):
	if (request.method != 'POST') or (not request.is_ajax()):
		raise Http404("Page not found.")

	# Get the user object
	client = request.user
	group = getAccountGroup(request.session)

	depositAccountGroupForm = AccountTypesForm(request.POST, user=client, group=group)

	if depositAccountGroupForm.is_valid():
		# Get the account group type
		type = depositAccountGroupForm.cleaned_data['group_type']
		typeObj = AccountType.objects.get(name=type)
		groupObj = AccountGroup.objects.get(name=group)
		groupType = AccountGroupType.objects.get(group=groupObj, type=typeObj)

		# Save account group type into current session
		setAccountType(session=request.session, type=type)
		setAccountGroupType(session=request.session, groupType=groupType)
		setAccountStep(session=request.session, step=ACCOUNT_STEP_ACCOUNT_GROUP_TYPE)

		accountForm = getAccountFormByGroupAndGroupType(request=request, group=group, groupType=groupType)

		# Prepare the JSON response for AJAX request
		data = {
			'status': 'success',
			'form': accountForm
		}
		return JsonResponse(data)

	return JsonResponse(
		{
			'status': 'error',
		}
	)
		