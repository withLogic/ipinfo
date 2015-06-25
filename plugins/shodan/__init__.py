#!/usr/bin/env python
#
# plugin for ipinfo
#	returns information from Shodan's databases
#	psi

def load(parent):
	ii_shodan = ipinfo_shodan(parent);
	ii_shodan.init();
	
	return ii_shodan;

class ipinfo_shodan:
	_name = "Shodan";
	_author = "psi";
	_version = "1.0.0";
	_date = "2015-06-23";

	_loaded = False;
	_parent = None;

	def __init__(self, parent):
		self._parent = parent;

	def init():

	def data():