from django.shortcuts import render, redirect
from .models import Product
from ..login_app.models import Person
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        user = Person.objects.get(id=request.session['user_id'])
        context = {
            'data': user,
            #grab specifically the ones that user added
            'items': Product.objects.all().filter(group=user),
            #grab everything else except the ones that user added
            'users': Product.objects.all().exclude(group=user)
        }
        return render(request, 'wish_app/index.html', context)
    else:
        return redirect(reverse('login:index'))

def create(request):
    return render(request, 'wish_app/create.html')

def process(request):
    #bring in 'results' from addProduct! just like login/reg
    if request.method == 'POST':
        user = Person.objects.get(id=request.session['user_id'])
        result = Product.objects.addProduct(request.POST, user)
        if result[0] == True:
            messages.success(request, result[1])
            return redirect(reverse('wishlist:index'))
        else:
            for error in result[1]:
                messages.error(request, error)
            return redirect(reverse('wishlist:create'))

def display(request, item_id):
    item = Product.objects.get(id=item_id)
    context = {
        'items': item,
        'users': item.group.all()
    }
    return render(request, 'wish_app/display.html', context)

def join(request, item_id):
    #bring in 'results' from joinProduct
    user = Person.objects.get(id=request.session['user_id'])
    result = Product.objects.joinProduct(item_id, user)
    messages.success(request, result[1])
    return redirect(reverse('wishlist:index'))

def delete(request, item_id):
    # DELETE the item completely from the data
    Product.objects.get(id=item_id).delete()
    messages.success(request, "Successfully deleted")
    return redirect(reverse('wishlist:index'))

def remove(request, item_id):
    # remove from my wish list but do not delete from the data
    user = Person.objects.get(id=request.session['user_id'])
    item = Product.objects.get(id=item_id)
    item.group.remove(user)
    messages.success(request, "Successfully removed from Wishlist")
    return redirect(reverse('wishlist:index'))

def logout(request):
    request.session.clear()
    return redirect(reverse('login:index'))
