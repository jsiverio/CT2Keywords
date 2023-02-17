import re
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