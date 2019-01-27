from django.db import models
from user.models import User

class CeModelEntity(models.Model):
    class Meta:
    	db_table = 'ce_model_entities'
    model = models.ForeignKey('webo_admin.CeModel', on_delete=models.CASCADE, related_name='modelEntities')
    asset_class = models.ForeignKey('webo_admin.AssetClass', on_delete=models.CASCADE)
    subclass = models.ForeignKey('webo_admin.Subclass', on_delete=models.CASCADE, related_name='ceModelEntities')
    security_assignment = models.ForeignKey('webo_admin.SecurityAssignment', on_delete=models.CASCADE)
    percent = models.FloatField()
    nb_edits = models.SmallIntegerField()
    is_qualified = models.BooleanField()

    def __str__(self):
    	return str(self.pk) + ": " + self.model.name + " - " + str(self.model.pk) + " - " + str(self.asset_class.pk) + " - " + str(self.subclass.pk) + " - " + str(self.security_assignment.pk) + " - " + str(self.percent)
    
    def toArray(self):
        context = {
            'label': self.asset_class.name,
            'data': self.percent,
        }
        return context
