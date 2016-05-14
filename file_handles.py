from __future__ import print_function
import os
import unittest

reading_encoding = "UTF-8"

def get_directory_full_list(path):
   print("Start to parse directories : " + path)
   full_directories = []
   for dirpath, dirnames, filenames in os.walk(path):
      for dir in dirnames:
         full_path_dir = os.path.join(dirpath, dir)
         full_directories.append(full_path_dir)

   print("--------------- end")
   print("Total directory # :", len(full_directories))
   return full_directories

def remove_not_leaf(origin_list, root):
   for dirpath, dirnames, filenames in os.walk(root):
      if (not filenames):
         try:
            origin_list.remove(dirpath)
         except ValueError:
            continue

def get_file_full_list(path):
   print("Start to parse files : " + path)
   full_files = []
   for dirpath, dirnames, filenames in os.walk(path, followlinks=True):
      for file in filenames:
         full_files.append(os.path.join(dirpath, file))
   print("--------------- end")
   print("Total file # :", len(full_files))
   return full_files

def read_file(path):
   file_content = ""
   with open(path, 'r', encoding = reading_encoding) as file:
      file_content = file_content + file.read()
   return file_content

class file_handles_test(unittest.TestCase):
   def test_get_directory_full_list(self):
      root = r"..\ruten"
      full_dir = get_directory_full_list(root)
      remove_not_leaf(full_dir, root)

if __name__ == "__main__":
   unittest.main()


