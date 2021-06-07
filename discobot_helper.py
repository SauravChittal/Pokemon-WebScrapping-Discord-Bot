from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

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
    # The message is received in the form /sets (Pokemon) (Generation), here you remove /sets
    liste = message.split(" ")
    liste.remove(r"/sets")

    # actua_string is used to check whether the tier they entered is correct or not
    actua_string = ""

    # This if-elif statements turn tier with multiple names into 1.
    # For example, Almost Any Ability becomes Almost-Any-Ability
    if len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        actua_string = " ".join(liste[2:])
        liste[2] = "-".join(liste[2:])
        del(liste[3:])
    elif len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        actua_string = " ".join(liste[1:])
        liste[1] = "-".join(liste[1:])
        del(liste[2:])
    assert len(liste) <= 3

    # This set of if functions is basically used to enter in the remaining details if 
    # they are not entered. For example, if the user inputs /sets Hydreigon, these
    # if functions put the tier in as "" and Generation as "SS", similarly if either
    # one of those is provided
    if len(liste) == 1:
        liste.append("SS")
        liste.append("")
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        liste.insert(1, "SS")
        actua_string = liste[2]
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        liste.append("")
    driver.get("https://www.smogon.com/dex/{0}/pokemon/{1}/{2}".format(liste[1], liste[0], liste[2])) 

    # This portion of my function was done in a bit of a rush, since I just added new functionality
    # and didn't have enough time to fully test it
    try:
        finalstr = "```"
        # Actual Web Scraping
        all_exports = driver.find_elements_by_class_name("ExportButton")
        sets = driver.find_elements_by_class_name("BlockMovesetInfo")
        if len(all_exports) == 0:
            return "```The Pokemon doesn't have an analysis in said generation and tier```"
        # After going to the site, it clicks on the export button and copies the text presented
        for i in range(len(all_exports)):
            all_exports[i].click()
            time.sleep(3)
            finalstr += sets[i].text + "\n\n"
        selected_el = driver.find_elements_by_class_name("is-selected")

        actua_string = actua_string.replace("-", " ")
        # Here we make use of actua-string. If the tier represented by actua-string and the tier
        # tier currently selected are the same, then we got the correct tier, else either the tier
        # is incorrect or analysis doesn't exist in that tier
        if liste[2] != "" and selected_el[1].text.upper() != actua_string.upper():
            finalstr += "The set(s) for {0} are from within the {1} tier from your specified (or SS) generation, since there was some error with your specified tier, hence the default sets are shown. For sets from a specific tier, type the tier at the end".format(liste[0], selected_el[1].text)
        else:
            finalstr += "The set(s) for {0} are from within the {1} tier. For sets from a specific tier, type the tier at the end".format(liste[0], selected_el[1].text)
            if liste[2] != "" and liste[2].upper() not in main_tier_list:
                file_write.write("," + liste[2].upper())
        finalstr += "```"
        return finalstr
    except:
        return "```The Pokemon or Generation you entered is incorrect```"

# I'll only comment new things in this function
def get_tiers(message):
    """This gets and shows the tiers for a Pokemon which have analysis"""
    liste = message.split(" ")
    liste.remove(r"/tier")

    # In this and the next if statements, I don't have to worry about a third argument
    if len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        liste[2] = "-".join(liste[2:])
        del(liste[3:])
    elif len(liste) > 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        liste[1] = "-".join(liste[1:])
        del(liste[2:])
    assert len(liste) <= 2

    if len(liste) == 1:
        liste.append("SS")
        liste.append("")
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is False:
        return "```The Generation you entered is incorrect```"
    if len(liste) == 2 and "SSSMXYBWDPRSGSRB".__contains__(liste[1].upper()) is True:
        liste.append("")

 
    driver.get("https://www.smogon.com/dex/{0}/pokemon/{1}/{2}".format(liste[1], liste[0], liste[2]))

    try:
        # Web Scraping the tiers
        all = str(driver.find_element_by_class_name("PokemonPage-StrategySelector").text)
        all = all.replace(" ", "-")
        all = all.upper()
        # Trying to decipher which all tiers are present within all, since I
        # couldn't find a good algorithm to seperate it normally, I had to resort to
        # storing the tiers in a different file and checking it here. Leads to issues
        listOfTier = []
        for i in main_tier_list:
            if all.__contains__(i):
                listOfTier.append(i)
                all.replace(i, "", 1)

        if len(listOfTier) == 0:
            return "```The Pokemon you mentioned doesn't have an analysis in any tier for the generation```"
        stri = "```"
        # The first if statement preseve the capitalization of OU or NFE, otherwise puts them in title case
        for i in listOfTier:
            if len(i) == 2 or len(i) == 3:
                stri += str(i) + "    "
            else:
                stri += str(i).title() + "    "
        stri += "```"
        return stri
    except:
        return "```The Pokemon you entered is incorrect```"
