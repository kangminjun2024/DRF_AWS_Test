from django.shortcuts import render
from django.core.cache import cache
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

# Create your views here.

@api_view(["GET"])
def product_list(request):
    cache_key = "product_lsit"  # 일단 캐쉬 키를 만들어 두고
    
    if not cache.get(cache_key):    #해당 키가 없으면   키에다가 값 넣어
        print("cache miss")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        json_response = serializer.data
        cache.set(cache_key, json_response, 100)    # 캐쉬를 써서 넣어주는거다    3번째 인자는 해당 캐시를 몇초 유지할 것인지
        
    response_data = cache.get(cache_key)
    return Response(response_data)