from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Student
from .serializers import StudentSerializer

@api_view(['GET'])
def getStudents(request):
    items = Student.objects.all()
    serializer = StudentSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addStudent(request):
    serializer = StudentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def updateStudent(request, pk):
    student = Student.objects.get(id=pk)
    serializer = StudentSerializer(instance=student ,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return Response('Student succesfully delete!')

@api_view(['PATCH'])
def patchStudent(request, pk):
    student = Student.objects.get(id=pk)
    serializer = StudentSerializer(instance=student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
