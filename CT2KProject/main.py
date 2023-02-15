import PyPDF2
import re


# Return page where keyword hit is found.
def page_finder(pdfstream, keyword):
    page_count = len(pdfstream.pages)
    hit = 0
    for i in range(2, page_count - 1):
        page = pdfstream.pages[i].extract_text()
        if (keyword in page):
            hit = i
    return (hit)


"""
NCMEC List the suspects username under the "Suspect" section usually found under "Screen/User Name
The function seeks for that keyword and extracts the line which returns a list of n items. If the username is one
word, then it will be the 3rd item or the the items from the 3rd position to the end of the list.
"""
def get_id_username(sp_page):
    usr_list = []
    usr_string = ""

    for line in sp_page.split("\n"):
        if "Screen/User Name" in line:
            usr_list = line.split()
    if len(usr_list) == 3:
        return usr_list[2]
    elif len(usr_list) > 3:
        for e in usr_list[2:]:
            usr_string += " " + e
        return usr_string.strip()


"""
NCMEC List the suspects ESP under the "Suspect" section. The function seeks for that keyword and extracts
the ESP or USER ID in the same manner as the get_id_username(1) function does
"""
def get_id_esp(sp_page):
    esp_list = []
    esp_string = ""

    for line in sp_page.split("\n"):
        if "ESP User ID" in line:
            esp_list = line.split()
    if len(esp_list) == 4:
        return esp_list[3]
    elif len(esp_list) > 4:
        for e in esp_list[3:]:
            esp_string += " " + e
        return esp_string.strip()


def get_emails(pdfstream, start_page):
    email_list = []
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[^ncmec]+\.[A-Z|a-z]{2,}\b'
    page_count = len(pdfstream.pages)
    for i in range(start_page, page_count - 1):
        page = pdfstream.pages[i].extract_text()
        result = re.search(regex, page)
        if result:
            email_list.append(result.group())
    return email_list

def get_md5(pdfstream,start_page):
    md5_list=[]
    regex = r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b"
    page_count = len(pdfstream.pages)
    for i in range(start_page, page_count - 1):
        page = pdfstream.pages[i].extract_text()
        result = re.findall(regex, page)
        if len(result) > 0:
            md5_list += result
    md5_list = list(dict.fromkeys(md5_list))
    return md5_list

def get_file_names(pdfstream,start_page):
    file_list=[]
    regex = r'\b[\D\d]+\.[a-zA-Z\d]{3}'
    page_count = len(pdfstream.pages)
    for i in range(start_page, page_count - 1):
        page = pdfstream.pages[i].extract_text()
        result = re.findall(regex, page)
        if len(result) > 0:
            print(result)
            file_list += result
    file_list = list(dict.fromkeys(file_list))
    return file_list






file_obj = PyPDF2.PdfReader('Dataset/109290088.pdf')
suspect_page = page_finder(file_obj, "Section A:")
suspect_page_text = file_obj.pages[suspect_page].extract_text()

print(get_id_username(suspect_page_text))
print(get_id_esp(suspect_page_text))
print((get_emails(file_obj, suspect_page)))
print(get_md5(file_obj,suspect_page))
print(get_file_names(file_obj,suspect_page))


