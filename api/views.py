from functools import partial
from http.client import HTTPResponse
import re
from api import pagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator
from rest_framework import filters, status
from django.core.serializers import deserialize
from base.models import *
from .serializers import *
from django.db import transaction
from django.db.models import Sum, Q
from django.views.decorators.http import condition


def get_etag_year(request, pk_year):
    item = Year.objects.get(year=pk_year)
    key = f'{item.year}{item.description}'
    key = re.sub('[^A-Za-z0-9]+', '', key)
    request.META['HTTP_IF_MATCH']=key
    return key

def get_etag_user(request, pk_u):
    item = User.objects.get(index=pk_u)

    key = f'{item.created}'
    key = re.sub('[^A-Za-z0-9]+', '', key)
    request.META['HTTP_IF_MATCH']=key
    return key


def get_etag_income(request, pk_year, pk_inc):
    item = Income.objects.get(id=pk_inc, year=pk_year)
    key = f'{item.created}'
    key = re.sub('[^A-Za-z0-9]+', '', key)
    request.META['HTTP_IF_MATCH']=key
    return key

def get_etag_contribution(request,pk_year,pk_mem,pk_con):
    item = Contributions.objects.get(id=pk_con,member=pk_mem , year=pk_year)
    key = f'{item.date}{item.month}'
    key = re.sub('[^A-Za-z0-9]+', '', key)
    request.META['HTTP_IF_MATCH']=key
    return key

def get_etag_expenditure(request, pk_year, pk_exp):
    item = Expenditure.objects.get(id=pk_exp, year=pk_year)
    key = f'{item.created}'
    key = re.sub('[^A-Za-z0-9]+', '', key)
    request.META['HTTP_IF_MATCH']=key
    
    return key

@api_view(['GET','POST'])
def getYears(request):
    if request.method=='GET':
        items = Year.objects.all()
        paginator = PageNumberPagination()
        resources = paginator.paginate_queryset(items, request)
        serializer = YearSerializer(resources, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    if request.method=='POST':
        y = request.data['year']
        d = {'year':y}
        serializer = YearSerializer(data = d)
        
        if serializer.is_valid():
            serializer.save()
            print("saved")
            location = request.get_host()+"/api/years/"+str(y)
            resp = { "Location":location }
            print("po put:",resp)
            return Response(resp)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
@condition(etag_func=get_etag_year)
def getYear(request, pk_year):
    if request.method=='GET':
        item = Year.objects.get(year=pk_year)   
        serializer = YearSerializer(item)
        return Response(serializer.data)
    
    if request.method=='PUT':
        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
            if("year" not in request.data):
                request.data["year"]=pk_year
            student = Year.objects.get(year=pk_year)
            serializer = YearSerializer(instance=student ,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

    if request.method=='DELETE':
        student = Year.objects.get(year=pk_year)
        student.delete()
        return Response('Year succesfully delete!')



#{"year":2001, "description":"hahahah"}
#{"year":999,"description":"wtedy to było"}


#-----------------------------------------------

@api_view(['GET','POST'])
def getUsers(request):
    if request.method=='GET':
        items = User.objects.all()
        paginator = PageNumberPagination()
        resources = paginator.paginate_queryset(items, request)
        serializer = UserSerializer(resources, many=True)
        return paginator.get_paginated_response(serializer.data)

    if request.method=='POST':
        index = request.data['index']
        d = {'index':index}
        serializer = UserSerializer(data = d)
        
        if serializer.is_valid():
            serializer.save()
            location = request.get_host()+"/api/users/"+str(index)
            request.META['Content-Location']=location
            resp = { "Location":location }
            return Response(resp)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','DELETE','PUT','PATCH'])
@condition(etag_func=get_etag_user)
def getUser(request,pk_u):
    if request.method=='GET':
        items = User.objects.get(index=pk_u)
        serializer = UserSerializer(items)
        return Response(serializer.data)
    if request.method=='DELETE':
        student = User.objects.get(index=pk_u)
        student.delete()
        return Response('User succesfully delete!')
    if request.method=='PUT':
        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
            if("index" not in request.data):
                request.data["index"]=pk_u
            student = User.objects.get(index=pk_u)
            serializer = UserSerializer(instance=student ,data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

    if request.method=='PATCH':
        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
            if("index" not in request.data):
                request.data["index"]=pk_u
            student = User.objects.get(index=pk_u)
            serializer = UserSerializer(instance=student ,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

#----------------------------------------------

@api_view(['GET','PUT','DELETE'])
@condition(etag_func=get_etag_contribution)
def getContribution(request,pk_year,pk_mem,pk_con):
    
    if request.method=='GET':
        items = Contributions.objects.filter(id=pk_con,member=pk_mem , year=pk_year)
        serializer = ContributionsSerializer(items, many=True)
        return Response(serializer.data)

    if request.method=='PUT':
        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
        
            if('year' not in request.data.keys()):
                request.data["year"]=pk_year
            if(pk_mem not in request.data):
                request.data["member"]=pk_mem
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED)

        item = Contributions.objects.get(id=pk_con)
        serializer = ContributionsSerializer(instance=item ,data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    
    if request.method=='DELETE':
        item = Contributions.objects.filter(id=pk_con, year=pk_year, member=pk_con)
        item.delete()
        return Response('Contribution succesfully delete!')

@api_view(['GET','POST'])
def getContributions(request,pk_year, pk_mem):
    
    if request.method=='GET':
        items = Contributions.objects.filter(year=pk_year, member=pk_mem)
        paginator = PageNumberPagination()
        resources = paginator.paginate_queryset(items, request)
        serializer = ContributionsSerializer(resources, many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        if("year" not in request.data.keys()):
            request.data["year"]=pk_year
        if("member" not in request.data.keys()):
            request.data["member"]=pk_mem

        index = request.data["member"]
        year = request.data["year"]

        d = {'year':year,'member':index}
        print(d)
        serializer = ContributionsSerializer(data=d)
        if serializer.is_valid():
            serializer.save()
            id = serializer.data['id']
            location = request.get_host()+"/api/years/"+str(year)+"/members/"+str(index)+'/contributions/'+str(id)
            resp = Response({ "Location":location })
            request.META["CONTENT_LOCATION"]=location
            request.META["HTTP_REFERER"]=location

            return resp
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------------------

@api_view(['GET','PUT','DELETE','PATCH'])
@condition(etag_func=get_etag_income)
def getIncome(request,pk_year, pk_inc):
    
    if request.method=='GET':
        items = Income.objects.get(year=pk_year, id=pk_inc)
        serializer = IncomeSerializer(items)
        return Response(serializer.data)
    
    if request.method=='DELETE':
        item = Income.objects.filter(id=pk_inc, year=pk_year)
        item.delete()
        return Response('Income succesfully delete!')
    
    if request.method=='PUT':

        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
            if("year" not in request.data.keys()):
                request.data["year"]=pk_year
            item = Income.objects.get(id=pk_inc)
            serializer = IncomeSerializer(instance=item ,data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED) 
    
    if request.method=='PATCH':

        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
    
            if("year" not in request.data.keys()):
                request.data["year"]=pk_year
            
            item = Income.objects.get(id=pk_inc)
            serializer = IncomeSerializer(instance=item ,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED) 


@api_view(['GET','POST'])
def getIncomes(request,pk_year):
    if request.method=='GET':
        items = Income.objects.filter(year=pk_year)

        paginator = PageNumberPagination()
        resources = paginator.paginate_queryset(items, request)

        serializer = IncomeSerializer(resources, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    if request.method=='POST':
        if('year' not in request.data.keys()):
            request.data["year"]=pk_year
        year = request.data['year']    
        d = {'year':year}
        serializer = IncomeSerializer(data=d)
        if serializer.is_valid():
            serializer.save()
            id = serializer.data["id"]
            location = request.get_host()+"/api/years/"+str(year)+"/incomes/"+str(id)
            resp = { "Location":location }
            return Response(resp)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------------------

@api_view(['GET','PUT','DELTE','PATCH'])
@condition(etag_func=get_etag_expenditure)
def getExpenditure(request,pk_year, pk_exp):

    if request.method=='GET':

        items = Expenditure.objects.get(year=pk_year, id=pk_exp)
        serializer = ExpenditureSerializer(items)
        return Response(serializer.data)
    
    if request.method=='PUT':
        
        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
            if("year" not in request.data.keys()):
                request.data["year"]=pk_year
            item = Expenditure.objects.get(id=pk_exp)
            serializer = ExpenditureSerializer(instance=item ,data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED) 

    if request.method=='DELETE':
        
        item = Expenditure.objects.filter(id=pk_exp, year=pk_year)
        item.delete()
        return Response('Expenditure succesfully delete!')

    if request.method=='PATCH':

        if 'HTTP_IF_MATCH' in request.META.keys() and request.META['HTTP_IF_MATCH']:
            if("year" not in request.data.keys()):
                request.data["year"]=pk_year
            item = Expenditure.objects.get(id=pk_exp)
            serializer = ExpenditureSerializer(instance=item ,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_412_PRECONDITION_FAILED) 


@api_view(['GET','POST'])
def getExpenditures(request,pk_year):
    if request.method=='GET':

        items = Expenditure.objects.filter(year=pk_year)

        paginator = PageNumberPagination()
        resources = paginator.paginate_queryset(items, request)

        serializer = ExpenditureSerializer(resources, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    if request.method=='POST':

        if('year' not in request.data.keys()):
            request.data["year"]=pk_year
        year = request.data['year']    
        d = {'year':year}
        serializer = ExpenditureSerializer(data=d)
        if serializer.is_valid():
            serializer.save()
            id = serializer.data["id"]
            location = request.get_host()+"/api/years/"+str(year)+"/expenditures/"+str(id)
            resp = { "Location":location }
            return Response(resp)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
        i = income
    else:
        i = 0
    
    if(expenditure != None):
        e = expenditure
    else:
        e = 0
    
    if(contributions != None):
        c = contributions
    else:
        c = 0
        
    result = { "Wpływy":i+c,"Wydatki":e,"Bilans":i+c-e }

    return Response(result)




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
