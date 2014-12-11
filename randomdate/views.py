from django.shortcuts import render

from django.http import HttpResponse
from randomdate.forms import DateForm
from randomdate.restaurants import getHTML
from randomdate.events import eventHTML

def find_date(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = DateForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.

            # Now call the index() view.
            # The user will be shown the homepage.
            return view_results(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = DateForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'randomdate/finddate.html', {'form': form})

def view_results(request, context_dict={}):	
	if not request.POST['category'] or  request.POST['category'] == 'any':
		context_dict['category'] = None
	else:
		context_dict['category'] = request.POST['category']
	if not request.POST['date']:
		context_dict['date'] = None
	else:
		context_dict['date'] = request.POST['date']

	context_dict['restaurantHTML'] = getHTML(request.POST['cuisine'])
	if not context_dict['category'] and not context_dict['date']:
		context_dict['eventHTML'] = eventHTML()
	elif not context_dict['category']:
		context_dict['eventHTML'] = eventHTML(date=context_dict['date'])
	elif not context_dict['date']:
		context_dict['eventHTML'] = eventHTML(category=context_dict['category'])
	else:
		context_dict['eventHTML'] = eventHTML(context_dict['date'], context_dict['category'])
	return render(request, 'randomdate/viewresults.html', context_dict)

def index(request, context_dict={}):
	return render(request, 'randomdate/index.html', context_dict)
