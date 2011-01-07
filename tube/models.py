from django.db import models

from panya.models import ModelBase

class AbstractClip(models.Model):
    class Meta:
        abstract = True

    age_restriction = models.ForeignKey(
        'tube.AgeRestriction',
        blank=True,
        null=True,
    )
    show = models.ForeignKey(
        'tube.Show',
        help_text="Select a show for which this clip is an episode.",
        blank=True,
        null=True,
    )
    channel = models.ForeignKey(
        'tube.Channel',
        help_text="Select a channel on which this clip will be displayed. This field is only honoured when a show is not specified. If a show is specified its channel field takes priority.",
        blank=True,
        null=True,
    )
    season = models.IntegerField(
        help_text="Season number of this clip.",
        blank=True,
        null=True,
    )
    episode = models.IntegerField(
        help_text="Episode number of this clip.",
        blank=True,
        null=True,
    )
    duration = models.IntegerField(
        help_text="Duration of this clip in seconds. This is automatically determined from the uploaded clip and should only be manually specified if you really know what you are doing.",
        blank=True,
        null=True,
    )

    def get_channel(self):
        """
        Get channel for this clip.
        Return the show's channel is show is populated, otherwise channel.
        If no show or channel is populated return None.
        """
        # Return show's channel if this clip has a show associated with it.
        if self.show and self.show.channel:
            return self.show.channel
        
        # Otherwise, return channel if this clip has a channel associated with it.
        if self.channel:
            return self.channel
       
        return None
    
    def get_channel_id(self):
        channel = self.get_channel()
        return channel.content_id if channel else None
            
    def get_show_title(self):
        return self.show.title if self.show else ''
        
    def get_show_id(self):
        return self.show.id if self.show else ''


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
    Base channel model from which all Channel types should inherit.
    """
    age_restriction = models.ForeignKey(
        'tube.AgeRestriction',
        blank=True,
        null=True,
    )
