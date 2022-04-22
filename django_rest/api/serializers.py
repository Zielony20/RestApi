from rest_framework import serializers, validators
from base.models import Student
from rest_framework.validators import UniqueTogetherValidator

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Student.objects.all(),
                fields=['name','surname']
            )
        ]
