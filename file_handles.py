import os

reading_encoding = "UTF-8"

def get_file_full_list(path):
   print("Start to parse directory : " + path)
   full_files = []
   file_numbers = 0
   for dirpath, dirnames, filenames in os.walk(path):
      for dir in filenames:
         full_files.append(os.path.join(dirpath, dir))
         file_numbers += 1
   print("End of parsing directory : " + path)
   print("Total file amounts : " + str(file_numbers))
   return full_files
   
def read_file(path):
   file_content = ""
   with open(path, 'r', encoding = reading_encoding) as file:
      file_content = file_content + file.read()
   file.close()
   return file_content
   
class file_handles_test(unittest.TestCase):
   def test_get_file_full_list(self):
      print("")

if __name__ == "__main__":
   unittest.main()


