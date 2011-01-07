import math
import mimetypes
import os
import subprocess
import tempfile

from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from panya.admin import ModelBaseAdmin
from tube.models import AgeRestriction, Channel, Clip, Series
from tube.widgets import RadioFieldImageRenderer

import pyffmpeg

class ChannelAdmin(ModelBaseAdmin):
    def queryset(self, request):
        """
        Limit queryset to Channel objects (those of content type Channel)
        """
        channel_type = ContentType.objects.get_for_model(Channel)
        return self.model.objects.filter(content_type=channel_type)

class ClipForm(forms.ModelForm):
    image_choice = forms.fields.CharField(
        widget=forms.RadioSelect(
            renderer=RadioFieldImageRenderer
        ),
        required=False,
        help_text='Upload a media resource above to enable scraped image selection.'
    )
    
    class Meta:
        model = Clip

    def __init__(self, *args, **kwargs):
        super(ClipForm, self).__init__(*args, **kwargs)
       
        # Generate choices from scraped thumbnails.
        if not self.is_bound or self.errors:
            choices = []
            instance = self.instance
            if instance.media_resource:
                thumb_paths = self.generate_thumbs(instance.media_resource)

                if thumb_paths:
                    for idx, val in enumerate(thumb_paths):
                        choices.append({'file_path': val['file_path'], 'media_path': val['media_path'], 'label': 'Scraped Image %s' % (idx + 1)})
        
                    self.fields['image_choice'].widget.choices = choices
                    self.fields['image_choice'].help_text='Select a scraped image you want to use for this clip. Alternatively upload a custom image below.'

    def generate_thumbs(self, resource):
        """
        Generate image thumbnails from provided media resource.
        """
        # Open video stream.
        stream = pyffmpeg.VideoStream()
        try:
            stream.open(resource.path)
        except:
            stream.close()
            # Fail silently if something goes wrong during stream opening.
            return None

        # Calculate frame indexes from which to generate thumbs.
        fps = stream.tv.get_fps()
        duration = stream.vr.duration_time()
        frame_count = int(math.floor(duration) * math.floor(fps))
        frame_indexes = range(0, frame_count, frame_count / 4)[:4]

        # Offset first frame by 3 seconds.
        frame_indexes[0] = int(fps) * 3

        paths = []
        for index in frame_indexes:
            # Get image from stream.
            try:
                image = stream.GetFrameNo(index)
                file_name = '%s.thumb%s.png' % (resource.name.split('/')[-1], index)
                file_path = '%s%s' % (settings.MEDIA_ROOT, file_name)
                image.save(file_path, 'PNG')
                paths.append({'file_path': file_path, 'media_path': '%s%s' % (settings.MEDIA_URL, file_name)})
            except IOError, e:
                # Abort if we can not scrape images. most likely means something is wrong with the clip.
                return None

        stream.close()
        return paths

    def clean_media_resource(self):
        """
        Validate provided media format against ffmpeg by trying to grab a frame from it.
        Automatically assume format is invalid if it doesn't have a video mimetype.
        """
        error_msg = "Unsupported media format."
        data = self.cleaned_data['media_resource']
        
        # Only validate on change.
        if 'media_resource' not in self.changed_data:
            return data

        # Check for video mimetype.
        if 'video' not in data.content_type:
            raise forms.ValidationError(error_msg)
            
        # Create temp file and dump uploaded data to it.
        temp_filename = tempfile.mkstemp("-validate-%s" % data.name)[1]
        temp_file = open(temp_filename, 'wb')
        for chunk in data.chunks():
            temp_file.write(chunk)
        temp_file.close()

        # Try to grab a frame through ffmpeg and record the process result.
        temp_image_filename = '%s.png' % temp_filename
        result = subprocess.call(['ffmpeg', '-vframes', '1', '-i', temp_filename, temp_image_filename])

        # Remove temp files.
        os.remove(temp_filename)
        os.remove(temp_image_filename)

        # If ffmpeg failed assume the format is invalid
        if result != 0:
            raise forms.ValidationError(error_msg)
        else:
            return data
        
class ClipAdmin(ModelBaseAdmin):
    form = ClipForm
    
    def __init__(self, model, admin_site):
        from copy import deepcopy
        super(ClipAdmin, self).__init__(model, admin_site)
        fieldsets = deepcopy(self.fieldsets)
        for fieldset in fieldsets:
            if fieldset[0] == 'Image':
                fieldset[1]['fields'] = ('image_choice',) + fieldset[1]['fields']

        self.fieldsets = fieldsets
    
    def assign_image_to_field(self, file_path, field):
        f = open(file_path, 'r')
        
        # guess content type from filename
        content_type = mimetypes.guess_type(file_path)[0]
        # calc size
        size = len(f.read())

        # create InMemoryUploadedFile
        field_file = InMemoryUploadedFile(f, field.field.name, file_path, content_type, size, None)
        # save field file to field
        field.save(field_file.name, field_file)

        f.close()
    
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if 'image_choice' in form.changed_data:
            file_path = form.cleaned_data['image_choice']
            self.assign_image_to_field(file_path, obj.image)
        
        obj.save()

admin.site.register(AgeRestriction)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Clip, ClipAdmin)
admin.site.register(Series, ModelBaseAdmin)
