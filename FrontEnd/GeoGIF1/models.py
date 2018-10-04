from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text =  models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default =0)
    def __str__(self):
        return self.choice_text
class Source(models.Model):
    # The name of the sourceS
    name = models.CharField(max_length = 200)
    # Source http link
    source = models.CharField(max_length = 300)
    # LastUpdate
    lastUpdate = models.DateTimeField(default=timezone.now())
class GetCapapilities(models.Model):
    # Source http link
    source = models.CharField(max_length = 300)
    # Product name
    prodName = models.CharField(max_length = 300)
    # timeEnabled
    timeEnabled = models.BooleanField()
    # Time extent
    timeExtent = models.CharField(max_length = 500)
    # LastUpdate
    lastUpdate = models.DateTimeField(default=timezone.now())
