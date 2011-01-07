from django import forms
from django.utils.safestring import mark_safe

class RadioFieldImageRenderer(forms.widgets.RadioFieldRenderer):
    def render(self):
        """
        Outputs a <ul> for this set of radio fields.
        """
        output = []
        output.append('<table style="border: 0 solid black"><tr>')
        for choice in self.choices:
            output.append("""
<th style="border: 0 solid black">
<center>
<input type="radio" name="%s" value="%s" id="%s" >
%s
</center>
<br />
<img src="%s" height="130"/></th>""" % (self.name, choice['file_path'], self.attrs['id'], choice['label'], choice['media_path']))
        output.append('</tr></table>')
        return mark_safe(u''.join(output))
