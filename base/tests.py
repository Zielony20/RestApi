from django.test import TestCase
from rest_framework.test import APIRequestFactory


# Create your tests here.


factory = APIRequestFactory()
request = factory.post('/notes/', {'title': 'new idea'}, format='json')


