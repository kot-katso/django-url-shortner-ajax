from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from hashlib import md5

from .models import Url


# Create your views here.
def home(request):
    return render(request, 'index.html')


def shortner(request, hash_cd):
    is_vlaid = get_object_or_404(Url, hash_code=hash_cd)

    return redirect(is_vlaid.actual_url)
    

def list_url(request):
    urls = Url.objects.all().order_by('-created_at')

    context = {
        'urls': urls
    }

    return render(request, 'list.html', context)

def edit_url(request, pk):


    if request.method == 'POST':
        
        # get the url 
        url = request.POST['url']

        # get pk 
        pk = request.POST['pk']

        req_url = Url.objects.filter(pk=pk)

        if not req_url:
            return JsonResponse({
                'msg': 'There is something wrong!',
                'status': False
            })
        else:

            # create the url
            host = request.get_host()
            random_code = md5(url.encode()).hexdigest()[:10] 

            hash_link = 'http://'+host+'/shortner/'+random_code

            Url.objects.filter(pk=pk).update(actual_url=url, hash_url=hash_link, hash_code=random_code)

            return JsonResponse({
                'msg': 'Edited Successfully!',
                'status': True,
                'url': url
            })


    obj = get_object_or_404(Url, pk=pk)

    context = {
        'url': obj
    }

    return render(request, 'edit_url.html', context)

@require_http_methods(["POST"])
def create_url(request):

    # get the url 
    url = request.POST['url']

    # create the url in the database
    host = request.get_host()
    random_code = md5(url.encode()).hexdigest()[:10] 

    hash_link = 'http://'+host+'/shortner/'+random_code

    create = Url(actual_url=url, hash_url=hash_link, hash_code=random_code)
    create.save()

    return JsonResponse({
        'msg': 'Created Successfully!',
        'status': True
    })

@require_http_methods(["POST"])
def delete_url(request):
    url = get_object_or_404(Url, pk=request.POST['pk'])
    url.delete()
    return JsonResponse({
        'msg': 'Deleted Successfully!',
        'status': True
    })
