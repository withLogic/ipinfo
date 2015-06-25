#!/usr/bin/env python
#
# plugin for ipinfo
#	returns information from robtex service
#	psi

def load(parent):
	ii_robtex = ipinfo_robtex(parent);
	ii_robtex.init();
	
	return ii_robtex;

class ipinfo_robtex:
	_name = "Robtex";
	_author = "psi";
	_version = "1.0.0";
	_date = "2015-06-23";

	_loaded = False;
	_parent = None;

	def __init__(self, parent):
		self._parent = parent;

	def init(self):
		try:
			# let's make sure we have the whois library loaded
			global mechanize
			global BeautifulSoup
			global re

			import mechanize
			from bs4 import BeautifulSoup;
			import re

			self._loaded = True;

		except ImportError, e:
			self._loaded = False;
			if(self._parent._debug):
				self._parent.message("DEBUG", e);

	def data(self):
		returnObject = {};
		tempObject = {};
		ipaddress = self._parent._ip.__str__();


		if(self._loaded == False):
			returnObject["ROBTEX"] = {};
			return returnObject;

		"""
		Construct the URL
		"""
		baseURL = "https://www.robtex.com/en/advisory/ip/";
		ipaddressURL = ipaddress.replace(".","/");
		completeURL = baseURL + ipaddressURL;

		"""
		Open the webpage
		"""
		br = mechanize.Browser();
		try:
			html = br.open(completeURL);
			soup = BeautifulSoup(html);
		except:
			returnObject["ROBTEX"] = {};
			return returnObject;	

		try:
			pointingTo = soup.find(id="x_shared");
			pointingToList =  [];
			for li in pointingTo.findAll("li"):
				aText = li.find('a').contents[0];
				pointingToList.append(aText);
			tempObject["domains"] = ','.join(list(set(pointingToList)));

			otherIPs = soup.find(id="x_summary");
			otherIPsList =  [];
			for li in otherIPs.findAll("li"):
				t = li.find('a')
				if t != None:
					aText = t.contents[0];
					otherIPsList.append(aText);

			tempObject["other_domains"] = ','.join(list(set(otherIPsList)));

		except Exception, e:
			if(self._parent._debug):
				self._parent.message("DEBUG", e);
			pass

		returnObject["ROBTEX"] = tempObject;
		return returnObject;
