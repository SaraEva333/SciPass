from django.db import models

class Sciedit(models.Model):
    seid = models.BigAutoField(primary_key=True)
    issn = models.CharField(max_length=8, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=False)

class Iff(models.Model):
    ifid = models.BigAutoField(primary_key=True)
    if_value = models.DecimalField(max_digits=7, decimal_places=3, null=True, blank=False)
    db = models.CharField(max_length=100, choices=[('Scopus', 'Scopus'), ('WoS', 'WoS'), ('РИНЦ', 'РИНЦ'), ('ВАК', 'ВАК')], null=True, blank=False)
    year = models.IntegerField(null=True, blank=False)
    seid = models.ForeignKey(Sciedit, on_delete=models.CASCADE)

class Quart(models.Model):
    qid = models.BigAutoField(primary_key=True)
    current_quartile = models.CharField(max_length=2, choices=[('K1', 'K1'), ('K2', 'K2'), ('K3', 'K3'), ('Q1', 'Q1'), ('Q2', 'Q2'), ('Q3', 'Q3'), ('Q4', 'Q4')], null=True, blank=False)
    db = models.CharField(max_length=100, choices=[('Scopus', 'Scopus'), ('WoS', 'WoS'), ('РИНЦ', 'РИНЦ'), ('ВАК', 'ВАК')], null=True, blank=False)
    year = models.IntegerField(null=True, blank=False)
    seid = models.ForeignKey(Sciedit, on_delete=models.CASCADE)

class Specialty(models.Model):
    spid = models.BigAutoField(primary_key=True)
    code = models.CharField(max_length=9, null=True, blank=False)
    dat = models.DateField(null=True, blank=False)
    seid = models.ForeignKey(Sciedit, on_delete=models.CASCADE)

class MyModel(models.Model):
    file = models.FileField(upload_to='uploads/')
