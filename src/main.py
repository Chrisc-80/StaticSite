import os, shutil
from textnode import TextNode, TextType

def copy_static(source_dir, dest_dir):

	# del public if it exist
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)
		
	# create public
	os.mkdir(dest_dir)
	
	#copy static to public
	items = os.listdir(source_dir)
	for item in items:
		item_path = os.path.join(source_dir, item)
		dest_path = os.path.join(dest_dir, item)
		if os.path.isfile(item_path):
			shutil.copy(item_path, dest_path)
			
		else:
			os.mkdir(dest_path)
			copy_static(item_path, dest_path)
		print(item_path, dest_path)

def main():
    copy_static("static", "public")
	


main()
