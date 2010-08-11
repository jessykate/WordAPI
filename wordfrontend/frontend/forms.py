from django import forms

# default is required = True
class TagCloudForm(forms.Form):
    help_text = {
        'body' : 'This is the minimum required field.',
        'strip' : 'Strip any html markup. Default is True.',
        'max_size' : 'Maximum word size in px. Default is 70px.',
        'min_size' : 'Minimum word size in px. Default is 10px.',
        'width' : 'Width of the div containing the tag cloud in px. Default is 400px',
        'height' : 'Height of the div containing the tag cloud in px. Default is None, to allow the height to accomodate as many words as needed.',
        'tokenizer' : 'You may specify a custom tokenizer if you like, by passing in a <a href="http://docs.python.org/library/re.html">python regular expression</a>',
        'max_words' : 'Maximum number of words to be included in the tag cloud (will always truncate least frequent words)',
        'normalize' : "this option will normalize the case of all words, making 'Hello' and 'hello' equivalent",
        'stopwords' : "Whether or not to remove (exclude) common english words (so-called 'stop words' from the tag cloud, such as 'the' and 'it'. Default is True.",
        'sort_order' : 'What order should the words be sorted in? Options are frequency, random, or alphabetical. In practice random seems to look best most of the time, but try different ones and see what you like.'
    }

    allowed_sort_orders = [('random', 'random'), ('frequency', 'frequency'),
                           ('alphabetical', 'alphabetical (not implemented)')]

    body = forms.CharField(widget=forms.Textarea(attrs={'rows':'20', 'cols':60 }), help_text = help_text['body'])
    strip = forms.BooleanField(initial=True, help_text = help_text['strip'], required=False)
    normalize = forms.BooleanField(initial=True, help_text = help_text['normalize'], required=False)
    remove_stopwords = forms.BooleanField(initial=True, help_text = help_text['stopwords'], 
                        required=False)
    sort_order = forms.ChoiceField(help_text= help_text['sort_order'], required=False, choices = allowed_sort_orders) 
    max_words =  forms.IntegerField(help_text = help_text['max_words'], required=False)
    max_size = forms.IntegerField(help_text = help_text['max_size'], required=False)
    min_size = forms.IntegerField(help_text = help_text['min_size'], required=False)
    width = forms.IntegerField(help_text = help_text['width'], required=False)
    height = forms.IntegerField(help_text = help_text['height'], required=False)
    tokenizer = forms.CharField(help_text = help_text['tokenizer'], required=False)

