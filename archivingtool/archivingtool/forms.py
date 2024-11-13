from django import forms

class PostUrlForm(forms.Form):  
	url = forms.CharField(
		widget = forms.TextInput(attrs = {
			"class" : "user-input",
            "placeholder" : "Enter disinformation post URL here",
		}),
	)