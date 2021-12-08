from django.contrib import admin

# Register your models here.

from .models import *
from .forms import *

admin.site.register(Customer)
admin.site.register(Evaluation)
