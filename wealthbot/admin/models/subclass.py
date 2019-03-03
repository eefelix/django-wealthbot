from django.db import models

class Subclass(models.Model):
    class Meta:
    	db_table = 'subclasses'
    asset_class = models.ForeignKey('webo_admin.AssetClass', on_delete=models.CASCADE, related_name='subclasses')
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True, null=True)
    source = models.ForeignKey('webo_admin.Subclass', on_delete=models.CASCADE, related_name='targets', blank=True, null=True)
    name = models.CharField(max_length=255)
    expected_performance = models.FloatField()
    priority = models.IntegerField(blank=True, null=True)
    tolerance_band = models.IntegerField(blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.name
    