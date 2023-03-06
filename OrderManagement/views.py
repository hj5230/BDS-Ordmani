from django import forms
from django.shortcuts import render, redirect
from OrderManagement import models
from OrderManagement.utils.secure import md5
from OrderManagement.utils.functions import *

'''website'''
class LoginForm(forms.Form):
    pid = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'margin-bottom: 15px',
            'placeholder': '用户名',
        }),
    )
    pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'margin-bottom: 15px',
            'placeholder': '密码',
        })
    )
    def cleanPassword(self):
        pwd = self.cleaned_data.get('pwd')
        return md5(pwd)

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(data=request.POST)
    if form.is_valid():
        admin = models.Personnel.objects.filter(**form.cleaned_data).first()
        if not admin:
            form.add_error('pwd', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        request.session['user'] = {'name': admin.name, 'pid': admin.pid, 'pos_id': admin.pos_id}
        request.session.set_expiry(60 * 60 * 2)
        return redirect('/dashboard/')
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.clear()
    return redirect('/login/')

def myProfile(request):
    pos = models.Position.objects.filter(
        id=request.session['user']['pos_id']
    ).first()
    return render(request, 'my_profile.html', {'pos': pos})

def dashBoard(request):
    return render(request, 'dashboard.html')

def notYetFinished(request):
    return render(request, 'not_yet_finished.html')

'''customer'''
class CustomerModel(forms.ModelForm):
    correspond = forms.ModelChoiceField(queryset=models.Personnel.objects.all())
    class Meta:
        model = models.Customer
        fields = ['cid', 'name', 'gender', 'phone', 'organization',
        'address', 'job_title', 'remark', 'correspond',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cid'].initial = getCid()
        for name, field in self.fields.items():
            field.widget.attrs = {
                'class': 'form-control',
                'style': 'margin-bottom: 15px',
                'placeholder': field.label,
            }

def customerMain(request):
    if request.method == 'GET':
        customers = models.Customer.objects.all()
        return render(request, 'customer_main.html', {'customers': customers})
    search = request.POST.get('search')
    matches = models.Customer.objects.filter(name__icontains=search) | models.Customer.objects.filter(cid__icontains=search) | models.Customer.objects.filter(phone__icontains=search)
    return render(request, 'customer_main.html', {'customers': matches})

def customerAdd(request):
    if request.method == 'GET':
        form = CustomerModel()
        return render(request, 'customer_add.html', {'form': form})
    form = CustomerModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/customer/main/')
    return render(request, 'customer_add.html', {'form': form})

def customerDel(request, cid):
    models.Customer.objects.filter(cid=cid).delete()
    return redirect('/customer/main/')

def customerEdit(request, cid):
    row = models.Customer.objects.filter(cid=cid).first()
    if request.method == 'GET':
        form = CustomerModel(instance=row)
        return render(request, 'customer_edit.html', {'form': form, 'cid': cid})
    form = CustomerModel(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect('/customer/main/')
    return render(request, 'customer_edit.html', {'form': form, 'cid': cid})

'''product'''
class ProductModel(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = ['rid', 'name', 'model', 'unit',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rid'].initial = getRid()
        for name, field in self.fields.items():
            field.widget.attrs = {
                'class': 'form-control',
                'style': 'margin-bottom: 15px',
                'placeholder': field.label,
            }

def productMain(request):
    if request.method == 'GET':
        products = models.Product.objects.all()
        return render(request, 'product_main.html', {'products': products})
    search = request.POST.get('search')
    matches = models.Product.objects.filter(name__icontains=search) | models.Product.objects.filter(rid__icontains=search)
    return render(request, 'product_main.html', {'products': matches})

def productAdd(request):
    if request.method == 'GET':
        form = ProductModel()
        return render(request, 'product_add.html', {'form': form})
    form = ProductModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/product/main/')
    return render(request, 'product_add.html', {'form': form})

def productDel(request, rid):
    models.Product.objects.filter(rid=rid).delete()
    return redirect('/product/main/')

def productEdit(request, rid):
    row = models.Product.objects.filter(rid=rid).first()
    if request.method == 'GET':
        form = ProductModel(instance=row)
        return render(request, 'product_edit.html', {'form': form, 'rid': rid})
    form = ProductModel(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect('/product/main/')
    return render(request, 'product_edit.html', {'form': form, 'rid': rid})

'''order'''
class OrderModel(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=models.Customer.objects.all())
    form_maker = forms.ModelChoiceField(queryset=models.Personnel.objects.all())
    class Meta:
        model = models.OrderTable
        fields = ['oid', 'date', 'customer', 'receiver', 'pay_method',
            'delivery', 'freight', 'remark', 'phone', 'form_maker',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['oid'].initial = getOid()
        self.fields['date'].initial = getDate()
        # self.fields['form_maker'].initial = request.session['user']
        for name, field in self.fields.items():
            field.widget.attrs = {
                'class': 'form-control',
                'style': 'margin-bottom: 15px',
                'placeholder': field.label,
            }

def orderMy(request):
    if request.method == 'GET':
        orders = models.OrderTable.objects.all()
        return render(request, 'order_my.html', {'orders': orders})
    search = request.POST.get('search')
    matches = models.OrderTable.objects.filter(oid__icontains=search)
    return render(request, 'order_my.html', {'orders': matches})

def orderCreate(request):
    oid = getOid()
    if request.method == 'GET':
        form = OrderModel()
        return render(request, 'order_create.html', {'form': form})
    form = OrderModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/order/addproduct/'+str(oid)+'/')
    return render(request, 'order_create.html', {'form': form})

def orderCustomer(request, cid):
    oid = getOid()
    if request.method == 'GET':
        form = OrderModel()
        obj = models.Customer.objects.filter(cid=cid)
        form.fields['customer'] = forms.ModelChoiceField(queryset=obj,
            initial=1, widget=forms.Select(attrs={
                    'class': 'form-control',
                    'style': 'margin-bottom: 15px',
                }))
        return render(request, 'order_create.html', {'form': form})
    form = OrderModel(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/order/addproduct/'+str(oid)+'/')
    return render(request, 'order_create.html', {'form': form})

def orderDel(request, oid):
    models.OrderTable.objects.filter(oid=oid).delete()
    return redirect('/order/my/')

def orderReview(request, oid):
    oid = str(oid)
    order = models.OrderTable.objects.filter(oid=oid).first()
    if request.method == 'GET':
        includes = models.Include.objects.filter(oid_id=oid)
        products = [{include.id: (include.amount, include.univalent)} for include in includes]
        includes = []
        for product in products:
            for _, __ in product.items():
                rid = models.Include.objects.filter(id=_).first().rid_id
                includes.append({models.Product.objects.filter(rid=rid).first(): [_, __]})
        form = OrderModel(instance=order)
        customer = models.Customer.objects.filter(cid=order.customer_id).first()
        return render(request, 'order_review.html', {'includes': includes, 'order': form, 'oid':oid, 'customer': customer.name})
    form = OrderModel(data=request.POST, instance=order)
    if form.is_valid():
        form.save()
        return redirect('/order/my/')
    return render(request, 'order_review.html', {'includes': includes, 'order': form, 'oid':oid, 'customer': customer.name})
    
'''include'''
class IncludeModel(forms.ModelForm):
    rid = forms.ModelChoiceField(queryset=models.Product.objects.all())
    class Meta:
        model = models.Include
        fields = ['oid', 'rid', 'amount', 'univalent',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {
                'class': 'form-control',
                'style': 'margin-bottom: 15px',
                'placeholder': field.label,
            }

def addProduct(request, oid):
    oid = int(oid)
    row_order = models.OrderTable.objects.filter(oid=oid).first()
    order = OrderModel(instance=row_order)
    includes = models.Include.objects.filter(oid_id=oid)
    products = [{include.rid_id: (include.amount, include.univalent)} for include in includes]
    includes = []
    for product in products:
        for _, __ in product.items():
            includes.append({models.Product.objects.filter(rid=_).first(): __})
    if request.method == 'GET':
        form = IncludeModel()
        return render(request, 'addproduct.html', {'form': form, 'order': order, 'oid': oid, 'includes': includes})
    form = IncludeModel(data=request.POST)
    if 'done' in request.POST:
        if form.is_valid():
            form.save()
            return redirect('/order/my/')
        return render(request, 'addproduct.html', {'form': form, 'order': order, 'oid': oid, 'includes': includes})
    if form.is_valid():
        form.save()
        return redirect('/order/addproduct/'+str(oid)+'/')
    return render(request, 'addproduct.html', {'form': form, 'order': order, 'oid': oid, 'includes': includes})

def includeEdit(request, id):
    include = models.Include.objects.filter(id=id).first()
    order = models.OrderTable.objects.filter(oid=include.oid_id).first()
    if request.method == 'GET':
        customer = models.Customer.objects.filter(cid=order.customer_id).first()
        orderForm = OrderModel(instance=order)
        includeForm = IncludeModel(instance=include)
        return render(request, 'include_edit.html', {'include': includeForm, 'order': orderForm, 'oid': include.oid_id, 'customer': customer.name})
    form = IncludeModel(data=request.POST, instance=include)
    if form.is_valid():
        form.save()
        return redirect('/order/review/%d/'%(include.oid_id))
    return render(request, 'include_edit.html', {'include': includeForm, 'order': orderForm, 'oid': include.oid_id, 'customer': customer.name})

def includeDel(request, id):
    oid = models.Include.objects.filter(id=id).first().oid_id
    models.Include.objects.filter(id=id).delete()
    return redirect('/order/review/%d/'%(oid))