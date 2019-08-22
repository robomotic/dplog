from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
#from django.contrib.postgres.fields import JSONField

class Question(models.Model):

    OBS_TYPES = (
        ('U', 'URL'),
        ('I', 'IP'),
        ('D', 'DomainName'),
        ('F', 'FileHash'),
        ('P', 'ProcessName'),
        ('R', 'RegistryKey'),
    )

    RRT_TYPES = (
        ('M', 'MirroredQuestion'),
        ('F', 'ForcedResponseDesign'),
        ('D', 'DisguisedResponseDesign'),
        ('R', 'LaPlaceReal'),
        ('A', 'LaPlaceDiscrete'),
    )

    title = models.CharField(max_length=50)
    observable = models.CharField(max_length=50)
    observable_type = models.CharField(max_length=1, choices=OBS_TYPES)

    begin_datetime= models.DateTimeField(default=now)
    end_datetime = models.DateTimeField(default=now)

    max_rounds = models.IntegerField(default=1)
    algorithm = models.CharField(max_length=1, choices=RRT_TYPES)
    params = JSONField()
    completed = models.BooleanField(default=False)

class QuestionVirtual(models.Model):
    RRT_TYPES = (
        ('M', 'MirroredQuestion'),
        ('F', 'ForcedResponseDesign'),
        ('D', 'DisguisedResponseDesign'),
        ('R', 'LaPlaceReal'),
        ('A', 'LaPlaceDiscrete')
    )
    OBS_TYPES = (
        ('U', 'URL'),
        ('I', 'IP'),
        ('D', 'DomainName'),
        ('F', 'FileHash'),
        ('P', 'ProcessName'),
        ('R', 'RegistryKey'),
    )

    title = models.CharField(max_length=50)
    observable = models.CharField(max_length=50)
    observable_type = models.CharField(max_length=1, choices=OBS_TYPES)

    max_rounds = models.IntegerField(default=1)
    positive_clients = models.IntegerField(default=5)
    total_clients = models.IntegerField(default=100)
    algorithm = models.CharField(max_length=1, choices=RRT_TYPES)

    params = JSONField()

    completed = models.BooleanField(default=False)

class Client(models.Model):
    guid = models.CharField(max_length = 32)
    rsa_public_key = models.CharField(max_length = 2048)
    registered_datetime = models.DateTimeField(default=now, editable=False)

class ClientVirtual(models.Model):
    id = models.IntegerField(primary_key=True)

class ClientEvents(models.Model):
    id = models.AutoField(primary_key=True)
    guid = models.CharField(max_length = 32)
    request_type = models.CharField(max_length=50)
    response_type = models.CharField(max_length=50)
    event_datetime = models.DateTimeField(default=now, editable=False)

class Response(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=now, editable=False)

class ResponseVirtual(models.Model):
    question = models.ForeignKey(QuestionVirtual, on_delete=models.CASCADE, related_name='responses')
    client = models.ForeignKey(ClientVirtual, on_delete=models.CASCADE, related_name='clients')
    datetime = models.DateTimeField(default=now, editable=False)
    count = models.IntegerField(default=0,null=False,editable=False)

class AggregateResponseVirtual(models.Model):
    question = models.ForeignKey(QuestionVirtual, on_delete=models.CASCADE,related_name='aggregated')
    run_datetime = models.DateTimeField(default=now, editable=False)

    estimated_positive_clients = models.IntegerField(default=0)
    estimated_positive_error = models.IntegerField(default=0)

class AggregateResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    positive_clients = models.IntegerField(default=0)
