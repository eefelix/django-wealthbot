from django.db import models
from django.utils.text import slugify
from user.models import User

class CeModel(models.Model):
    class Meta:
    	db_table = 'ce_models'
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    parent = models.ForeignKey('webo_admin.CeModel', on_delete=models.CASCADE, blank=True, null=True)
    TYPE_STRATEGY = 1
    TYPE_CUSTOM = 2
    TYPE_CHOICES = (
        (TYPE_STRATEGY, '1: Strategy type'),
        (TYPE_CUSTOM, '2: Custom type'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    is_deleted = models.BooleanField()
    risk_rating = models.IntegerField(blank=True, null=True)
    commission_min = models.FloatField(blank=True, null=True)
    commission_max = models.FloatField(blank=True, null=True)
    forecast = models.IntegerField(blank=True, null=True)
    generous_market_return = models.FloatField(blank=True, null=True)
    low_market_return = models.FloatField(blank=True, null=True)
    is_assumption_locked = models.BooleanField()
    groupedModelEntities = None

    def __str__(self):
    	return str(self.pk) + ": " + self.name

    def save(self, *args, **kwargs):
        bare_slug = slugify(self.name).replace('-','_')
        unique_slug = bare_slug
        num = 1
        while CeModel.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}_{}'.format(bare_slug, num)
            num += 1
        self.slug = unique_slug
        super(CeModel, self).save(*args, **kwargs)

    def buildGroupModelEntities(self):
        self.groupedModelEntities = {
            'qualified': [],
            'non_qualified': [],
        }

        for modelEntity in self.modelEntities.all():
            if modelEntity.is_qualified:
                self.groupedModelEntities['qualified'].append(modelEntity)
            else:
                self.groupedModelEntities['non_qualified'].append(modelEntity)

    def getQualifiedModelEntities(self):
        return self.groupedModelEntities['qualified']

    def getNonQualifiedModelEntities(self):
        return self.groupedModelEntities['non_qualified']
    
    def getCommissions(self):
        commission = []

        min = self.commission_min
        if min is not None:
            commission.append(min)

        max = self.commission_max
        if max is not None:
            commission.append(max)

        return commission
    