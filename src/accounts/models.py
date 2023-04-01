from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Personne(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    adresse = models.JSONField(default=list, blank=True, null=True)
    contact = models.CharField(max_length=100, unique=True, blank=True)

    class Meta:
        abstract = True

    def showAdresse(self):
        if len(self.adresse) == 3:
            return f"Ville : {self.adresse[0]}, Quartier : {self.adresse[1]}, localisation : {self.adresse[2]}"
        return "Non renseigné."
    def getTown(self):
        if len(self.adresse) > 0:
            return self.adresse[0]
        return ""
    def getNeighborhood(self):
        if len(self.adresse) > 1:
            return self.adresse[1]
        return ""
    def getReferencePlace(self):
        if len(self.adresse) == 3:
            return self.adresse[2]
        return ""
        
    def __str__(self):
        return self.user.username