from django import forms
# from randomdate.models import Page, Category

CHOICES = (
	('any', 'Any'),
	('music', 'Music & Concerts'),
	('comedy', 'Comedy'),
	('learning_education', 'Education'),
	('family_fun_kids', 'Kids & Family'),
	('festivals_parades', 'Festivals'),
	('movies_film', 'Movies & Film'),
	('food', 'Food'),
	('art', 'Art'),
	('holiday', 'Holiday'),
	('books', 'Books & Literary'),
	('attractions', 'Museums & Attractions'),
	('outdoors_recreation', 'Outdoors & Recreation'),
	('performing_arts', 'Performing Arts'),
	('politics_activism', 'Politics & Activism'),
	('religion_spirituality', 'Religion & Spirituality'),
	('science', 'Science'),
	('sports', 'Sports'),
	('technology', 'Technology'),
)
 
CUISINE = (
	('restaurants', 'Any'),
	('pizza', 'Pizza'),
	('mexican', 'Mexican'),
	('tradamerican', 'American (Traditional)'),
	('japanese', 'Japanese'),
	('newamerican', 'American (New)'),
	('chinese', 'Chinese'),
	('burgers', 'Burgers'),
	('italian', 'Italian'),
	('seafood', 'Seafood'),
	('french', 'French'),
	('vietnamese', 'Vietnamese'),
	('vegetarian', 'Vegetarian'),
	('thai', 'Thai'),
	('mediterranean', 'Mediterranean'),
	('indpak', 'Indian'),
	('aisianfusion', 'Asian Fusion'),
	('korean', 'Korean'),
)
 


class DateForm(forms.Form):
    date = forms.CharField(widget=forms.TextInput(attrs={'class': 'auto-kal', 'type':'text', 'placeholder': 'MM/DD/YYYY','data-kal': 'direction: \'today-future\'', 'id': 'date', 'name':'date'}))
    category = forms.ChoiceField(choices=CHOICES)
    cuisine = forms.ChoiceField(choices=CUISINE)
    

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        # model = Page
       	fields = ('date', 'category', 'cuisine')


