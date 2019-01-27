from django.db import models

class AssetClass(models.Model):
    class Meta:
    	db_table = 'asset_classes'
    model = models.ForeignKey('webo_admin.CeModel', on_delete=models.CASCADE, blank=True, null=True)
    # ENUM values type column
    TYPE_STOCKS = 'Stocks'
    TYPE_BONDS = 'Bonds'
    TYPE_CHOICES = (
        (TYPE_STOCKS, 'Stocks'),
        (TYPE_BONDS, 'Bonds'),
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    tolerance_band = models.IntegerField(blank=True, null=True)

    def __str__(self):
    	return str(self.pk) + ": " + self.name
    