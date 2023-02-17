import PyPDF2
import constant


def scraper(CTfile):
    cybertip_number = 0
    n_pages = 0
    sp_page = 0
    keywords = {
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
    #Finding the Suspect info page
    for i in range(2, n_pages):
        page = pdfFile.pages[i].extract_text()
        if (constant.SP_PAGE_KEYWORD in page):
            for line in page.split("\n"):
                #Get the username
                if "Screen/User Name" in line:
                    usr_list = line.split()
                    if len(usr_list) == 3:
                        keywords["username"] = usr_list[2]
                    elif len(usr_list) > 3:
                        for e in usr_list[2:]:
                            keywords["username"] += " " + e
                keywords["username"] = keywords["username"].strip()
                #Get the ESP
                if "ESP User ID" in line:
                    esp_list = line.split()
                    if len(esp_list) == 4:
                        keywords["ESP"] = esp_list[3]
                    elif len(esp_list) > 4:
                        for e in esp_list[3:]:
                            keywords["ESP"] += " " + e
                keywords["ESP"] = keywords["ESP"].strip()
    print(keywords["username"])
    print(keywords["ESP"])





