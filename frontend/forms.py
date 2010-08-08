from django import forms

# default is required = True
class TagCloudForm(forms.Form):
    help_text = {
        'body' : 'This is the minimum required field.',
        'strip' : 'Default is True.',
        'max_size' : 'Maximum word size in px. Default is 20px.',
        'min_size' : 'Minimum word size in px. Default is 10px.',
        'width' : 'Width of the div containing the tag cloud in px. Default is 400px',
        'height' : 'Height of the div containing the tag cloud in px. Default is None, to allow the height to accomodate as many words as needed.',
        'tokenizer' : 'You may specify a custom tokenizer if you like, by passing in a <a href="http://docs.python.org/library/re.html">python regular expression</a>'
    }

    body = forms.CharField(widget=forms.Textarea(attrs={'rows':'20', 'cols':60 }), help_text = help_text['body'])
    strip = forms.BooleanField(initial=True, help_text = help_text['strip'], required=False)
    max_size = forms.IntegerField(help_text = help_text['max_size'], required=False)
    min_size = forms.IntegerField(help_text = help_text['min_size'], required=False)
    width = forms.IntegerField(help_text = help_text['width'], required=False)
    height = forms.IntegerField(help_text = help_text['height'], required=False)
    tokenizer = forms.CharField(help_text = help_text['tokenizer'], required=False)

