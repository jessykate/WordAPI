from django import forms

# default is required = True
class TagCloudForm(forms.Form):
    help_text = {
        'body' : 'Paste your text inline (eg. into this box)',
        'url' : 'Retrieve text from the specified url.',
        'file' : 'Upload a file',
        'freqs' : "Enter in a dictionary of word:frequency counts",
        'strip' : 'Strip any html markup. Default is True.',
        'max_size' : 'Maximum word size (px). Default 70px.',
        'min_size' : 'Minimum word size (px). Default 10px.',
        'width' : 'Width of the div containing the tag cloud (px). Default none.',
        'height' : 'Height of the div containing the tag cloud (px). Default None.',
        'tokenizer' : 'Specify a custom tokenizer, by passing in a <a href="http://docs.python.org/library/re.html">python regular expression</a>',
        'max_words' : 'Maximum number of words to be included in the tag cloud (will always truncate least frequent words)',
        'normalize' : "Normalize the case of all words, making 'Hello' and 'hello' equivalent",
        'stopwords' : "Remove (exclude) common english words (so-called 'stop words'), such as 'the' and 'it'. Default True.",
        'sort_order' : 'What order should the words be sorted in?',
    }

    allowed_sort_orders = [('random', 'random'), ('frequency', 'frequency'),
                           ('alphabetical', 'alphabetical (not implemented)')]

    body = forms.CharField(widget=forms.Textarea(attrs={'rows':'20', 'cols':60 }), help_text = help_text['body'], required=False, label="Text")
    url =           forms.CharField(help_text = help_text['url'], required=False)
    file =          forms.FileField(help_text = help_text['file'], required=False)
    # this is an option in the API but not likely to be useful in the frontend
    #freqs =         forms.CharField(help_text = help_text['freqs'], required=False)
    max_words =     forms.IntegerField(help_text = help_text['max_words'], required=False)
    start_color =   forms.CharField(required=False)
    end_color =     forms.CharField(required=False)
    color_steps =   forms.IntegerField(required=False)
    strip =         forms.BooleanField(initial=True, help_text = help_text['strip'], required=False)
    normalize =     forms.BooleanField(initial=True, help_text = help_text['normalize'], required=False)
    remove_stopwords = forms.BooleanField(initial=True, help_text = help_text['stopwords'], 
                    required=False)
    max_size =      forms.IntegerField(help_text = help_text['max_size'], required=False)
    min_size =      forms.IntegerField(help_text = help_text['min_size'], required=False)
    tokenizer =     forms.CharField(help_text = help_text['tokenizer'], required=False)
    width =         forms.IntegerField(help_text = help_text['width'], required=False)
    height =        forms.IntegerField(help_text = help_text['height'], required=False)
    sort_order =    forms.ChoiceField(help_text= help_text['sort_order'], required=False, 
                    choices = allowed_sort_orders) 

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        body = cleaned_data.get('body')
        file = cleaned_data.get('file')
        if not url and not body and not file:
            raise forms.ValidationError('You must specify one of "url", "body" or "file" fields')
        if (url and body) or (url and file) or (body and file):
            raise forms.ValidationError('Specify only one of "url" or "body" or "file" fields')

        start_color = cleaned_data.get('start_color')
        end_color = cleaned_data.get('end_color')
        color_steps = cleaned_data.get('color_steps')
        if start_color or end_color or color_steps:
            if not (start_color and end_color and color_steps):
                raise forms.ValidationError('To customize the color scheme, please enter all color scheme information: start color, end color, and number of steps to extrapolate in between.')

        return cleaned_data

class NewTopicForm(forms.Form):
    name = forms.CharField()

    def __init__(self, *args, **kwargs):
        num_file_sources = kwargs.pop('file_sources', None)
        num_web_sources = kwargs.pop('web_sources', None)
        print num_file_sources
        print num_web_sources
        super(NewTopicForm, self).__init__(*args, **kwargs)
        while num_file_sources:
            self.fields['file_%d' % num_file_sources] = forms.FileField()
            num_file_sources -= 1
        while num_web_sources:
            self.fields['web_%d' % num_web_sources] = forms.CharField()
            num_web_sources -= 1




