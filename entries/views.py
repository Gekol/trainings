from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Entry
from .forms import EntryForm, FilterForm
from django.urls import reverse
import datetime
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Avg
# Create your views here.

def show_main(request):
    return render(request, "main_page.html")

@login_required(login_url="/users/login")
def show_entries(request):
    fromDate = request.GET.get("date_from", None)
    toDate = request.GET.get("date_to", None)
    if fromDate and toDate:
        entries = Entry.objects.filter(owner=request.user, date__lte=toDate, date__gte=fromDate)
    else:
        entries = Entry.objects.filter(owner=request.user).order_by("-date")
    distance = duration = 0
    for entry in entries:
        distance += entry.distance
        duration += entry.duration
    # print(entries)
    data = {"entries": entries, "form": FilterForm()}
    if entries:
        data["added"] = True
    else:
        data["added"] = False
    if (duration):
        data["average"] = round((distance * 1000) / (duration * 60), 2)
    return render(request, "entries.html", data)

@login_required(login_url="/users/login")
def add_entry(request):
    if (request.method == "POST"):
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            if entry.duration > 0 < entry.distance:
                entry.owner = request.user
                entry.save()
                return redirect(reverse("entries:entries"))
        else:
            return
    return render(request, "add_entry.html", {"form": EntryForm()})

@login_required(login_url="/users/login")
def delete_entry(request, id):
    entry = Entry.objects.get(id=id)
    entry.delete()
    return redirect(reverse("entries:entries"))

def statistics(request):
    current_year = datetime.date.today().year
    start = datetime.date(current_year - 1, 1, 1)
    end = datetime.date(current_year, 1, 1)
    last_year_entries = Entry.objects.filter(date__gte=start, date__lt=end)
    stats = []
    current_week = 1
    for i in range(last_year_entries):
        isodata = last_year_entries[i].date.isocalendar()
        year = isodata[0], week = isodata[1]
        if (current_week < week):
            pass
    print(stats)
    return render(request, "statistics.html", {"entries": last_year_entries})