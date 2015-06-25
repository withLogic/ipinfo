#!/usr/bin/env python
#
# Get all of the information based on the ip address
# psi 
#

import sys, os, inspect, json, collections, imp, pprint
from optparse import OptionParser
 
from lib.ipaddr import *

class ipinfo:
	""" Define variables needed
	"""
	_savefile = None;
	_debug = False;
	_verbose = False;
	_silent = False;
	_ip = None;
	_ipversion = None;

	_output = {};
	_outputJson = False;

	_pluginsfolder = "./plugins";
	_mainmodule = "__init__";
	_pluginsList = [];

	def main(self, args):
		""" Parse the arguments fed to us by the User
		"""
		parser = OptionParser();
		parser.disable_interspersed_args();
		parser.add_option("-d", "--debug", dest="o_debug", action="store_true", help="Enables debug output");
		parser.add_option("-v", "--verbose", dest="o_verbose", action="store_true", help="Enables verbose output");
		parser.add_option("-o", "--output", dest="o_outfile", help="Output the data to a file");
		parser.add_option("-j", "--json", dest="o_json", action="store_true", help="Ouptut the data as JSON");
		parser.add_option("-s", "--silent", dest="o_silent", action="store_true", help="Supress the terminal output");

		(options, args) = parser.parse_args();

		self._debug = options.o_debug;
		self._verbose = options.o_verbose;
		self._outputJson = options.o_json;
		self._savefile = options.o_outfile;
		self._silent = options.o_silent;

		""" Perform some basic error checking on the data provided
		"""
		if(len(args) < 1):
			if(self._verbose):
				self.message("ERROR", "No IP address specified.");
			return -1;

		try:
			self._ip = IPAddress(args[0]);
			if(isinstance(self._ip, IPv4Address)):
				self._ipversion = 4;
			else:
				self._ipversion = 6;

		except ValueError, e:
				if(self._verbose):
					self.message("ERROR", e);
				return -1;

		""" Load our plugins from the plugins directory
		"""
		for i in self.getPlugins():
			plugin = self.loadPlugin(i);
			self._pluginsList.append( plugin.load(self) );

		""" Update our output dictionary with information from the plugins
		"""
		for plugin in self._pluginsList:
			self._output.update( plugin.data() );

		""" Sort and display the data
		"""
		self._output = self.convertDictToOrderedDict(self._output);

	def message(self, type, text):
		""" Take a message and type and display it on the screen. 
				Message types will be color coded if on a *nix system.
		"""
		text = str(text);
		debug = "";

		if(len(text) <= 0):
			return 0;

		typeText = {"INFO" : "[*]","ERROR" : "[!]", "DEBUG" : "[~]"};
		typeColors = {"INFO" : "\033[94m", "ERROR" : "\033[91m", "DEBUG": "\033[.43m", "END" : "\033[0m"};

		if(type == "DEBUG"):
			debug = "(" + os.path.basename(inspect.getfile(inspect.currentframe().f_back)) + " ln. " + str(inspect.currentframe().f_back.f_lineno) + ")";

		if(os.name != "nt"):
			print typeColors[type] + typeText[type] + " " + text + " " + debug + typeColors["END"];
		else:
			print typeText[type] + " " + text;

	_xxx = "";

	def dumpclean(self, obj, level=0):
		""" Take a nested dict or list and present it in a much more readable format
		"""

		if (type(obj) == dict) or (type(obj) == collections.OrderedDict):
			for k, v in obj.items():
				if hasattr(v, '__iter__'):
					self._xxx += k + "\n";
					self.dumpclean(v, level+1);
				else:
					self._xxx += '%s %s : %s \n' % ((" " * (level * 4)),k, v)
		elif type(obj) == list:
			for v in obj:
				if hasattr(v, '__iter__'):
					self.dumpclean(v);
				else:
					self._xxx += (" " * (level * 4)) & v & "\n";
		else:
			self._xxx += (" " * (level * 4)) & obj & "\n";

	def convertDictToOrderedDict(self, source):
		""" Take a standard dict and convert it to a sorted OrderedDict
		"""
		returnOD = collections.OrderedDict();

		if(type(source) != dict):
			return returnOD;

		if (type(source) == dict) or (type(source) == collections.OrderedDict):
			for k,v in source.items():
				if hasattr(v, '__iter__'):
					returnOD[k] = self.convertDictToOrderedDict(v);

		returnOD = collections.OrderedDict(sorted(source.items(), key=lambda t: t[0].lower()));

		return returnOD;

	def getPlugins(self):
		""" Plugin loading, returns a list of plugins
		"""
		plugins = [];
		possibleplugins = os.listdir(self._pluginsfolder);
		for i in possibleplugins:
			location = os.path.join(self._pluginsfolder, i);
			if not os.path.isdir(location) or not self._mainmodule + ".py" in os.listdir(location):
				continue
			info = imp.find_module(self._mainmodule, [location]);
			plugins.append({"name": i, "info": info});
		return plugins;

	def loadPlugin(self, plugin):
		""" Loads the selected plugin
		"""
		if(self._debug):
			self.message("DEBUG", plugin);
		return imp.load_module(self._mainmodule, *plugin["info"])


if __name__ == "__main__":
	try:
		ii = ipinfo();
		ii.main(sys.argv);

		if(ii._outputJson):
			 ii._xxx = json.dumps(ii._output);
		else:
			ii.dumpclean(ii._output);

		if(not(ii._silent)):
			print ii._xxx;

		if(ii._savefile != None):
			outfile = open(ii._savefile, "w");
			outfile.write(ii._xxx + "\n");
			outfile.close();

	except KeyboardInterrupt:
		sys.stdout.flush(); 
		self.message("ERROR", "User quit."); 






