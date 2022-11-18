from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Max
from django.template import loader
from .models import Members
from .forms import Trsc,Usearch,AddR,AddST,AddT,AddRT
import json

from home.models import RouteStation,Station,Route,Trains,Reservation,Payment
def getTrains(request):
    if request.method=='POST':
        form=Usearch(request.POST)
        if form.is_valid():

            data=form.cleaned_data
            src=data['src']
            des=data['des']
            a=RouteStation.objects.filter(sid=des)
            x=[]
            o=0
            for i in a:
                tno=i.tno
                b=RouteStation.objects.filter(tno=tno,sid=src)
                for j in b:
                    if j.order<i.order:
                        x.append(j)
                        o=i.order-j.order

        else:
            return HttpResponse('<h1>invalid Data</h1>')
        return render(request,'features/trains.html',{'data':x,'o':o,'src':src,'des':des})
    return HttpResponse('<h1>Wrong REq</h1>')




def schedule(request):
    a=Trains.objects.all()
    return render(request,'features/schedule.html',{'a':a})

def getTinfo(request):
    form=Trsc(request.GET)
    if form.is_valid():
        data=form.cleaned_data
        tno=data['tnum']
        a=RouteStation.objects.filter(tno=tno).order_by('order')


        return render(request,'features/trinfo.html',{'data':a})

    return HttpResponse('<h1>DAta invalid<h1>')







def search(request):
    a=Station.objects.all()
    return render(request,'features/seat.html',{'a':a})

def addR(request):
    if request.method == 'POST':
        form = AddR(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            a=Route()
            a.rid=data['rid']
            a.ostation=data['ostation']
            a.dstation=data['dstation']
            a.save()
            return redirect('/home/addR')
        else:
            return HttpResponse('<h1>Invalid Data</h1>')






    a=Station.objects.all()

    return render(request,'features/addR.html',{'stn':a})


def addST(request):
    if request.method == 'POST':
        form = AddST(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            a = Station()
            a.sid = data['sid']
            a.sname = data['sname']
            a.save()
            return redirect('/home/addST')
        else:
            return HttpResponse('<h1>Invalid Data</h1>')

    return render(request, 'features/addST.html')

def addT(request):
    if request.method == 'POST':
        form = AddT(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            a=Trains()
            a.tno=data['tno']
            a.tname=data['tname']
            r1=Route.objects.get(rid=data['rid'])
            a.rid=r1
            a.save()
            return redirect('/home/addT')
        else:
            return HttpResponse('<h1>Invalid Data</h1>')






    a=Route.objects.all()

    return render(request,'features/addT.html',{'tr':a})

def addRT(request):
    if request.method == 'POST':
        form = AddRT(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            a = RouteStation()
            t1= Trains.objects.get(tno=data['tno'])
            a.tno = t1
            s1=Station.objects.get(sid=data['sid'])
            a.sid = s1
            r1=Route.objects.get(rid=data['rid'])
            a.rid = r1
            a.order=data['order']
            a.atime=data['atime']
            a.save()
            return redirect('/home/addRT')
        else:
            return HttpResponse(form.errors)

    a = Route.objects.all()
    b=Trains.objects.all()
    c=Station.objects.all
    return render(request, 'features/addRT.html', {'rt': a,'tr':b,'st':c})


def cva(request):
    if request.method=='POST':
        tn1=request.POST['tno']
        o=int(request.POST['od'])

        cls=request.POST['cls']
        p=0
        if cls=='AC':
            p=120*o
        if cls=='SL':
            p=80*o
        if cls=='3A':
            p=100*o
        if cls=='2S':
            p=50*o
        dt=request.POST['dt']
        c=0
        a=Reservation.objects.filter(tno=tn1,cls=cls,date=dt)

        for i in a:
            c=c+i.nos
        if c>30:
            x="Waiting-"+str(c-30)
            data = json.dumps({
                'read': x,
                'price': p,
            })
            return HttpResponse(data,content_type='application/json')
        else:
            x="Available-"+str(30-c)
            data = json.dumps({
                'read': x,
                'price': p,
            })
            return HttpResponse(data,content_type='application/json')

def book1(request):
    if(request.method=='POST'):
        dt=request.POST['date']
        src=request.POST['src']
        des=request.POST['des']
        tno=request.POST['bk']
        cls = request.POST['cls'+str(tno)]
        nos=request.POST['nos'+str(tno)]
        pr=request.POST['price'+str(tno)]
        tname=Trains.objects.get(tno=tno).tname
        return render(request,'features/payment.html',{'price':int(pr)*int(nos),'dt':dt,'cls':cls,'tno':tno,'nos':nos,'tname':tname,'src':src,'des':des})


def book(request):

    if request.method=='POST':
        nos=int(request.POST['nos'])
        tno=request.POST['tno']
        dt=request.POST['date']
        tn1=Trains.objects.get(tno=tno)
        cls=request.POST['cls']
        op=request.POST['select']
        tname=request.POST['tname']
        src=request.POST['src']
        des=request.POST['des']
        price=int(request.POST['price'])
        pp=price/nos
        mtd='Paytm'
        if op=='option1':
            crd=request.POST['crd']
            nam=request.POST['nam']
            cvv=request.POST['cvv']
            exp=request.POST['exp']
            mtd='Credit/Debit Card'
            if len(crd)!=16 or len(cvv)!=3:
                return render(request,'features/nopay.html')


        c = 0
        f=0
        pay=Payment()
        pay.user=request.user
        pay.amt=price
        pay.date=dt
        pay.mtd=mtd
        pay.cancel='NO'

        a = Reservation.objects.filter(tno=tno, cls=cls, date=dt)
        c1=Reservation.objects.all()
        cp=0
        for i in c1:
            cp=max(cp,int(i.pnr))
        for i in a:
            c = c + i.nos
        if c<30:
            if nos>(30-c):
                b=Reservation()
                b.cls=cls
                b.tno=tn1
                b.status="C"
                b.nos=30-c
                b.amt=200
                b.date=dt
                b.user=request.user
                b.pnr=cp+1
                b.src=src
                b.des=des
                b.save()
                e = Reservation()
                e.cls = cls
                e.tno = tn1
                e.status = "W"
                e.nos = nos-(30 - c)
                e.amt = price
                e.date = dt
                e.user = request.user
                e.pnr = cp + 1
                e.src=src
                e.des=des
                e.save()
                f=1
            else:
                b = Reservation()
                b.cls = cls
                b.tno = tn1
                b.status = "C"
                b.nos = nos
                b.amt = price
                b.date = dt
                b.user = request.user
                b.pnr = cp + 1
                b.src=src
                b.des=des
                b.save()
                f = 1
        else:
            b = Reservation()
            b.cls = cls
            b.tno = tn1
            b.status = "W"
            b.nos = nos
            b.amt = price
            b.date = dt
            b.user = request.user
            b.pnr = cp + 1
            b.save()
            f=2
        c=0
        a = Reservation.objects.filter(tno=tno, cls=cls, date=dt)
        for i in a:
            c = c + i.nos

        pay.pnr = cp+1
        pay.save()
        return render(request,"features/final.html",{'tname':tname,'tno':tno,'date':dt,'src':src,'des':des,'cls':cls,'pnr':(cp+1),'nos':nos,'dt':dt})



def cancel(request):
    a=Reservation.objects.filter(user=request.user).values('pnr','date','tno','src','des','cls','nos').distinct()
    return render(request,'features/cancel.html',{'res':a})

def cn(request):

    if request.method=='POST':


        pnr=request.POST['id']
        a=Reservation.objects.filter(pnr=pnr)
        z=Payment.objects.filter(pnr=pnr,cancel='NO')
        for j in z:
            amt = j.amt
            j.cancel='YES'
            j.save()

        c=0
        cls='X'

        for i in a:
            if i.status=='C':
                c=c+i.nos
            cls=i.cls
        a.delete()
        a=Reservation.objects.all()
        f=0
        for i in a:
            if i.status=='W' and i.cls==cls:
                if i.nos<=c:
                    c=c-i.nos
                    i.status='C'
                    i.save()
                else:
                    f=1
                    b=Reservation()
                    b.cls = i.cls
                    b.tno = i.tno
                    b.status = "C"
                    b.nos = c
                    b.amt = 200
                    b.date = i.date
                    b.user = i.user
                    b.pnr = i.pnr
                    b.save()
                    i.nos=i.nos-c
                    i.save()
                    c=0
                    break
        return HttpResponse(amt)

def pnr(request):
    if request.method=='POST':
        pnr=request.POST['pnr']
        a=Reservation.objects.filter(pnr=pnr)

        return render(request,'features/pnr.html',{'r':a})


    return render(request,'features/pnr.html')





