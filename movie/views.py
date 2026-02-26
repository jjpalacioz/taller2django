
from django.shortcuts import render
from .models import Movie
import matplotlib.pyplot as plt
import matplotlib, io, base64

def home(request):
    return render(request,'movie/home.html',{'movies':Movie.objects.all()})

def statistics(request):
    matplotlib.use('Agg')
    data={}
    for m in Movie.objects.all():
        data[m.year]=data.get(m.year,0)+1
    plt.bar(data.keys(),data.values())
    plt.xticks(rotation=90)
    buf=io.BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    graphic=base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    return render(request,'movie/statistics.html',{'graphic':graphic})

def signup(request):
    return render(request,'movie/signup.html',{'email':request.GET.get('email')})
