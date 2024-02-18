import os
import zipfile
import requests
import sqlite3
import csv

DESTINY2_URL = 'https://www.bungie.net/Platform/Destiny2/'
watermarkToSeason = {
    "/common/destiny2_content/icons/fb50cd68a9850bd323872be4f6be115c.png": [1,'2017-09-06','2017-12-05'],
    "/common/destiny2_content/icons/dd71a9a48c4303fd8546433d63e46cc7.png": [1,'2017-09-06','2017-12-05'],
    "/common/destiny2_content/icons/2c024f088557ca6cceae1e8030c67169.png": [2,'2017-12-05','2018-05-08'],
    "/common/destiny2_content/icons/50d36366595897d49b5d33e101c8fd07.png": [2,'2017-12-05','2018-05-08'],
    "/common/destiny2_content/icons/ed6c4762c48bd132d538ced83c1699a6.png": [3,'2018-05-08','2018-09-04'],
    "/common/destiny2_content/icons/aaa61f6c70478d87de0df41e5709a773.png": [3,'2018-05-08','2018-09-04'],
    "/common/destiny2_content/icons/1b6c8b94cec61ea42edb1e2cb6b45a31.png": [4,'2018-09-04','2018-12-04'],
    "/common/destiny2_content/icons/eb621df1be42ae5db9e8cd20eda17c44.png": [4,'2018-09-04','2018-12-04'],
    "/common/destiny2_content/icons/448f071a7637fcefb2fccf76902dcf7d.png": [5,'2018-12-04','2019-03-05'],
    "/common/destiny2_content/icons/c23c9ec8709fecad87c26b64f5b2b9f5.png": [5,'2018-12-04','2019-03-05'],
    "/common/destiny2_content/icons/1448dde4efdb57b07f5473f87c4fccd7.png": [6,'2019-03-05','2016-06-04'],
    "/common/destiny2_content/icons/e4a1a5aaeb9f65cc5276fd4d86499c70.png": [6,'2019-03-05','2016-06-04'],
    "/common/destiny2_content/icons/5364cc3900dc3615cb0c4b03c6221942.png": [7,'2016-06-04','2019-10-01'],
    "/common/destiny2_content/icons/69bb11f24279c7a270c6fac3317005b2.png": [7,'2016-06-04','2019-10-01'],
    "/common/destiny2_content/icons/2352f9d04dc842cfcdda77636335ded9.png": [8,'2019-10-01','2019-12-10'],
    "/common/destiny2_content/icons/ee3f5bb387298acbdb03c01940701e63.png": [8,'2019-10-01','2019-12-10'],
    "/common/destiny2_content/icons/e8fe681196baf74917fa3e6f125349b0.png": [8,'2019-10-01','2019-12-10'],
    "/common/destiny2_content/icons/82a8d6f2b1e4ee14e853d4ffbe031406.png": [8,'2019-10-01','2019-12-10'],
    "/common/destiny2_content/icons/3ba38a2b9538bde2b45ec9313681d617.png": [9,'2019-12-10','2020-03-10'],
    "/common/destiny2_content/icons/9b7e4bbc576fd15fbf44dfa259f8b86a.png": [9,'2019-12-10','2020-03-10'],
    "/common/destiny2_content/icons/b12630659223b53634e9f97c0a0a8305.png": [10,'2020-03-10','2020-06-09'],
    "/common/destiny2_content/icons/e27a4f39c1bb8c6f89613648afaa3e9f.png": [10,'2020-03-10','2020-06-09'],
    "/common/destiny2_content/icons/4c25426263cacf963777cd4988340838.png": [11,'2020-06-09','2020-11-10'],
    "/common/destiny2_content/icons/49dc693c5f3411b9638b97f38a70b69f.png": [11,'2020-06-09','2020-11-10'],
    "/common/destiny2_content/icons/9e0f43538efe9f8d04546b4b0af6cc43.png": [12,'2020-11-10','2021-02-09'],
    "/common/destiny2_content/icons/1f702463c5e0c4e25c9f00a730dbc6ac.png": [12,'2020-11-10','2021-02-09'],
    "/common/destiny2_content/icons/be3c0a95a8d1abc6e7c875d4294ba233.png": [12,'2020-11-10','2021-02-09'],
    "/common/destiny2_content/icons/d3cffdcb881085bc4fe19d9671c9eb0c.png": [12,'2020-11-10','2021-02-09'],
    "/common/destiny2_content/icons/0ec87dd7ef282db27e1fc337e9545cd0.png": [12,'2020-11-10','2021-02-09'],
    "/common/destiny2_content/icons/5ac4a1d48a5221993a41a5bb524eda1b.png": [13,'2021-02-09','2021-05-11'],
    "/common/destiny2_content/icons/e197b731c11556b17664b90a87dd0c11.png": [13,'2021-02-09','2021-05-11'],
    "/common/destiny2_content/icons/23968435c2095c0f8119d82ee222c672.png": [14,'2021-05-11','2021-08-24'],
    "/common/destiny2_content/icons/a9faab035e2f59f802e99641a3aaab9e.png": [14,'2021-05-11','2021-08-24'],
    "/common/destiny2_content/icons/671a19eca92ad9dcf39d4e9c92fcdf75.png": [15,'2021-08-24','2021-12-07'],
    "/common/destiny2_content/icons/d92e077d544925c4f37e564158f8f76a.png": [15,'2021-08-24','2021-12-07'],
    "/common/destiny2_content/icons/6e4fdb4800c34ccac313dd1598bd7589.png": [16,'2022-02-22','2022-05-24'],
    "/common/destiny2_content/icons/b973f89ecd631a3e3d294e98268f7134.png": [16,'2022-02-22','2022-05-24'],
    "/common/destiny2_content/icons/d05833668bcb5ae25344dd4538b1e0b2.png": [16,'2022-02-22','2022-05-24'],
    "/common/destiny2_content/icons/ab075a3679d69f40b8c2a319635d60a9.png": [17,'2022-05-24','2022-08-23'],
    "/common/destiny2_content/icons/a3923ae7d2376a1c4eb0f1f154da7565.png": [18,'2022-08-23','2022-12-06'],
    "/common/destiny2_content/icons/e775dcb3d47e3d54e0e24fbdb64b5763.png": [19,'2022-12-06','2023-02-28'],
    "/common/destiny2_content/icons/31445f1891ce9eb464ed1dcf28f43613.png": [20,'2023-02-28','2023-05-22'],
    "/common/destiny2_content/icons/af00bdcd3e3b89e6e85c1f63ebc0b4e4.png": [20,'2023-02-28','2023-05-22'],
    "/common/destiny2_content/icons/a568c77f423d1b49aeccbce0e7af79f6.png": [20,'2023-02-28','2023-05-22'],
    "/common/destiny2_content/icons/6026e9d64e8c2b19f302dafb0286897b.png": [21,'2023-05-22','2023-08-22'],
    "/common/destiny2_content/icons/3de52d90db7ee2feb086ef6665b736b6.png": [22,'2023-08-22','2023-11-28'],
    "/common/destiny2_content/icons/a2fb48090c8bc0e5785975fab9596ab5.png": [23,'2023-11-28','2024-06-04']
}
#dictionary of season watermark to season number as well as start and end date
damageType = {
    0: "None",
    1: "Kinetic",
    2: "Arc",
    3: "Solar",
    4: "Void",
    5: "Raid",
    6: "Stasis",
    7: "Strand"
}
#dict of enum to dmg type 
slotHashToSlot = {
    1498876634:'Kinetic',
    2465295065:'Energy',
    953998645 :'Heavy'
}
#dict of slot hash to slot

def update_manifest():
    '''If there is a new manifest, grab and return path, else return last manifest path'''
    #prepare header and url to send using requests
    header = {'X-API-KEY':'61bee9a3181f47afa237fc254c7f3dbf'}
    url = "https://www.bungie.net/Platform/Destiny2/Manifest/"

    #send http get request
    r = requests.get(url)
    response = r.json()

    #check if retrieval was successful
    if response['ErrorCode'] != 1:
        raise ConnectionError("Could not retrieve Manifest from Bungie.net")

    #prepare url for download and name for file
    manifest_url = 'https://www.bungie.net' + response['Response']['mobileWorldContentPaths']['en']
    manifest_filename = manifest_url.split('/')[-1]

    if not os.path.isfile(manifest_filename.split('.')[0] + '.sqlite3'):
        #download contents and write as zip file
        r = requests.get(manifest_url, allow_redirects=True)
        open('manifest_test.zip', 'wb').write(r.content)

        #unzip file
        with zipfile.ZipFile('./manifest_test.zip') as zip_ref:
            zip_ref.extractall('./')
            zip_ref.close()
            os.remove('manifest_test.zip')

        temp = manifest_filename.split('.')[0]
        os.rename(manifest_filename, temp + '.sqlite3')
        return temp + '.sqlite3'
    else:
        print('No update to Destiny 2 manifest since last execution.\n')
        return manifest_filename.split('.')[0] + '.sqlite3'

def cnvthash(somehash):
    id = int(somehash) #put hash # inside int()
    if (id & (1 << (32 - 1))) != 0:
        id = id - (1 << 32)
    return id

def season_statistics(manifest, season):
    connection = sqlite3.connect(manifest)
    crsr = connection.cursor()

    seasons = "'"
    #some seasons have multiple watermarks associated so grab all watermark urls associated with the season
    for url in watermarkToSeason:
        if watermarkToSeason[url][0] == int(season):
            seasons += str(url) + "', '"
    seasons = seasons[:len(seasons)-4] + "'"
    #grab counts of every type of equipment from the season
    statement = "SElECT JSON_extract(json, '$.itemTypeDisplayName') AS type,  COUNT(JSON_extract(json, '$.itemTypeDisplayName')) AS count FROM DestinyInventoryItemDefinition WHERE JSON_extract(json, '$.inventory.bucketTypeHash') IN (953998645, 2465295065, 1498876634) AND JSON_extract(json, '$.iconWatermark') IN (" + seasons + ") AND JSON_extract(json, '$.damageTypeHashes') NOT NULL AND JSON_extract(json, '$.inventory.tierTypeName') = 'Legendary' GROUP BY type ORDER BY count DESC"

    crsr.execute(statement)
    result = crsr.fetchall()

    counts = {}
    total = 0
    for row in result:
        total += row[1]
        counts[row[0]] = row[1]
    counts["Total"] = total

    crsr.close()
    connection.close()

    return counts
    

def export_to_excel(manifest):
    connection = sqlite3.connect(manifest)
    crsr = connection.cursor()

    #select name, tier, damage type, weapon type, equipment slot, and season from all primary, energy and heavey weapons
    crsr.execute("SELECT JSON_extract(json, '$.displayProperties.name') AS name, JSON_extract(json, '$.inventory.tierTypeName') AS tier, Json_extract(json, '$.damageTypes') AS dmgType, JSON_extract(json, '$.itemTypeDisplayName') AS type, CASE WHEN JSON_extract(json, '$.itemTypeDisplayName') LIKE '%Fusion%' THEN JSON_extract(json, '$.stats.stats.2961396640.value') WHEN JSON_extract(json, '$.itemTypeDisplayName') LIKE '%Bow%' THEN JSON_extract(json, '$.stats.stats.2961396640.value') ELSE JSON_extract(json, '$.stats.stats.4284893193.value') END AS subtype, JSON_extract(json, '$.inventory.bucketTypeHash') AS slot, JSON_extract(json, '$.iconWatermark') AS season FROM DestinyInventoryItemDefinition WHERE JSON_extract(json, '$.inventory.bucketTypeHash') IN (953998645, 2465295065, 1498876634) AND JSON_extract(json, '$.damageTypeHashes') NOT NULL AND JSON_extract(json, '$.inventory.tierTypeName') = 'Legendary' ORDER BY type")
    result = crsr.fetchall()


    csv_file_path = 'weapons.csv'
    #begin writing to csv file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        #use column descriptions for headers in csv file and add missing headers
        header = [description[0] for description in crsr.description]
        header.extend(['season_start','season_end'])
        csv_writer.writerow(header)
        for row in result:
            row = list(row)
            #convert damage type and slot hash to understandable string
            row[2] = damageType[int(row[2][1])]
            row[5] = slotHashToSlot[row[5]]
            #if watermark corresponds to a season, convert the watermark to the season number and append start/end dates
            if row[6] in watermarkToSeason:
                watermarkStr = row[6]
                row[6] = watermarkToSeason[watermarkStr][0] 
                row.append(watermarkToSeason[watermarkStr][1])
                row.append(watermarkToSeason[watermarkStr][2])
            else:
                row[6] = 'other'
                row.extend(['None','None'])
            csv_writer.writerow(row)


    crsr.close()
    connection.close()
    return True