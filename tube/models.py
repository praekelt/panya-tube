from django.db import models

from panya.models import ModelBase

class AgeRestriction(models.Model):
    """
    Simple age restriction model.
    """
    age = models.IntegerField(
        help_text="Rating age, i.e. 13, 18 etc.",
    )
    symbol = models.CharField(
        max_length=128,
        help_text='Rating symbol, i.e. PG, SN, R, G etc.',
        blank=True,
        null=True,
    )
    description = models.TextField(
        help_text='A short description. Usually an explanation of the symbol, i.e. Parental Guidance Suggested. Some material may not be suitable for children.',
        blank=True,
        null=True,
    )

class Channel(ModelBase):
    """
    Basic channel model.
    """
    age_restriction = models.ForeignKey(
        'tube.AgeRestriction',
        blank=True,
        null=True,
    )

class ClipBase(ModelBase):
    """
    Model defining clip metadata. Clip types should inherit from this model.
    I.e. Dexter - Dex Lies and Videotape.
    """
    duration = models.IntegerField(
        help_text="Duration of this clip in seconds. This is automatically determined from the media resource.",
        blank=True,
        null=True,
    )
    age_restriction = models.ForeignKey(
        'tube.AgeRestriction',
        blank=True,
        null=True,
    )
    channel = models.ForeignKey(
        'tube.Channel',
        help_text="Select a channel for which this clip should be available. This field is only honoured when a series is not specified. If a series is specified its channel takes priority.",
        blank=True,
        null=True,
    )
    series = models.ForeignKey(
        'tube.Series',
        help_text="Select a series for which this clip is an episode.",
        blank=True,
        null=True,
    )
    
    def get_channel(self):
        """
        Get channel for this clip.
        Return the series' channel if series is populated, otherwise channel.
        If no series or channel is populated return None.
        """
        # Return show's channel if this clip has a show associated with it.
        if self.series:
            if self.series.channel:
                return self.series.channel
        
        # Otherwise, return channel if this clip has a channel associated with it.
        if self.channel:
            return self.channel
       
        return None
    
    def get_channel_id(self):
        channel = self.get_channel()
        return channel.content_id if channel else None
            
    def get_series_title(self):
        return self.series.title if self.series else ''
        
    def get_series_id(self):
        return self.series.id if self.series else ''

    @property
    def duration_as_hours_minute_seconds(self):
        return {'hours': self.duration/60/60, 'minutes': (self.duration % 3600) / 60, 'seconds': self.duration % 60}
   
class MediaResourceAbstractClip(models.Model):
    """
    Abstract clip model with local media resource.
    """
    media_resource = models.FileField(
        help_text="Upload the media file for this clip.",
        upload_to='tube_clip_resources',
        blank=True,
        null=True,
    )

    class Meta():
        abstract = True

class Clip(ClipBase, MediaResourceAbstractClip):
    """
    Concrete Clip model with local media resource.
    """
    pass

class Episode(models.Model):
    """
    Model storing metadata associated with episode.
    I.e. Dexter - Dex Lies and Videotape, Season 2 Episode 6.
    """
    clip = models.ForeignKey(
        'tube.ClipBase',
    )
    season = models.ForeignKey(
        'tube.Season',
    )
    episode_number = models.IntegerField(
        help_text="Episode number of this clip.",
        blank=True,
        null=True,
    )
    
class Season(models.Model):
    """
    Model storing metadata associated with season.
    I.e. Simpsons Season 2.
    """
    clips = models.ManyToManyField(
        'tube.ClipBase',
        through='tube.Episode',
        blank=True,
        null=True,
    )

class Series(ModelBase):
    """
    Model storing metadata associated with series.
    I.e. Law & Order.
    """
    pass
