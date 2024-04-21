from django.shortcuts import render,redirect
from .forms import ExpenseForm,UserRegistrationForm
from .models import Expense
import datetime
from django.db.models import Sum
from django.contrib.auth import logout

def index(request):
    if request.method=="POST":
        expense=ExpenseForm(request.POST)
        if expense.is_valid():
            user_expense = expense.save(commit=False)
            user_expense.person=request.user
            user_expense.save()

    expenses=Expense.objects.filter(person=request.user)  
    total_expenses=expenses.aggregate(Sum('amount')) 

    last_year=datetime.date.today()-datetime.timedelta(days=365)
    data=Expense.objects.filter(person=request.user, date__gt=last_year)
    yearly_sum=data.aggregate(Sum('amount'))

    last_month=datetime.date.today()-datetime.timedelta(days=30)
    data=Expense.objects.filter(person=request.user,date__gt=last_month)
    monthly_sum=data.aggregate(Sum('amount'))

    last_week=datetime.date.today()-datetime.timedelta(days=7)
    data=Expense.objects.filter(person=request.user,date__gt=last_week)
    weekly_sum=data.aggregate(Sum('amount'))

    daily_sums=Expense.objects.filter(person=request.user).values('date').order_by('date').annotate(sum=Sum('amount'))

    categorical_sums=Expense.objects.filter(person=request.user).values('category').order_by('category').annotate(sum=Sum('amount'))
    
    expense_form=ExpenseForm()
    return render(request,'myapp/index.html',{'expense_form':expense_form,'expenses':expenses,'total_expenses':total_expenses,'yearly_sum':yearly_sum,'monthly_sum':monthly_sum,'weekly_sum':weekly_sum,'daily_sums':daily_sums,'categorical_sums':categorical_sums})



def edit(request,id):
    expense=Expense.objects.get(id=id)
    if expense.person != request.user:
        return redirect('invalid')
    expense_form=ExpenseForm(instance=expense)
    if request.method=="POST":
        expense=Expense.objects.get(id=id)
        form=ExpenseForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request,'myapp/edit.html',{'expense_form':expense_form})



def delete(request,id):
    if request.method=='POST' and 'delete' in request.POST:
        expense=Expense.objects.get(id=id)
        if expense.person != request.user:
            return redirect('invalid')
        expense.delete()
    return redirect('index')



def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        new_user = user_form.save(commit=False)
        new_user.set_password(user_form.cleaned_data['password'])
        new_user.save()
        return redirect('index')
    user_form=UserRegistrationForm()
    return render(request,'myapp/register.html',{'user_form':user_form})


def logout_view(request):
    logout(request)
    return render(request, 'myapp/logout.html')



def invalid(request):
    return render(request,'myapp/invalid.html')
