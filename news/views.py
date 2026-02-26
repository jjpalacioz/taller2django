
from django.shortcuts import render
from .models import News
def news_list(request):
    return render(request,'news/news.html',{'news':News.objects.all().order_by('-date')})
