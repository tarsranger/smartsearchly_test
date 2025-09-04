from django.db import models


class POI(models.Model):
    internal_id = models.AutoField(primary_key=True)
    name = models.CharField(null=True, blank=True, max_length=255)
    external_id = models.CharField(null=True, blank=True, max_length=100, db_index=True)
    category = models.CharField(null=True, blank=True, max_length=100, db_index=True)
    poi_latitude = models.FloatField(null=True, blank=True)
    poi_longitude = models.FloatField(null=True, blank=True)
    avg_rating = models.FloatField(null=True, blank=True)
    ratings = models.JSONField(default=list, null=True, blank=True)

    def set_avg_rating(self):
        if self.ratings:
            self.avg_rating = sum(self.ratings) / len(self.ratings)
        else:
            self.avg_rating = None