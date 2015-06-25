#!/usr/bin/env python
#
# plugin for ipinfo
#	returns information from MaxMind's GeoIPv1 databases
#	psi

import imp, os

def load(parent):
	ii_geoip = ipinfo_geoip(parent);
	ii_geoip.init();

	return ii_geoip;

class ipinfo_geoip:
	_name = "GeoIPv1";
	_author = "psi";
	_version = "1.0.0";
	_date = "2015-06-23";

	_loaded = False;
	_parent = None;

	_hasGeoIPDat = False;
	_hasGeoIPASNumDat = False;
	_hasGeoIPv6Dat = False; 
	_hasGeoLiteCityDat = False;

	def __init__(self, parent):
		self._parent = parent;

		try:
			# let's make sure we have the geoip library installed
			global GeoIP;
			import GeoIP
			self._loaded = True;

		except ImportError:
			self._loaded = False;
			if(self._parent._debug):
				self._parent.message("DEBUG", ImportError);

	def init(self):
			self.checkForDataFiles();

	def checkForDataFiles(self):

		if(os.path.isfile("/usr/share/GeoIP/GeoIP.dat")):
			self._hasGeoIPDat = True;
		if(os.path.isfile("/usr/share/GeoIP/GeoIPASNum.dat")):
			self._hasGeoIPASNumDat = True;
		if(os.path.isfile("/usr/share/GeoIP/GeoIPv6.dat")):
			self._hasGeoIPv6Dat = True;
		if(os.path.isfile("/usr/share/GeoIP/GeoLiteCity.dat")):
			self._hasGeoLiteCityDat = True;

		if(not self._hasGeoIPDat):
			self._loaded = False;
			if(self._parent._verbose):
				self._parent.message("ERROR", "Unable to find GeoIP.dat");

	def data(self):
		returnObject = {};
		tempObject = {};

		_ip = self._parent._ip.__str__();

		if(self._loaded == False):
			returnObject["GEOIP"] = {};
			return returnObject;

		if(self._parent._ipversion == 4):
			if(self._hasGeoIPDat):
				gi = GeoIP.open("/usr/share/GeoIP/GeoIP.dat", GeoIP.GEOIP_STANDARD);
				gic = GeoIP.open("/usr/share/GeoIP/GeoLiteCity.dat", GeoIP.GEOIP_STANDARD);
				gia = GeoIP.open("/usr/share/GeoIP/GeoIPASNum.dat", GeoIP.GEOIP_STANDARD);

		else:
			if(self._hasGeoIPv6Dat):
				gi = GeoIP.open("/usr/share/GeoIP/GeoIPv6.dat", GeoIP.GEOIP_STANDARD);
		
		tempObject["country_code"] = gi.country_code_by_addr(_ip);
		t = gic.record_by_addr(_ip);
		if(isinstance(t, dict)):
			tempObject.update(t);

		t = gi.range_by_ip(_ip);
		if(isinstance(t, tuple)):
			tempObject["range_start"] = t[0];
			tempObject["range_end"] = t[1];

		returnObject["GEOIP"] = tempObject;
		return returnObject;