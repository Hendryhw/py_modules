# Testing Environment: Python 2.6, 2.7, 3.4, and 3.5.
# ckip_postag requires requests module.
# jieba_postag and jieba_segment require jieba module and optionally hanziconv.
from __future__ import print_function
import re
import unicodedata

try: # Python 2.
    unicode # NameError is raised because Python 3 does not have this class.
    str_bytes_type = str
except NameError: # Python 3.
    str_bytes_type = bytes

def ckip_postag(str, encoding_list=("UTF8", "BIG5"), form=""):
    import requests
    str, encoding = try_decode(str, encoding_list)
    ckip_remote_url = "http://140.116.245.151/ckip.php"
    post_data = {"text": str}
    response = requests.post(ckip_remote_url, post_data)
    pos_result = response.content.decode("UTF8")
    tag_result = re.findall(u"([^\u3000]+)\((.*?)\)", pos_result)
    return process_result(tag_result, encoding, form)

def jieba_postag(str, encoding_list=("UTF8", "BIG5"), form=""):
    import jieba.posseg as pseg
    str, encoding = try_decode(str, encoding_list)
    # if type(str) is bytes: str = str.decode("UTF-8")
    # Convert into simplified Chinese.
    str = chinese_convert(str, 0)
    words = pseg.cut(str)
    # Convert back to traditional Chinese.
    words = [(chinese_convert(word, 1), tag) for word, tag in words]
    return process_result(words, encoding, form)

def jieba_segment(str, cut_all_mode, encoding_list=("UTF8", "BIG5"), form=""):
    import jieba
    str, encoding = try_decode(str, encoding_list)
    str = chinese_convert(str, 0)
    seg_list = jieba.cut(str, cut_all=cut_all_mode)
    seg_list = [chinese_convert(word, 1) for word in seg_list]
    return process_result(seg_list, encoding, form)

def chinese_convert(str, mode):
    try:
        from hanziconv import HanziConv
        return (HanziConv.toSimplified, HanziConv.toTraditional)[mode](str)
    except (ImportError, ValueError): pass
    return str

def process_result(result, encoding, form):
    if encoding != "" or form != "":
        if hasattr(result[0], "encode"):
            apply = lambda r, f: [f(item) for item in r]
        else:
            apply = lambda r, f: [(f(term), tag) for term, tag in r]
        if form != "": result = apply(result, lambda t: unicodedata.normalize(form, t))
        if encoding != "": result = apply(result, lambda t: t.encode(encoding))
    return result

def try_decode(str, encoding_list):
    encoding = ""
    if type(str) is str_bytes_type:
        for e in encoding_list:
            try: str = str.decode(e)
            except UnicodeDecodeError: continue
            encoding = e
            break
        if encoding == "": raise UnicodeDecodeError("All codecs failed to decode input.")
    return (str.encode("UTF8"), encoding)

if __name__ == "__main__":
    import sys
    data = u"WMMKS \u5be6\u9a57\u5ba4\uff0c\u81ea\u7136\u8a9e\u8a00\u8655\u7406\u6a21\u7d44\u3002"
    if not type(data) is str: data = data.encode("BIG5")
    ckip_tag_result = ckip_postag(data)
    jieba_tag_result = jieba_postag(data)
    jieba_segment_result = jieba_segment(data, False)
    print("Input:", data)
    print("CKIP POS Result:")
    for term, tag in ckip_tag_result:
        print("Term:", term, "Tag:", tag)
    print("Jieba POS Result:")
    for term, tag in jieba_tag_result:
        print("Term:", term, "Tag:", tag)
    print("Jieba Segment Result:")
    print(" ".join(jieba_segment_result))
