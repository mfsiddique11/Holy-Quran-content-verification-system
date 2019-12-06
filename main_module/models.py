from django.db import models

# Create your models here.
class Quran(models.Model):
    ChapterID = models.IntegerField()
    VerseID = models.IntegerField()
    ChapterArabic=models.CharField(max_length=9999)
    ChapterNArabic = models.CharField(max_length=9999)

    def __str__(self):
        return (self.ChapterID,self.VerseID,self.ChapterArabic,self.ChapterNArabic)
