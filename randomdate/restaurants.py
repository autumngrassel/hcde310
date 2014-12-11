# -*- coding: utf-8 -*-

import argparse
import json
import pprint
import sys
import urllib
import urllib2
import random

import oauth2


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'Seattle'
SEARCH_LIMIT = 20
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'mW16xzd8plHMouLGI4n8OA'
CONSUMER_SECRET = '1KD0sE4KwsIYoEPJK2dLeuOP4nQ'
TOKEN = '9PT7uiW2IV_Uui5czYQLpvKfz4QQQVtG'
TOKEN_SECRET = 'XEvBSrVI3JtOmd7KlXm6A_eMRNM'

class Restaurant():
    def __init__(self, restdict):
        self.name = restdict['name'].encode('ascii', 'xmlcharrefreplace')
        self.address = restdict['location']['display_address']
        if restdict.has_key('display_phone'):
            self.phone = restdict['display_phone']
        else:
            self.phone = None
        self.rating = restdict['rating']
        self.rating_img = restdict['rating_img_url_small']
        self.review_excerpt = restdict['reviews'][0]['excerpt'].encode('ascii', 'xmlcharrefreplace')
        self.url = restdict['url']
        self.html = self.getHTML()

    def __str__(self):
        summary = self.name + '\n'
        summary += 'Rating: ' + str(self.rating) + '\n'
        summary += 'Address: ' + self.formatAddress()
        if self.phone:
            summary += 'Phone: ' + self.phone + '\n'
        summary += 'What people are saying: ' + self.review_excerpt + '\n'
        summary += 'More info: ' + self.url + '\n'
        summary += self.getHTML()
        return summary

    def formatAddress(self):
        address = ''
        for line in self.address:
            address += line.encode('ascii', 'xmlcharrefreplace') + '\n'
        return address

    def formatAddressHTML(self):
        address = ''
        for line in self.address:
            address += line.encode('ascii', 'xmlcharrefreplace') + ' <br />'
        return address

    def getHTML(self):
        html = '<h2 class=\'tablehead\'>' + self.name + '</h2>' 
        html += '<table>'
        html += '<tr>'
        html += '<td style=\"text-align: right\"><strong>Rating:</strong></td>'
        html += '<td>' + str(self.rating) +'</td> '
        html += '</tr>'
        if self.phone:    
            html += '<tr>'
            html += '<td style=\"text-align: right\"><strong>Reservations:</strong></td>'
            html += '<td>' + self.phone +'</td> '
            html += '</tr>'
        html += '<tr>'
        html += '<td style=\"text-align: right\"><strong>Address:</strong></td>'
        html += '<td>' + self.formatAddressHTML() +'</td> '
        html += '</tr>'
        html += '<tr>'
        html += '<td style=\"text-align: right\"><strong>What people are saying:</strong></td>'
        html += '<td>' + self.review_excerpt +'</td> '
        html += '</tr>'
        html += '<tr>'
        html += '<td style=\"text-align: right\"><strong>More info:</strong></td>'
        html += '<td> <a href=\"'+ self.url+ '\">'+ self.url +'</a></td> '
        html += '</tr>'
        html += '</table>'
        return html


def request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = 'http://{0}{1}?'.format(host, path)

    print url + urllib.urlencode(url_params)

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()
    
    print 'Querying {0} ...'.format(url)
    print signed_url

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def search(term='dinner', location='Seattle', category='tradamerican'):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'category_filter' : category,
        'radius_filter' : 6000,
        'sort' : 2
    }
    return request(API_HOST, SEARCH_PATH, url_params=url_params)

def get_business(business_id):
    """Query the Business API by a business ID.

    Args:
        business_id (str): The ID of the business to query.

    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path)

def query_api(term='dinner', location='Seattle', category='restaurants'):
    """Queries the API by the input values from the user.

    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(term, location, category)

    restaurants = response.get('businesses')

    if not restaurants:
        return

    no_restaurant = True

    while no_restaurant:
        try:
            randomnum = random.randrange(len(restaurants))
            restaurant_id = restaurants[randomnum]['id']
            response_dict = get_business(restaurant_id)
            restaurant = Restaurant(response_dict)
            no_restaurant = False
        except:
            print 'searching again'

    return restaurant
    
def getHTML(r_category):
    try:
        restaurant = query_api(category=r_category)
        return restaurant.getHTML
    except urllib2.HTTPError as error:
        sys.exit('Encountered HTTP error {0}. Abort program.'.format(error.code))

