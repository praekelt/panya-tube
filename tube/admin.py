from django.contrib import admin

from panya.admin import ModelBaseAdmin
from tube.models import Channel

admin.site.register(Channel, ModelBaseAdmin)
