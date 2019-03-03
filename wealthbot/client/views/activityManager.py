from client.models import Activity
from user.models import Profile
from django.db.models.signals import post_save

def saveActivityByObject(sender, **kwargs):
	# print('Get into saveActivityByObject call')
	# print(kwargs['instance'].registration_step)
	if kwargs['created']:
		# print('Get into create activity call')
		client = kwargs['instance'].user
		message = client.getActivityMessage()

		# print(client)
		# print(message)

		if client is not None and message is not None:
			# print('Go ahead to create the activity object')
			# Create activity object
			activity = Activity(
				client_user=client,
				client_status=client.profile.client_status,
				first_name=client.profile.first_name,
				last_name=client.profile.last_name,
				ria_user=client.profile.ria_user,
				message=message,
			)
			# Save activity object
			# print('Save the activity object')
			activity.save()

post_save.connect(saveActivityByObject, sender=Profile)
