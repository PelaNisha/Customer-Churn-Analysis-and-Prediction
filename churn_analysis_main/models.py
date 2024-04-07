from django.db import models

class CustomerGroup(models.Model):
    group_name = models.CharField(primary_key=True, max_length=100)
    group_type = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

class Customer(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    group_name = models.ForeignKey(CustomerGroup, on_delete=models.CASCADE)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class ChurnPredictionModel(models.Model):
    model_name = models.CharField(primary_key=True, max_length=100)
    date_created = models.DateField()
    prediction = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    date = models.DateField()
    username = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.transaction_id)
