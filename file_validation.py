import os
import sys
from dotenv import load_dotenv



def file_validation(url, jhovePath):
	os.chdir(jhovePath)

	# Check if operating system is posix or windows
	if os.name == "posix":
		jhoveOSvariable = "./jhove"
	else:
		jhoveOSvariable = "jhove.bat"
		url = url.replace("/", "\\")

	# Runs the file validation and saves the output to a variable
	if url.lower().endswith('.jpg'):
		stream = os.popen(jhoveOSvariable + " -m JPEG-hul -kr " + "\"" + url + "\"")
	elif url.lower().endswith('.tiff'):
		stream = os.popen(jhoveOSvariable + " -m TIFF-hul -kr " + "\"" + url + "\"")
	output = stream.read()

	# Prints a response
	if "Status: Well-Formed and valid" not in output:
		print("File validation failed")
		print(output)
	else:
		print("File validation successful\n")
		print(output)

url1 = "C:/Users/Ukhur/Documents/Skole/6.Semester/Bachelor/Test bilder/DSC06766.jpg"
#url2 = "C:\Users\Ukhur\Documents\Skole\6. Semester\Bachelor\Test bilder\GoldenThread\Golden_Thread_Test_2021_04_07 1.jpg"

load_dotenv()
jhovePath = os.getenv('JHOVE_PATH')
file_validation(url1, jhovePath)