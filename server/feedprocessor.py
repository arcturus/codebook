#!/usr/bin/python

import feedparser
import datetime
import iso8601
import urllib
import time

HOST = 'http://gentle-stream-2067.herokuapp.com/'
ACCESS_TOKEN = 'AAAC0ujN1UXEBAHvePMPjOreCk7GyvfZCsKoW51Hp5OD5bn6nYb8AdZABwhmWpnLkxw87t25JjXXrLNMh4WN10bAeD9ZCl6PWdm4B5jVhQZDZD'
latest_access = None

#Get a list of users ... yes, this could be huge, but we are just hacking ;)
users = ['arcturus']

def get_user_commits(user):
	global latest_access
	user_feed = feedparser.parse('https://github.com/' + user + '.atom')
	print 'Got ' + user_feed.feed.title
	latest = None
	for element in user_feed.entries:
		date = iso8601.parse_date(str(element.published))
		title = str(element.title)
		if title.find('pushed') != -1 and is_date_bigger_than(date, latest_access) :
			#Is this the latest interaction?
			project = title[title.index('/') + 1:]
			commit = str(element.links[0].href)[str(element.links[0].href).index('...') + 3:]		
			url = HOST + 'projects/' + user + '/' + project + '/' + commit
			print 'Got to notify for url: ' + url
			params = {}
			params['access_token'] = ACCESS_TOKEN
			params['project'] = url
			params = urllib.urlencode(params)
			f = urllib.urlopen("https://graph.facebook.com/me/_codebook:Commit", params)
			if latest_access == None:
				latest = date
			elif is_date_bigger_than(date, latest_access):
				latest = date
			#print 'New push!: \n' + str(element)
			
	if latest != None:
		print 'Latest interaction was: ' + str(latest)
		latest_access = latest
			
def is_date_bigger_than(date1, date2):
	"""
		Given two dates, just say if one is bigger than the other one.
	"""
	if date2 is None:
		date2 = datetime.datetime.now()
	dt1 = date1.replace(tzinfo=None)
	dt2 = date2.replace(tzinfo=None)
	if dt1 - dt2 > datetime.timedelta(seconds = 0):
		return True
	return False
	
def main():
	while True:
		for user in users:
			get_user_commits(user)
			#get_user_commits(user, datetime.datetime(2011, 12, 30, 20, 43, 20))
		time.sleep(15)
	
if __name__ == '__main__':
	main()	