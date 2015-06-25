#!/usr/bin/env python
#
# plugin for ipinfo
#	returns information other information from Google's ipaddress object
#	psi

def load(parent):
	ii_other = ipinfo_other(parent);
	ii_other.init();
	
	return ii_other;

class ipinfo_other:
	_name = "Other";
	_author = "psi";
	_version = "1.0.0";
	_date = "2015-06-23";

	_loaded = False;
	_parent = None;

	def __init__(self, parent):
		self._parent = parent;

	def init(self):
		self._loaded = True;	

	def data(self):
		returnObject = {};
		tempObject = {};
		ipaddress = self._parent._ip;

		if(self._loaded == False):
			returnObject["OTHER"] = {};
			return returnObject;

		tempObject["binary"] = int(bin(ipaddress)[2:]);
		tempObject["hex"] = hex(ipaddress);
		tempObject["version"] = ipaddress.version;
		tempObject["local_link"] = ipaddress.is_link_local;
		tempObject["multicast"] = ipaddress.is_multicast;
		tempObject["reserved"] = ipaddress.is_reserved;
		tempObject["private"] = ipaddress.is_private;
		tempObject["loopback"] = ipaddress.is_loopback;

		returnObject["OTHER"] = tempObject;
		return returnObject