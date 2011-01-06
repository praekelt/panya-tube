from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from panya.admin import ModelBaseAdmin
from tube.models import AgeRestriction, Channel

class ChannelAdmin(ModelBaseAdmin):
    def queryset(self, request):
        """
        Limit queryset to Channel objects (those of content type Channel)
        """
        channel_type = ContentType.objects.get_for_model(Channel)
        return self.model.objects.filter(content_type=channel_type)

admin.site.register(AgeRestriction)
admin.site.register(Channel, ChannelAdmin)
