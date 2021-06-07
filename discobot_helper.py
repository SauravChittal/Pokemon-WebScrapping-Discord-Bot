from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# /sets Hippowdon OU is not working, fix that

import time

opti = Options()
opti.headless = True

driver = webdriver.Chrome(ChromeDriverManager().install(), port=0, options=opti)

file_read = open("Tiers.txt", "r")
file_write = open("Tiers.txt", "a")
main_tier_list = str(file_read.read())
main_tier_list = main_tier_list.split(",")

def get_sets(message):
    """The helper function which actually does all the heavy lifting"""
    liste = message.split(" ")
    liste.remove(r"/sets")

    actua_string = ""

    if len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        actua_string = " ".join(liste[2:])
        liste[2] = "-".join(liste[2:])
        del(liste[3:])
    elif len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        actua_string = " ".join(liste[1:])
        liste[1] = "-".join(liste[1:])
        del(liste[2:])
    assert len(liste) <= 3

    if len(liste) == 1:
        liste.append("SS")
        liste.append("")
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        liste.insert(1, "SS")
        actua_string = liste[2]
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        liste.append("")
    driver.get("https://www.smogon.com/dex/{0}/pokemon/{1}/{2}".format(liste[1], liste[0], liste[2])) 

    finalstr = "```"
    all_exports = driver.find_elements_by_class_name("ExportButton")
    sets = driver.find_elements_by_class_name("BlockMovesetInfo")
    if len(all_exports) == 0:
        return "```The Pokemon doesn't have an analysis in said generation and tier```"
    for i in range(len(all_exports)):
        all_exports[i].click()
        time.sleep(3)
        finalstr += sets[i].text + "\n\n"
    selected_el = driver.find_elements_by_class_name("is-selected")

    actua_string = actua_string.replace("-", " ")

    print("Selected text is {0} and actua text is {1}".format(selected_el[1].text.upper(), actua_string.upper()))

    if liste[2] != "" and selected_el[1].text.upper() != actua_string.upper():
        finalstr += "The set(s) for {0} are from within the {1} tier from your specified (or SS) generation, since there was some error with your specified tier, hence the default sets are shown. For sets from a specific tier, type the tier at the end".format(liste[0], selected_el[1].text)
    else:
        finalstr += "The set(s) for {0} are from within the {1} tier. For sets from a specific tier, type the tier at the end".format(liste[0], selected_el[1].text)
        if liste[2] != "" and liste[2].upper() not in main_tier_list:
            file_write.write("," + liste[2].upper())
    finalstr += "```"
    return finalstr

def get_tiers(message):
    """This gets and shows the tiers for a Pokemon which have analysis"""
    liste = message.split(" ")
    liste.remove(r"/tier")

    if len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        liste[2] = "-".join(liste[2:])
        del(liste[3:])
    elif len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        liste[1] = "-".join(liste[1:])
        del(liste[2:])
    assert len(liste) <= 3

    if len(liste) == 1:
        liste.append("SS")
        liste.append("")
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        liste.insert(1, "SS")
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        liste.append("")

    try:
        driver.get("https://www.smogon.com/dex/{0}/pokemon/{1}/{2}".format(liste[1], liste[0], liste[2]))
    except:
        return "```The Pokemon you entered is incorrect```"

    try:
        all = str(driver.find_element_by_class_name("PokemonPage-StrategySelector").text)
        all = all.replace(" ", "-")
        all = all.upper()

        listOfTier = []
        for i in main_tier_list:
            if all.__contains__(i):
                listOfTier.append(i)

        if len(listOfTier) == 0:
            return "```The Pokemon you mentioned doesn't have an analysis in any tier for the generation```"
        stri = "```"
        for i in listOfTier:
            if len(i) == 2 or len(i) == 3:
                stri += str(i) + "    "
            else:
                stri += str(i).title() + "    "
        stri += "```"
        return stri
    except:
        return "```The Pokemon you entered is incorrect```"
