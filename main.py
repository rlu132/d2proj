import helper
import os

manifest = helper.update_manifest()

cont = True
seasonStats = {}

while cont:
    choice = input(" 1. View Basic Season Statistics \n 2. Export to Excel \n 3. Exit \n")
    match choice:
        case "1":
            seasonchoice = input("Please input the season you would like to view: ")
            print("Generating basic statistics from Season " + str(seasonchoice))
            #querying takes awhile so save previous results 
            if input not in seasonStats.keys(): 
                seasonStats[input] = helper.season_statistics(manifest, seasonchoice)
            print("In season " + str(input) + " Bungie released:")
            print(seasonStats[input])
        case "2":
            print("Loading...")
            helper.export_to_excel(manifest)
            print("Completed.")
        case "3":
            cont = False

print("Have a good day")