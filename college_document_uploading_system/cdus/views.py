import django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from django.db.utils import DataError
from django.urls import reverse
from django.contrib.auth import hashers
from django.core import mail, cache
from django.db.models import Q
from . import models
import random
import string
import datetime
import random
from django.conf import settings
import sys

# Create your views here.
def index(request):
    return HttpResponse("FUC")
