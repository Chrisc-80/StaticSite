import os
import shutil

from gencontent import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def copy_files_recursive(dir_path_static, dir_path_public):

	if not os.path.exists(dir_path_public):
		# create public
		os.mkdir(dir_path_public)

	#copy static to public
	items = os.listdir(dir_path_static)
	for item in items:
		item_path = os.path.join(dir_path_static, item)
		dest_path = os.path.join(dir_path_public, item)
		if os.path.isfile(item_path):
			shutil.copy(item_path, dest_path)
			
		else:
			os.mkdir(dest_path)
			copy_files_recursive(item_path, dest_path)

def main():

	# del public if it exist
	print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
	
	print("Copying static files to public directory...")
	copy_files_recursive(dir_path_static, dir_path_public)

	print("Generating page...")
	generate_page(
		os.path.join(dir_path_content, "index.md"),
		template_path,
		os.path.join(dir_path_public, "index.html"),
	)


main()
