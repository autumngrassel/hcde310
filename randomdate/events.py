# -*- coding: utf-8 -*-


import md5
import urllib
import random
import httplib2
import simplejson
import HTMLParser
import time
import cgi

TODAY = time.strftime('%m/%d/%Y')

h = HTMLParser.HTMLParser()


__all__ = ['APIError', 'API']

APP_KEY = 'pgvX3ZB2ndKgWWQz'

def pretty(obj):
    return simplejson.dumps(obj, sort_keys=True, indent=2)

def plainText(text):
    return removeTags(h.unescape(text).encode('utf-8'))

def formatDate(date):
    date = date.split('/')
    month = date[0]
    day = date[1]
    year = date[2]
    format_date = year + month + day + '00'
    return format_date


def removeTags(text):
    result = ''
    in_tag = False
    for character in text:
        if character == '\u2019':
            result += '\''
        elif (in_tag == False) & (character == '<'):
            in_tag = True
        elif (in_tag) & (character == '>'):
            in_tag = False
            result += '\n'
        elif not in_tag:
            result += character
    return result

class Event:
    def __init__(self, eventdict):
        self.title = eventdict['title'].encode('ascii', 'xmlcharrefreplace')
        self.time = self.convertDate(eventdict['start_time'].encode('ascii', 'xmlcharrefreplace'))
        self.venue = eventdict['venue_name'].encode('ascii', 'xmlcharrefreplace')
        self.address = self.buildAddress(eventdict)
        self.description = eventdict['description']
        if self.description:
            self.description = self.description.encode('ascii', 'xmlcharrefreplace')
        self.url = eventdict['url']
        self.html = self.getHTML()

    def __str__(self):
        result = '-----' + self.title + '-----\n'
        if self.time:
            result += 'Date & Time: ' + self.time + '\n'
        if self.venue:
            result += 'Venue: ' + self.venue + '\n'
        if self.address:
            result += 'Location: ' + self.address + '\n'
        if self.description:
                result += 'Description:' + plainText(self.shortDescritpion()) + '\n'
        return result


    def buildAddress(self, eventdict):
        address = ''
        if eventdict['venue_address']:
            address += eventdict['venue_address'].encode('ascii', 'xmlcharrefreplace') + '\n' 
        if eventdict['city_name'] and (eventdict['region_abbr'] or eventdict['postal_code']) :
            address += eventdict['city_name'].encode('ascii', 'xmlcharrefreplace') + ', '
        elif eventdict['city_name']:
            address += eventdict['city_name'].encode('ascii', 'xmlcharrefreplace')
        if eventdict['region_abbr']:
            address += eventdict['region_abbr'].encode('ascii', 'xmlcharrefreplace') + ' '
        if eventdict['postal_code']: 
            address += eventdict['postal_code'].encode('ascii', 'xmlcharrefreplace')
        return address;

    def convertDate(self, date):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        month = months[int(date[5:7])-1]
        day = str(int(date[8:10]))
        year = date[0:4]
        hour = int(date[11:13])
        minutes = date[14:16]
        if hour == 0:
            time = '12:' + minutes + 'am' 
        elif hour == 12:
            time = "12:" + minutes + 'pm'
        elif hour > 12:
            time = str(hour - 12) + ':' + minutes +'pm'
        else:
            time = str(hour) + ':' + minutes + 'am'
        
        return month + ' ' + day + ', ' + year + ' at ' + time
        
    def shortDescritpion(self):
        if len(self.description) > 400:
            return self.description[:400] + '...'
        else:
            return self.description

    def getHTML(self):
        html = '<h2 class=\'tablehead\'>' + self.title + '</h2>' 
        html += '<table>'
        if self.time: 
            html += '<tr>'
            html += '<td style=\"text-align: right\"><strong>Date & Time:</strong></td>'
            html += '<td>' + self.time +'</td> '
            html += '</tr>'
        if self.venue:
            html += '<tr>'
            html += '<td style=\"text-align: right\"><strong>Venue:</strong></td>'
            html += '<td>' + self.venue +'</td> '
            html += '</tr>'
        if self.address:
            html += '<tr>'
            html += '<td style=\"text-align: right\"><strong>Address:</strong></td>'
            html += '<td>' + self.address.replace('\n', '<br />') +'</td> '
            html += '</tr>'
        if self.description and not self.description.isspace(): 
            html += '<tr>'
            html += '<td style=\"text-align: right\"><strong>Description:</strong></td>'
            html += '<td>' + self.shortDescritpion() +'</td> '
            html += '</tr>'
        if self.url:
            html += '<tr>'
            html += '<td style=\"text-align: right\"><strong>More info:</strong></td>'
            html += '<td> <a href=\"'+ self.url+ '\">'+ self.url +'</a></td> '
            html += '</tr>'
        html += '</table>'
        return html



class APIError(Exception):
    pass

class API:
    def __init__(self, app_key, server='api.eventful.com', cache=None):
        """Create a new Eventful API client instance.
If you don't have an application key, you can request one:
    http://api.eventful.com/keys/"""
        self.app_key = app_key
        self.server = server
        self.http = httplib2.Http(cache)

    def call(self, method='events/search', args={}):
        "Call the Eventful API's METHOD with ARGS."
        # Build up the request
        args['app_key'] = self.app_key
        if hasattr(self, 'user_key'):
            args['user'] = self.user
            args['user_key'] = self.user_key
        args = urllib.urlencode(args)
        url = "http://%s/json/%s?%s" % (self.server, method, args)

        # Make the request
        response, content = self.http.request(url, "GET")

        # Handle the response
        status = int(response['status'])
        if status == 200:
            try:
                return simplejson.loads(content)
            except ValueError:
                raise APIError("Unable to parse API response!")
        elif status == 404:
            raise APIError("Method not found: %s" % method)
        else:
            raise APIError("Non-200 HTTP response status: %s" % response['status'])


def make_request(date=TODAY, category=None):
    date_param = formatDate(date)
    date_param = date_param + '-' + date_param
    print date_param
    request_obj = API(APP_KEY)
    if category:
        params = {'location': 'Seattle', 
                    'date': date_param, 
                    'category': category, 
                    'within': '10', 
                    'units': 'miles'}
    else: 
        params = {'location': 'Seattle', 
                    'date': date_param, 
                    'within': '10', 
                    'units': 'miles'}
    request = request_obj.call('events/search', params)
    events = request['events']['event']
    event = events[random.randrange(len(events))]
    print date[6:10] + '-' + date[0:2]+'-' + date[3:5] + "    " + event['start_time']
    while not date[6:10] + '-' + date[0:2]+'-' + date[3:5] in event['start_time']:
        event = events[random.randrange(len(events))]
    event_obj = Event(event)
    return event_obj

def eventHTML(date=TODAY, category=None):
    return make_request(date, category).html.encode('ascii', 'xmlcharrefreplace')


