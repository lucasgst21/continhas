from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Sum, Case, When, F, DecimalField
from django.utils import timezone
from django.views.generic import CreateView
from .models import Transaction, Account, Category
from .forms import TransactionForm, AccountForm, CategoryForm, SignUpForm

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    def get_success_url(self): return '/login/'

@login_required
def dashboard(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    tx = Transaction.objects.filter(owner=request.user, date__gte=month_start, date__lte=today)
    income = tx.filter(kind='IN').aggregate(total=Sum('amount'))['total'] or 0
    expense = tx.filter(kind='OUT').aggregate(total=Sum('amount'))['total'] or 0
    balance = income - expense
    by_cat = (tx.values('category__name').annotate(
        total=Sum(Case(
            When(kind='IN', then=F('amount')),
            When(kind='OUT', then=-F('amount')),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        ))).order_by('-total')[:8])
    recent = Transaction.objects.filter(owner=request.user).select_related('account','category')[:10]
    accounts = Account.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'income':income,'expense':expense,'balance':balance,'by_cat':by_cat,'recent':recent,'accounts':accounts})

@login_required
def transaction_list(request):
    tx = Transaction.objects.filter(owner=request.user).select_related('account','category')
    return render(request, 'transaction_list.html', {'transactions': tx})

@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            obj = form.save(commit=False); obj.owner = request.user; obj.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'transaction_form.html', {'form': form})

@login_required
def account_list(request):
    return render(request, 'account_list.html', {'accounts': Account.objects.filter(owner=request.user)})

@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False); a.owner = request.user; a.save()
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'account_form.html', {'form': form})

@login_required
def category_list(request):
    return render(request, 'category_list.html', {'categories': Category.objects.filter(owner=request.user)})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False); c.owner = request.user; c.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})
