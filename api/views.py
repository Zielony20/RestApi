from api import pagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator
from rest_framework import filters
from django.core.serializers import deserialize
from base.models import *
from .serializers import *
from django.db import transaction
from django.db.models import Sum
from django.db.models import Q


@api_view(['GET'])
def getYears(request):
    items = Year.objects.all()
    paginator = PageNumberPagination()
    resources = paginator.paginate_queryset(items, request)
    serializer = YearSerializer(resources, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def getYear(request, pk_year):
    item = Year.objects.get(year=pk_year)   
    serializer = YearSerializer(item)
    return Response(serializer.data)

@api_view(['POST'])
def addYear(request):
    with transaction.atomic():
        serializer = YearSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

@api_view(['PUT'])
def updateYear(request, pk_year):
    student = Year.objects.get(year=pk_year)
    serializer = YearSerializer(instance=student ,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteYear(request, pk_year):
    student = Year.objects.get(year=pk_year)
    student.delete()
    return Response('Year succesfully delete!')

#-----------------------------------------------

@api_view(['GET'])
def getUsers(request):
    items = User.objects.all()
    paginator = PageNumberPagination()
    resources = paginator.paginate_queryset(items, request)
    serializer = UserSerializer(resources, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def getUser(request,pk_u):
    items = User.objects.get(index=pk_u)
    serializer = UserSerializer(items)
    return Response(serializer.data)

@api_view(['POST'])
def addUser(request):
    with transaction.atomic():
        serializer = UserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, pk_u):
    student = User.objects.get(index=pk_u)
    student.delete()
    return Response('User succesfully delete!')

@api_view(['PUT'])
def updateUser(request, pk_u):
   
    student = User.objects.get(index=pk_u)
    serializer = UserSerializer(instance=student ,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['PATCH'])
def patchUser(request, pk_u):
    student = User.objects.get(id=pk_u)
    serializer = UserSerializer(instance=student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


#-----------------------------------------------

@api_view(['GET'])
def getMembers00(request,pk_year):

    #items = User.objects.filter(id =
    #(Member.objects.filter(year=pk_year).values('userid') ) )
    #print(items.values("userid"))
    #items = Member.objects.select_related('userid')
    #items = User.objects.filter( id in items['userid'].value() )
    
    #print(str(items.query))
    #items0 = Member.objects.filter(year=pk_year)
    #print(items0)
    #print(items0.values())

    items = Member.objects.filter(year=pk_year)
    ids = []
    for i in items.values('userid'):
        ids.append(dict(i)['userid'])
    print(ids)    
    
    
    my_filter_qs = Q()
    for creator in ids:
        my_filter_qs = my_filter_qs | Q(id=creator)
    items = User.objects.filter(my_filter_qs)
    print(items.values())
    

    #items = User.objects.filter(id = items0.userid)

    items0 = User.objects.all()
    print(items0.values())
   
    serializer = UserSerializer(items, many=True)
    print(serializer)    
   
    paginator = PageNumberPagination()
    resources = paginator.paginate_queryset(items, request)
    
    serializer = UserSerializer(resources, many=True)

    return paginator.get_paginated_response(serializer.data)
    #return Response(serializer.data)

@api_view(['GET'])
def getMember(request,pk_year,pk_mem):
    items = Year.objects.get(year = pk_year)
    print(type(items))
    serializer = YearSerializer(items)
    item = serializer.data['members']
    for i in item:
        if i['index']==pk_mem:
            item = i
            break;
    
    return Response(item)

@api_view(['GET'])
def getMembers(request,pk_year):
    items = Year.objects.get(year = pk_year)
    print(type(items))
    serializer = YearSerializer(items)
    print(serializer.data['members'])
    

    return Response(serializer.data['members'])



@api_view(['GET'])
def getMembers2(request,pk_year):
    items = Member.objects.filter(year=pk_year)
    serializer = MemberSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def addMember(request,pk_year):
    with transaction.atomic():
        if(pk_year not in request.data):
            request.data["year"]=pk_year
        serializer = MemberSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

@api_view(['DELETE'])
def deleteMember(request, pk_year, pk_mem):
    student = Member.objects.get(id=pk_mem)
    student.delete()
    return Response('Member succesfully delete!')

@api_view(['PUT'])
def updateMember(request, pk_year, pk_mem):
    if(pk_year not in request.data):
        request.data["year"]=pk_year
    student = Member.objects.get(id=pk_mem)
    serializer = MemberSerializer(instance=student ,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def patchMember(request, pk_year, pk_mem):
    if(pk_year not in request.data):
        request.data["year"]=pk_year
    student = Member.objects.get(id=pk_mem)
    serializer = MemberSerializer(instance=student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


#----------------------------------------------

@api_view(['GET'])
def getContribution(request,pk_year,pk_mem,pk_con):
    items = Contributions.objects.filter(id=pk_con,member=pk_mem , year=pk_year)
    serializer = ContributionsSerializer(items, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def getContributions(request,pk_year, pk_mem):
    items = Contributions.objects.filter(year=pk_year, member=pk_mem)

    paginator = PageNumberPagination()
    resources = paginator.paginate_queryset(items, request)

    serializer = ContributionsSerializer(resources, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addContributions(request, pk_year, pk_mem):
    with transaction.atomic():
        if(pk_year not in request.data):
            request.data["year"]=pk_year
        if(pk_mem not in request.data):
            request.data["member"]=pk_mem
        serializer = ContributionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)

@api_view(['DELETE'])
def deleteContributions(request, pk_year, pk_mem, pk_con):
    item = Contributions.objects.filter(id=pk_con, year=pk_year, member=pk_mem)
    item.delete()
    return Response('Contribution succesfully delete!')

@api_view(['PUT'])
def updateContributions(request, pk_year, pk_mem, pk_con):
    print(request.data.keys())
    if('year' not in request.data.keys()):
        request.data["year"]=pk_year
    if(pk_mem not in request.data):
        request.data["member"]=pk_mem
    
    item = Contributions.objects.get(id=pk_con)
    serializer = ContributionsSerializer(instance=item ,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#-----------------------------------------------

@api_view(['GET'])
def getIncome(request,pk_year, pk_mem):
    items = Income.objects.filter(year=pk_year, member=pk_mem)
    serializer = IncomeSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getIncomes(request,pk_year):
    items = Income.objects.filter(year=pk_year)

    paginator = PageNumberPagination()
    resources = paginator.paginate_queryset(items, request)

    serializer = IncomeSerializer(resources, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def addIncome(request, pk_year):
    with transaction.atomic():
        if('year' not in request.data.keys()):
            request.data["year"]=pk_year
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


@api_view(['DELETE'])
def deleteIncome(request, pk_year, pk_exp):
    item = Income.objects.filter(id=pk_exp, year=pk_year)
    item.delete()
    return Response('Income succesfully delete!')

@api_view(['PUT'])
def updateIncome(request, pk_year, pk_exp):

    if("year" not in request.data.keys()):
        request.data["year"]=pk_year
    
    item = Income.objects.get(id=pk_exp)
    serializer = IncomeSerializer(instance=item ,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def patchIncome(request, pk_year, pk_exp):

    item = Income.objects.get(id=pk_exp)
    serializer = IncomeSerializer(instance=item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

#-----------------------------------------------

@api_view(['GET'])
def getExpenditure(request,pk_year, pk_exp):
    items = Expenditure.objects.get(year=pk_year, id=pk_exp)
    serializer = ExpenditureSerializer(items)
    return Response(serializer.data)


@api_view(['GET'])
def getExpenditures(request,pk_year):
    items = Expenditure.objects.filter(year=pk_year)

    paginator = PageNumberPagination()
    resources = paginator.paginate_queryset(items, request)

    serializer = ExpenditureSerializer(resources, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def addExpenditure(request, pk_year):
    with transaction.atomic():
        if(pk_year not in request.data):
            request.data["year"]=pk_year
        serializer = ExpenditureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("save")
        return Response(serializer.data)

@api_view(['DELETE'])
def deleteExpenditure(request, pk_year, pk_exp):
    item = Expenditure.objects.filter(id=pk_exp, year=pk_year)
    item.delete()
    return Response('Expenditure succesfully delete!')

@api_view(['PUT'])
def updateExpenditure(request, pk_year, pk_exp):

    if("year" not in request.data.keys()):
        request.data["year"]=pk_year
    
    item = Expenditure.objects.get(id=pk_exp)
    serializer = ExpenditureSerializer(instance=item ,data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PATCH'])
def patchExpenditure(request, pk_year, pk_exp):

    item = Expenditure.objects.get(id=pk_exp)
    serializer = ExpenditureSerializer(instance=item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


#-----------------------------------------------

@api_view(['GET'])
def getBudget(request):
    contributions = Contributions.objects.all().aggregate(Sum('cost'))['cost__sum']
    expenditure = Expenditure.objects.all().aggregate(Sum('cost'))['cost__sum']
    income = Income.objects.all().aggregate(Sum('cost'))['cost__sum']

    print(income)
    print(expenditure)
    print(contributions)

    result = { "Wpływy":income+contributions,"Wydatki":expenditure,"Bilans":income+contributions-expenditure }

    return Response(result)


@api_view(['GET'])
def getBudgetYear(request, pk_year):
    contributions = Contributions.objects.filter(year = pk_year).aggregate(Sum('cost'))['cost__sum']
    expenditure = Expenditure.objects.filter(year = pk_year).aggregate(Sum('cost'))['cost__sum']
    income = Income.objects.filter(year = pk_year).aggregate(Sum('cost'))['cost__sum']

    if(income != None):
        i = None
    else:
        i = 0
    
    if(expenditure != None):
        e = None
    else:
        e = 0
    
    if(contributions != None):
        c = None
    else:
        c = 0
        
    result = { "Wpływy":i+c,"Wydatki":e,"Bilans":i+c-e }

    return Response(result)



class ApiYearListView(ListAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    pagination_class = PageNumberPagination

class ApiUserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

class ApiIncomeListView(ListAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    pagination_class = PageNumberPagination

class ExpenditureListView(ListAPIView):
    queryset = Expenditure.objects.all()
    serializer_class = ExpenditureSerializer
    pagination_class = PageNumberPagination

class ApicontributionsListView(ListAPIView):
    queryset = Contributions.objects.all()
    serializer_class = ContributionsSerializer
    pagination_class = PageNumberPagination


