#!/usr/bin/env python
#
# plugin for ipinfo
#	returns information from robtex service
#	psi

import dns.resolver, ast

def load(parent):
	ii_torcheck = ipinfo_torcheck(parent);
	ii_torcheck.init();
	
	return ii_torcheck;

class ipinfo_torcheck:
	_name = "TorCheck";
	_author = "psi";
	_version = "1.0.0";
	_date = "2015-06-23";

	_loaded = False;
	_parent = None;

	_torFlags = {"E" : "Exit", "X" : "Hidden Exit", "A" : "Authority", "B" : "BadExit", "D" : "V2Dir", "F" : "Fast", "G" : "Guard", "H" : "HSDir", "N" : "Named", "R" : "Running", "S" : "Stable", "U" : "Unnamed", "V" : "Valid"};

	def __init__(self, parent):
		self._parent = parent;

	def init(self):
		self._loaded = True;

	def decipherTorCode(self, torcode):
		returnObject = {};

		""" break the string into its parts
		"""
		returnObject["node_name"] = torcode[(torcode.index("N:") + 2):(torcode.index("/P:"))];
		returnObject["ports"] = torcode[(torcode.index("/P:") + 3):(torcode.index("/F:"))];
		returnObject["flags_raw"] = torcode[(torcode.index("/F:") + 3):];

		""" decode the flags
		"""
		flags_decoded = [];
		for letter in returnObject["flags_raw"]:
			flags_decoded.append( self._torFlags[letter] );
		returnObject["flags_decoded"] = ", ".join(flags_decoded);

		return returnObject;


	def data(self):
		returnObject = {};
		tempObject = {};
		ipaddress = self._parent._ip.__str__();

		baseurl = ".tor.dan.me.uk";

		if(self._loaded == False):
			returnObject["TORCHECK"] = {};
			return returnObject;

		""" get the inverse of the ipaddress
		"""
		ipurl = '.'.join(reversed(ipaddress.split(".")));
		completeurl = ipurl + baseurl;

		try:
			aanswer = dns.resolver.query(completeurl, 'A');
			if(aanswer[0].to_text() == "127.0.0.100"):
				txtanswer = dns.resolver.query(completeurl, 'TXT');
				for data in txtanswer:
					for txt in data.strings:
						txt_string = txt;

			tempObject["status"] = "In the TOR network";
			tempObject["txt"] = txt_string;
			tempObject.update( self.decipherTorCode(txt_string) );

		except Exception, e:
			tempObject["status"] = "Not in the TOR network";

			if(self._parent._debug):
				self._parent.message("DEBUG", e);

		returnObject["TORCHECK"] = tempObject;
		return returnObject;