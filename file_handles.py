import os
import unittest

reading_encoding = "UTF-8"

def get_directory_full_list(path):
   print("Start to parse directories : " + path)
   full_directories = []
   directory_numbers = 0
   for dirpath, dirnames, filenames in os.walk(path):
      for dir in dirnames:
         full_path_dir = os.path.join(dirpath, dir)
         full_directories.append(full_path_dir)
         directory_numbers += 1
   
   print("--------------- end")
   print("Total directory # : " + str(directory_numbers))
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
   file_numbers = 0
   for dirpath, dirnames, filenames in os.walk(path, followlinks=True):
      for file in filenames:
         full_files.append(os.path.join(dirpath, file))
         file_numbers += 1
   print("--------------- end")
   print("Total file # : " + str(file_numbers))
   return full_files
   
def read_file(path):
   file_content = ""
   with open(path, 'r', encoding = reading_encoding) as file:
      file_content = file_content + file.read()
   file.close()
   return file_content
   
class file_handles_test(unittest.TestCase):
   def test_get_directory_full_list(self):
      root = r"..\ruten"
      full_dir = get_directory_full_list(root)
      remove_not_leaf(full_dir, root)

if __name__ == "__main__":
   unittest.main()


