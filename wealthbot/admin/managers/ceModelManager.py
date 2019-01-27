from user.models import User
from admin.models import CeModel

class CeModelManager(object):

	# Get child models by parent model.
	def getChildModels(self, parent):
		owner = parent.owner

		return CeModel.objects.filter(parent=parent, owner=owner)
		