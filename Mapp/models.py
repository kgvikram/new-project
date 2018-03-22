from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class Album_table(models.Model):
    Album_ID = models.AutoField(primary_key=True)
    Album_Name = models.CharField(max_length=500, null=True)
    Album_Year = models.IntegerField(null=True)

    def __str__(self):
        return str(self.Album_Name)

class Songs_table(models.Model):
    Song_ID = models.AutoField(primary_key=True)
    Album_ID = models.ForeignKey(Album_table, on_delete=models.CASCADE)
    Song_Name = models.CharField(max_length=500, null=True)
    Artist_Name = models.CharField(max_length=500, null=True)
    Views_No = models.IntegerField(default=0)

    def __str__(self):
        return  str(self.Song_ID)

class Rating_table(models.Model):
    Rating_ID = models.AutoField(primary_key=True)
    Song_ID = models.ForeignKey(Songs_table, on_delete=models.CASCADE)
    User_ID = models.ForeignKey(User,on_delete=models.CASCADE )
    Ratings = models.IntegerField(null=True)

    def __str__(self):
        return  str(self.Rating_ID)
