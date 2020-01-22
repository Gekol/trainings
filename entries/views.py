from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Entry
from .forms import EntryForm, FilterForm
from django.urls import reverse
import datetime
import re
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Avg
# Create your views here.

def show_main(request):
    return render(request, "main_page.html")

@login_required(login_url="/users/login")
def show_entries(request):
    from_date = request.GET.get("date_from", None)
    to_date = request.GET.get("date_to", None)
    if from_date and to_date and re.match(r'\d\d\d\d-\d\d-\d\d', from_date) and re.match(r'\d\d\d\d-\d\d-\d\d', to_date):
        entries = Entry.objects.filter(owner=request.user, date__lte=to_date, date__gte=from_date)
    else:
        entries = Entry.objects.filter(owner=request.user).order_by("-date")
    distance = duration = 0
    for entry in entries:
        distance += entry.distance
        duration += entry.duration
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
    last_year_entries = Entry.objects.filter(owner=request.user, date__gte=start, date__lt=end).order_by("date")
    stats = []
    current_week = 0
    for entry in last_year_entries:
        isodata = entry.date.isocalendar()
        week = isodata[1]
        if (current_week < week):
            stats.append({"week": week, "distance": entry.distance, "duration": entry.duration, "number": 1})
            current_week = week
        elif current_week == week:
            stats[len(stats) - 1]["distance"] += entry.distance
            stats[len(stats) - 1]["duration"] += entry.duration
            stats[len(stats) - 1]["number"] += 1
        else:
            stats.append({"week": datetime.date(current_year - 1, 12, 24).isocalendar()[1] + 1, "distance": entry.distance, "duration": entry.duration, "number": 1})
            current_week = week
    for i in range(len(stats)):
        stats[i]["average"] = round((stats[i]["distance"] * 1000) / (stats[i]["duration"] * 60), 2)
    stats.reverse()
    return render(request, "statistics.html", {"stats": stats, "year": current_year - 1})