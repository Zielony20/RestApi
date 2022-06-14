from typing import OrderedDict
from rest_framework import serializers, validators
from base.models import *
from rest_framework.validators import UniqueTogetherValidator



class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        ordering = ['-index']
        model = User
        fields = ['index','name','surname','email','created', 'years']
        extra_kwargs = {'years': {'required': False}}
     #   validators = [
    #        UniqueTogetherValidator(
   #             queryset=User.objects.all(),
  #              fields=['name','surname','email']
 #           )
#        ]



class YearSerializer(serializers.ModelSerializer):

    members = UserSerializer(many=True, read_only=True)
    class Meta:
        ordering = ['-year']
        model = Year
        fields = ['year', 'description', 'members']
        extra_kwargs = {'members': {'required': False}}
     #   validators = [
    #        UniqueTogetherValidator(
   #             queryset=Year.objects.all(),
  #              fields=['year']
 #           )
#        ]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'  #['year','userid', 'created']
#        validators = [
#            UniqueTogetherValidator(
#                queryset=Member.objects.all(),
#                fields=['userid','year'])]
        


class ExpenditureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenditure
        fields = '__all__'
        
    
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'

class ContributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributions
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Contributions.objects.all(),
                fields=['month']
            )
        ]

