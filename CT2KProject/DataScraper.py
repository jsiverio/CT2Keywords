import PyPDF2
import constant
import re


def scraper(CTfile):
    cybertip_number = 0
    n_pages = 0
    content_page = 0
    keywords = {
        "name": [],
        "username": "",
        "ESP": "",
        "email": [],
        "file name": [],
        "hashes": [],
        "ip": []
    }

    pdfFile = PyPDF2.PdfReader(CTfile)
    n_pages = len(pdfFile.pages)-1 # Not interested in the last page
    #Extracting the cybertip number on the first page
    page = pdfFile.pages[0].extract_text()
    for line in page.split("\n"):
        if "CyberTipline Report" in line:
            cybertip_number = line.split()[5]

    # Getting suspect keywords

    for i in range(2, n_pages):
        page = pdfFile.pages[i].extract_text()
        for line in page.split("\n"):
            #Get Name
            if "Name:" in line:
                name_str = ""
                name_list = line.split()
                if len(name_list) < 4:
                    if len(name_list) == 2:
                        keywords["name"].append(name_list[1])
                    elif len(name_list) > 2:
                        for e in name_list[1:3]:
                            name_str += " " + e
                        name_str =name_str.strip()
                        keywords["name"].append(name_str)
    
        #Get the username
            if "Screen/User Name:" in line:
                usr_list = line.split()
                if len(usr_list) == 3:
                    keywords["username"] = usr_list[2]
                elif len(usr_list) > 3:
                    for e in usr_list[2:]:
                        keywords["username"] += " " + e
                    keywords["username"] = keywords["username"].strip()

        #Get the ESP
            if "ESP User ID:" in line:
                esp_list = line.split()
                if len(esp_list) == 4:
                    keywords["ESP"] = esp_list[3]
                elif len(esp_list) > 4:
                    for e in esp_list[3:]:
                        keywords["ESP"] += " " + e
                    keywords["ESP"] = keywords["ESP"].strip()

        #Get emails
        email_list = []
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[^ncmec]+\.[A-Z|a-z]{2,}\b'
        result = re.search(regex, page)
        if result:
            keywords["email"].append(result.group())

        #Get Hashes
        md5_list = []
        regex = r"\b(?!^[\d]*$)(?!^[a-fA-F]*$)([a-f\d]{32}|[A-F\d]{32})\b"
        result = re.findall(regex, page)
        if result:
            keywords["hashes"].append(result)

        #Get IPs
        ip_list = []
        regex_ipv4 = re.compile(
            r"((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))")
        regex_ipv6 = re.compile(
            r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))",
            re.IGNORECASE)
        result_ipv4 = re.findall(regex_ipv4, page)
        result_ipv6 = re.findall(regex_ipv6, page)
        if len(result_ipv4) > 0:
            keywords["ip"].append(result_ipv4)
        elif len(result_ipv6) > 0:
            keywords["ip"].append(result_ipv6)




    print(cybertip_number)
    print(n_pages)
    print(keywords["name"])
    print(keywords["username"])
    print(keywords["ESP"])
    print(keywords["email"])
    print(keywords["hashes"])
    print(keywords["ip"])





