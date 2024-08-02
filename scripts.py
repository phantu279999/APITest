import os
import glob


def get_same_file_in_two_folder(path_folder_One="", path_folder_Two=""):
	"""
	get same files in two folders
	:param path_folder_One:
	:param path_folder_Two:
	:return: list
	"""
	same_files = []
	pattern = os.path.join(path_folder_One, '**', '*')
	pattern2 = os.path.join(path_folder_Two, '**', '*')
	all_files = []
	for f in glob.glob(pattern, recursive=True):
		if os.path.isfile(f):
			name_file = f.split("\\")[-1]
			all_files.append(name_file)

	for f in glob.glob(pattern2, recursive=True):
		if os.path.isfile(f):
			name_file = f.split("\\")[-1]
			if name_file in all_files:
				same_files.append(name_file)

	return same_files


if __name__ == '__main__':
	list_same = get_same_file_in_two_folder(
		path_folder_One=r"G:\Py\APITest",
		path_folder_Two=r"G:\Vccorp\tinycd\api"
	)
	print(list_same)
