import os
import sys

def file_validation(url, jhove_path):
	os.chdir(jhove_path)

	# Check if operating system is posix or windows
	if os.name == "posix":
		jhove_command = "./jhove"
	else:
		jhove_command = "jhove.bat"
		url = url.replace("/", "\\")

	# Runs the file validation and saves the output to a variable
	if url.lower().endswith('.jpg'):
		stream = os.popen(jhove_command + " -m JPEG-hul -kr " + "\"" + url + "\"")
	elif url.lower().endswith('.tiff'):
		stream = os.popen(jhove_command + " -m TIFF-hul -kr " + "\"" + url + "\"")
	output = stream.read()

	# Prints a response
	if "Status: Well-Formed and valid" not in output:
		print("File validation failed")
	else:
		print("File validation successful\n")

	return output