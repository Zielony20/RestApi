from django.db import models


class Year(models.Model):
    year = models.IntegerField(primary_key = True)
    description = models.CharField(max_length=1500)
    '''
    {"year":2020,"description":"ok"}    
    '''

class User(models.Model):
    index = models.IntegerField(primary_key = True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    years = models.ManyToManyField(Year, related_name="members",null=True,blank=True)
    
# {"index":150000,"name":"Tymoteusz","surname":"Puchacz","email":"mailmail@gmail.com"}

class Member(models.Model):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    '''
    {"name":"Tymoteusz","surname":"Puchacz"}
    '''    


class Contributions(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    month = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

'''
{
"cost":40,
"month":"Styczeń",
"date":"2022-10-25"
}
'''

class Expenditure(models.Model):
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=1500)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

'''
{
"cost":40,
"description":"zakup koszulek",
"date":"2006-10-25"
}
'''

class Income(models.Model):
    year = models.ForeignKey(Year,on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length=1500)
    date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)

'''
{
"cost":40,
"description":"sprzedaż koszulek",
"date":"2006-10-25"
}
'''