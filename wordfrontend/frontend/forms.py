from django import forms

# default is required = True
class TagCloudForm(forms.Form):
    help_text = {
        'body' : 'One of either "url", "body" or "freqs" fields are the minimum required field. Use the body field if you would like to type or paste your text inline (eg. into this box)',
        'url' : 'One of either "url" or "body" or "freqs" fields are the minimum required field. Use the url field if you would like text from the specified url to be used for the tag cloud.',
        'strip' : 'Strip any html markup. Default is True.',
        'max_size' : 'Maximum word size in px. Default is 70px.',
        'min_size' : 'Minimum word size in px. Default is 10px.',
        'width' : 'Width of the div containing the tag cloud in px. Default is none-- eg. the div will be as wide as the div it is contained by.%',
        'height' : 'Height of the div containing the tag cloud in px. Default is None, to allow the height to accomodate as many words as needed.',
        'tokenizer' : 'You may specify a custom tokenizer if you like, by passing in a <a href="http://docs.python.org/library/re.html">python regular expression</a>',
        'max_words' : 'Maximum number of words to be included in the tag cloud (will always truncate least frequent words)',
        'normalize' : "this option will normalize the case of all words, making 'Hello' and 'hello' equivalent",
        'stopwords' : "Whether or not to remove (exclude) common english words (so-called 'stop words' from the tag cloud, such as 'the' and 'it'. Default is True.",
        'sort_order' : 'What order should the words be sorted in? Options are frequency, random, or alphabetical. In practice random seems to look best most of the time, but try different ones and see what you like.',
        'freqs' : "Enter in a dictionary of word:frequency counts",
    }

    allowed_sort_orders = [('random', 'random'), ('frequency', 'frequency'),
                           ('alphabetical', 'alphabetical (not implemented)')]

    body = forms.CharField(widget=forms.Textarea(attrs={'rows':'20', 'cols':60 }), help_text = help_text['body'], required=False)
    url = forms.CharField(help_text = help_text['url'], required=False)
    freqs = forms.CharField(help_text = help_text['freqs'], required=False)
    max_words =  forms.IntegerField(help_text = help_text['max_words'], required=False)
    start_color = forms.CharField(required=False)
    end_color = forms.CharField(required=False)
    color_steps = forms.IntegerField(required=False)
    strip = forms.BooleanField(initial=True, help_text = help_text['strip'], required=False)
    normalize = forms.BooleanField(initial=True, help_text = help_text['normalize'], required=False)
    remove_stopwords = forms.BooleanField(initial=True, help_text = help_text['stopwords'], 
                        required=False)
    max_size = forms.IntegerField(help_text = help_text['max_size'], required=False)
    min_size = forms.IntegerField(help_text = help_text['min_size'], required=False)
    tokenizer = forms.CharField(help_text = help_text['tokenizer'], required=False)
    width = forms.IntegerField(help_text = help_text['width'], required=False)
    height = forms.IntegerField(help_text = help_text['height'], required=False)
    sort_order = forms.ChoiceField(help_text= help_text['sort_order'], required=False, choices = allowed_sort_orders) 

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        body = cleaned_data.get('body')
        freqs = cleaned_data.get('freqs')
        if not url and not body and not freqs:
            raise forms.ValidationError('You must specify one of "url", "body" or "freqs" fields')
        if (url and body) or (url and freqs) or (body and freqs):
            raise forms.ValidationError('Specify only one of "url" or "body" or "freqs" fields')

        start_color = cleaned_data.get('start_color')
        end_color = cleaned_data.get('end_color')
        color_steps = cleaned_data.get('color_steps')
        if start_color or end_color or color_steps:
            if not (start_color and end_color and color_steps):
                raise forms.ValidationError('To customize the color scheme, please enter all color scheme information: start color, end color, and number of steps to extrapolate in between.')

        return cleaned_data
