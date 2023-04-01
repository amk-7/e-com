from django.db import models
from django.core.validators import MinValueValidator

class Post(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    loveNumber = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0)])
    media = models.FileField(upload_to="postes")
    #users = models.ManyToManyField()

    def __str__(self):
        return f"{self.name}"
    
    def incrementNbLike(self):
        self.loveNumber += 1
        self.save()

    def decrementNbLike(self):
        self.loveNumber -= 1
        self.save()
    
    def getMediaFormat(self):
        images = ['jpg', 'jpeg', 'png']
        if self.media.url.split('.')[1] in images:
            return "image"
        return "video"