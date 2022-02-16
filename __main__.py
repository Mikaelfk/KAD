import os
from kvalitetssikring_av_digitisering import jhove_validation
from dotenv import load_dotenv

def main():
	load_dotenv()
	jhove_path = os.getenv('JHOVE_PATH')
	url = "path/to/file"
	output = jhove_validation(url, jhove_path)
	print(output)

if __name__ == "__main__":
	main()
