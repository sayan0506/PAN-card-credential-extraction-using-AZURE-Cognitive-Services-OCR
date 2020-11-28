from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import re
from array import array
import os
from PIL import Image
import sys
import time
# finds whether an input is similar to asequence of elements
import difflib
# for checking date & time format
from dateutil.parser import parse

key = '321697159941436a8f3692497ed14ee5'
endpoint = 'https://temi0506.cognitiveservices.azure.com/'

# detects the pan id in the extracted text by OCR
def find_id(textlist, wordstring):
    lineno = -9999
    for wordline in textlist:
        xx = wordline.split()
        print(xx)
        if ([w for w in xx if re.search(wordstring.upper(), w) or re.search(wordstring.lower(), w)]):
            lineno = textlist.index(wordline)
            print(lineno)
            textlist = textlist[lineno+1:]
            return lineno, textlist
    return lineno, textlist

# checks whether the string is a date or not
def is_date(string, fuzzy = False):
    try:
        parse(string, fuzzy = fuzzy)
        return True
    except ValueError:
        return False
    
# Images uploaded are stored in the /Images folder
def extract_text(filename):
    path = os.path.join('Image', filename)
    # loading the image with PIL library
    im = Image.open(path)
    # resizing the image
    length_x, width_y = im.size
    factor = min(1, float(1024.0 / length_x))
    size = int(factor * length_x), int(factor * width_y)
    imr = im.resize(size, Image.ANTIALIAS)
    # saving the image with optimized quality
    imr.save(path, optimize = True, quality = 95)

    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))
    print("===== Detect Printed Text with OCR - local =====")
    # Get that optimized image with printed text
    local_image_printed_text_path = path
    local_image_printed_text = open(local_image_printed_text_path, "rb")

    ocr_result_local = client.recognize_printed_text_in_stream(local_image_printed_text)

    ls = []
    # variable for storing the date of birth of the cardholder
    dob = None
    # variable for storing the pan number the cardholder
    pan_no = None
    name = None
    line_nm = -1
    for region in ocr_result_local.regions:
        for c,line in enumerate(region.lines):
            s = ""
            for word in line.words:
                s += word.text + " "
            # print(s)
            # Name verification
            if len(difflib.get_close_matches(s, ['NAME']))!=0:
                line_nm = c            
            # dob verification
            if is_date(s):
                dob = s
            ls.append(s)
    # previous line of pan verification
    ln, pan_no = find_id(ls,  '(Number|umber|Account|ccount|count|\
                        Permanent|ermanent|manent)$')
    pan_no = pan_no[0].replace(" ", "") 
    
    # PAN id
    if ln == -9999:
        pan_no = 'Can not read pan no' 
    
    # DOB
    if dob is None:
        dob = 'Could not detect date'  
    
    # NAME
    if line_nm != -1:
        name = ls[line_nm + 1]
    else:
        wordstring = '(GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT\
             |PARTMENT|ARTMENT|INDIA|NDIA)$'
        for wordline in ls:
            xx = wordline.split()
            print(xx)
            if ([w for w in xx if re.search(wordstring.upper(), w) or re.search(wordstring.lower(), w)]):
                name = ls[ls.index(wordline)+1]
                break
        
        if name == None:
            name = 'Can not read NAME'

    return [name,dob,pan_no]

   
'''
if __name__ == '__main__':
    print(extract_text('sayan_pan.jpg'))
'''