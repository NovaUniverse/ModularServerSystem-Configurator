from pathlib import Path

import os
import json
import ruamel.yaml
import pprint
import sys

def reqursive_replacer(data, key, new_value):
	key_parts = key.split(".")
	#print("reqursive_replacer " + str(data) + " " + key + " " + str(new_value) + " lkp: " + str(len(key_parts)))

	if len(key_parts) == 1:
		data[key] = new_value
	else:
		key_to_use = key_parts[0]
		key_parts.pop(0)
		reqursive_replacer(data[key_to_use], ".".join(key_parts), new_value)

with open("msscfg.json") as mssconfig_file:
	mssconfig = json.load(mssconfig_file)
	plugin_config_file_path = mssconfig["data_folder"] + "/plugin_config.json"
	with open(plugin_config_file_path) as plugin_config_file:
		plugin_config = json.load(plugin_config_file)
		for plugin in plugin_config:
			plugin_data_folder = "./plugins/" + plugin
			print("Checking if " + plugin_data_folder + " exits")
			if not os.path.isdir(plugin_data_folder):
				print("Plugin data folder for " + plugin + " was not found")
				continue
			
			print("[INFO] Updating config for plugin: " + plugin)
			for config_file in plugin_config[plugin]:
				config_file_path = plugin_data_folder + "/" + config_file

				# Check if config file exits
				if not os.path.isfile(config_file_path):
					print("[ERR] Cant find " + config_file + " in plugin " + plugin)
					continue

				print("[INFO] Updating " + config_file + " in plugin " + plugin)
				yaml = ruamel.yaml.YAML()
				yaml.preserve_quotes = True

				# Read the config file
				with open(config_file_path) as cf:
					#print(cf)
					data = yaml.load(cf)
					keys = plugin_config[plugin][config_file]
					for key in keys:
						value = plugin_config[plugin][config_file][key]
						#print("Set " + key + " to " + str(value))
						reqursive_replacer(data, key, value)
					
					print("[INFO] Writing config to file")
					outf = Path(config_file_path)
					yaml.dump(data, outf)
