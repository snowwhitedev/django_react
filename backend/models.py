import datetime
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.
class GoogleAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,)
    gavatar = models.CharField(max_length=256, default=None, null=True, blank=True)

class EmailPattern(models.Model):
    pattern = models.CharField(max_length=128)

    def __str__(self):
        return self.pattern

class Document(models.Model):
    title = models.CharField(max_length = 128)
    description = models.TextField()
    body = models.TextField()
    policyItems = models.TextField(default=None)
    groups = models.ManyToManyField(to=Group, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    # def show_desc(self):
    #     return self.description[:50]

class PolicyItem(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, default=None,  null=True, blank=True)
    docTitle = models.CharField(max_length=256)
    itemText = models.TextField()
    importance = models.PositiveSmallIntegerField(default=1)
       
    def __str__(self):
        return self.docTitle + self.itemText

class Question(models.Model):
    # policyId = models.CharField(max_length=256)
    policy = models.ForeignKey(PolicyItem, on_delete=models.CASCADE, default=None, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    showed_at = models.DateTimeField(default=None,  null=True)
    
    def __str__(self):
        return self.question

#for displaying
class DocumentStructure(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, default=1, null=True, blank=True)
    descriptionId = models.IntegerField()
    description = models.TextField(default="")
    policyitems = models.ManyToManyField(to=PolicyItem, null=True)

    # class Meta:
    #     unique_together = (('document', 'descriptionId'), )

class PolicyItemQuestion(models.Model):
    policy = models.OneToOneField(PolicyItem, on_delete=models.CASCADE)
    questions = models.ForeignKey(Question, on_delete=models.SET_DEFAULT, default=1, null=True, blank=True)
    
class UserHandbook(models.Model):
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    policy = models.ForeignKey(PolicyItem, on_delete=models.CASCADE, default=None,  null=True, blank=True)
    first = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = (('user', 'document', 'policy'), )

class Repetition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    userrep_id = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'userrep_id'), )

class RepetitionItem(models.Model):
    repetition = models.ForeignKey(Repetition, on_delete=models.CASCADE)
    policy = models.ForeignKey(PolicyItem, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    itemNo = models.PositiveSmallIntegerField(default=1)
    answer=models.IntegerField(default=-1) #-1, 0, 1, 2
    answered_at = models.DateTimeField(default=None, null=True)

    class Meta:
        unique_together = (('repetition', 'policy'), )

#for cron work
class CronLog(models.Model):
    description = models.CharField(max_length=256, default="cron log")
    cron_time = models.DateTimeField(default=timezone.now)
    userNumber = models.IntegerField(default=0)
    def __str__(self):
        return str(self.description)

#for external event -- initial acknowledgement of all relevant documents.
class InitialComplete(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False )


class OverdueHandbook(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE ,default=1)
    overdue = models.PositiveIntegerField(default=1)