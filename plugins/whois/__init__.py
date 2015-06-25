#!/usr/bin/env python
#
# plugin for ipinfo
#	returns information from whois
#	psi

import imp, os

def load(parent):
	ii_whois = ipinfo_whois(parent);
	ii_whois.init();
	
	return ii_whois;

class ipinfo_whois:
	_name = "Whois";
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
			global IPWhois
			from lib.ipwhois import IPWhois
			self._loaded = True;

		except ImportError, e:
			self._loaded = False;
			if(self._parent._debug):
				self._parent.message("DEBUG", e);

	def data(self):
		returnObject = {};

		if(self._loaded == False):
			returnObject["WHOIS"] = {};
			return returnObject;

		try:
			tempObject = IPWhois(self._parent._ip);
		except Exception as e:
			if(self._parent._debug):
				self._parent.message("DEBUG", e);
			returnObject["WHOIS"] = {};	
			return returnObject;

		returnObject["WHOIS"] = tempObject.lookup();

		return returnObject;