# Please install modules : chardet, requests, jieba, hanziconv

import unittest
import requests
import jieba
import jieba.posseg as pseg
import re
import sys
from hanziconv import HanziConv

output_encoding = sys.stdin.encoding

def ckip_postag(str):
   ckip_remote_url = "http://140.116.245.151/ckip.php"
   corpus = str
   post_data = {"text" : corpus}
   #print("Corpus encoding : " + chardet.detect(corpus))
   response = requests.post(ckip_remote_url, post_data)
   # Decoding = utf-8, python default encode is ASCII
   pos_result = response.content.decode("utf-8")
   parse_chinese_pattern = "([^\u3000^\x00-\x2F\x3A-\x7F0-9a-zA-Z]*)\((.*?)\)"
   prog = re.compile(parse_chinese_pattern)
   tag_result = prog.findall(pos_result)
   return tag_result
      
def jieba_postag(str):
   corpus = str
   corpus = chinese_convert(corpus, 0)
   words = pseg.cut(corpus)
   # Tansfer back to tradition chinese
   words = [ (chinese_convert(word, 1), tag) for word, tag in words]
   return words
   
def jieba_segment(str, cut_all_mode):
   corpus = str
   corpus = corpus.encode("utf-8", "replace").decode("utf-8")
   corpus = chinese_convert(corpus, 0)
   if cut_all_mode == True:
      seg_list = jieba.cut(corpus, cut_all=True)
      # Tansfer back to tradition chinese
      seg_list = [ chinese_convert(word, 1) for word in seg_list]
      return seg_list
   else:
      seg_list = jieba.cut(corpus, cut_all=False)
      # Tansfer back to tradition chinese
      seg_list = [ chinese_convert(word, 1) for word in seg_list]
      return seg_list

def chinese_convert(str, mode):
   uni_str = str.encode("utf-8", "replace")
   if mode == 1:
      #convert to traditional Chinese
      uni_str = HanziConv.toTraditional(uni_str)
   else:
      #convert to simple Chinese
      uni_str = HanziConv.toSimplified(uni_str)
   return uni_str

def print_chinese_str(str):
   result_content = str.encode(output_encoding, 'replace').decode(output_encoding)
   print(result_content)
   
def nf_to_wf(strs, types):
   nft = [
      "(", ")", "[", "]", "{", "}", ".", ",", ";", ":",
      "-", "?", "!", "@", "#", "$", "%", "&", "|", "\\",
      "/", "+", "=", "*", "~", "`", "'", "\"", "<", ">",
      "^", "_",
      "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
      "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
      "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
      "u", "v", "w", "x", "y", "z",
      "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
      "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
      "U", "V", "W", "X", "Y", "Z",
      " "
   ]
   
   wft = [
      "（", "）", "〔", "〕", "｛", "｝", "﹒", "，", "；", "：",
      "－", "？", "！", "＠", "＃", "＄", "％", "＆", "｜", "＼",
      "／", "＋", "＝", "＊", "～", "、", "、", "＂", "＜", "＞",
      "︿", "＿",
      "０", "１", "２", "３", "４", "５", "６", "７", "８", "９",
      "ａ", "ｂ", "ｃ", "ｄ", "ｅ", "ｆ", "ｇ", "ｈ", "ｉ", "ｊ",
      "ｋ", "ｌ", "ｍ", "ｎ", "ｏ", "ｐ", "ｑ", "ｒ", "ｓ", "ｔ",
      "ｕ", "ｖ", "ｗ", "ｘ", "ｙ", "ｚ",
      "Ａ", "Ｂ", "Ｃ", "Ｄ", "Ｅ", "Ｆ", "Ｇ", "Ｈ", "Ｉ", "Ｊ",
      "Ｋ", "Ｌ", "Ｍ", "Ｎ", "Ｏ", "Ｐ", "Ｑ", "Ｒ", "Ｓ", "Ｔ",
      "Ｕ", "Ｖ", "Ｗ", "Ｘ", "Ｙ", "Ｚ",
      "　"
   ]
   
   transfer_list = []
   
   for i in range(0, len(nft)-1):
      transfer_list.append([nft[i], wft[i]])
      
   if types == 1: # to full type
      for search, replace in transfer_list:
         strs = strs.replace(search, replace)
   else: # to half type
      for replace, search in transfer_list:
         strs = strs.replace(search, replace)
   
   return strs

class nlp_module_test(unittest.TestCase):
   def test_ckip_postag(self):
      result_list = ckip_postag("今天天氣真好")
      for term, pos in result_list:
         print(term + "(" + pos + ")")

if __name__ == "__main__":
   unittest.main()