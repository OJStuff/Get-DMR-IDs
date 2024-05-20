"""
Environment: Thonny IDE v4.1.4 and builtin Python v3.10.11.
Copyright: Released under CC BY-SA 4.0
Author: GitHub/OJStuff, May 20, 2024, v1.0
"""

import sys
import os
import argparse
import requests
import json
import csv
from unidecode import unidecode

from region_codes import DMR_RC
from country_codes import DMR_CC

DMR_URL: str = "https://radioid.net/static/users.json"


def strLeftJust(string: str, width: int, fill: str = " ") -> str:
    """
    Create a left justified string and fill unused space
    Args:
        string: A string
        width: Width of left justified string
        fill: Fill string
    Returns:
        A left justified string
    """
    if len(string) > width:
        string = string[:width]
    fill = fill * width
    return (string + fill)[:width]


def fileExist(file: str) -> bool:
    """
    Check the existence of file
    Args:
        file: Local filname
    Returns:
        True if file exists
    """
    status = os.path.exists(file)
    return status


def jsonLoad(file: str) -> dict:
    """
    Loads a json file
    Args:
        file: Json filename
    Returns:
        data: Json dictionary
    """
    with open(file, "rt", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
    return data


def jsonDump(file: str, data: dict) -> None:
    """
    Dumps a local json file
    Args:
        file: Local json filename
        data: Data as a dictionary
    Returns:
        None
    """
    with open(file, "wt", encoding="utf-8") as jsonFile:
        json.dump(data, jsonFile)
    return None


def urlExist(url: str) -> bool:
    """
    Checks the existence of url
    Args:
        url: Url to check
    Returns:
        True if url exists
    """
    try:
        permanentRedirect: int = 308
        r = requests.head(url, timeout=5)
        status = r.status_code in (requests.codes.ok, permanentRedirect)
    except:
        status = False
    return status


def urlLoad(file: str, url: str, info: bool) -> bool:
    """
    Download file from url in blocks of 1024 bytes
    Args:
        file: Local filname
        url: Url to download
        info: True if info about downloaded kB will be shown
    Returns:
        None
    """
    try:
        status: bool = True
        count: int = 0
        r = requests.get(url, timeout=5)
        with open(file, "wb") as f:
            for block in r.iter_content(1024):
                f.write(block)
                count += 1
            f.close()
        if info:
            sep = ","
            print(f" ({count:{sep}} kB downloaded)")
    except:
        status = False
    return status


def removeConjugate(inputList: list) -> list:
    """
    Removes conjugates (x and -x pairs) in a list
    Args:
        inputList: List to process
    Returns:
        A list with conjugates (x and -x pairs) removed
    """
    negList: list = []
    for nr in inputList:
        if nr < 0:
            negList.append(nr)
    for nr in negList:
        if (-nr) in inputList:
            inputList.remove(nr)
            inputList.remove(-nr)
    return inputList


def argsHandle() -> tuple[bool, str, list, list]:
    """
    Collects and checks arguments before processing
    Args:
        None
    Returns:
        status: Returns True ig args are OK
        fFormat: Returns a string with selected file format
        cList: Returns a list of selected country codes
        rList: Returns a list of selected region codes
    """
    status: bool = True
    fFormat: str = ""
    cList: list = []
    rList: list = []

    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="""program creates formatted file with dmr-id's
        based on users criteria that can be imported into a dmr trx,
        like AnyTone D878/D578""",
        epilog="""updated version and resources may be found at
        https://GitHub.com/OJStuff""",
    )

    parser.add_argument(
        "-d",
        "--download",
        help="download DMR database from https://radioid.net",
        action="store_true",
    )

    parser.add_argument(
        "-f",
        "--format",
        help="file format for the formatted file",
        default=["anytone"],
        choices=["anytone", "text"],
        nargs=1,
    )

    parser.add_argument(
        "-r",
        "--region",
        help="region codes added for the formatted file",
        type=int,
        nargs="*",
    )

    parser.add_argument(
        "-c",
        "--country",
        help="country codes added/subtracted for the formatted file",
        type=int,
        nargs="*",
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        print(f"\nplease try {sys.argv[0]} -h if you need help")

    downActive = args.download
    if downActive:
        if urlExist(DMR_URL):
            print(f"\ndownloading DMR database {os.path.basename(DMR_URL)}", end="")
            if not urlLoad(os.path.basename(DMR_URL), DMR_URL, True):
                print(f"\nproblem downloading {DMR_URL} -> network problems !")
                sys.exit(1)
        else:
            print(f"\n{DMR_URL} unreachable -> network problems !")
            sys.exit(1)

    fFormat = args.format

    regionActive = not ((args.region == []) or (args.region == None))
    if regionActive:
        rList = list(set(args.region))

    countryActive = not ((args.country == []) or (args.country == None))
    if countryActive:
        cList = removeConjugate(list(set(args.country)))

    if (not regionActive) and (not countryActive):
        print("\nno options specified to do anything...")
        status = False

    if regionActive:
        print("\noptions specified for production of the export file:")
        for n in rList:
            if n in DMR_RC.keys():
                print("-r", n, "include region:", DMR_RC[n])
            else:
                print("-r", n, "ignore region: (non existant)")

    if countryActive:
        countryRemove: list = []
        for n in cList:
            if abs(n) in DMR_CC.keys():
                if n < 0:
                    firstDigitCountry = int(str(n)[1])
                    if firstDigitCountry not in rList:
                        print("-c", n, "exclude country:", DMR_CC[-n], "(redundant)")
                        countryRemove.append(n)
                    else:
                        print("-c", n, "exclude country:", DMR_CC[-n])
                else:
                    firstDigitCountry = int(str(n)[0])
                    if firstDigitCountry in rList:
                        print("-c", n, "include country:", DMR_CC[n], "(redundant)")
                        countryRemove.append(n)
                    else:
                        print("-c", n, "include country:", DMR_CC[n])
            else:
                print("-c", n, "ignores country: (non existant)")
        for r in countryRemove:
            cList.remove(r)

    if not fileExist(os.path.basename(DMR_URL)):
        print(f"\ncan't find local DMR database {os.path.basename(DMR_URL)}")
        print(f"\nUse -d option to download {os.path.basename(DMR_URL)}")
        status = False
    return status, fFormat, cList, rList


def regionInclude(id: int, rList: list) -> bool:
    """
    Check if id is a wanted dmr user according to region list
    Args:
        id: DMR ID to check
        rList: List of region codes
    Returns:
        status: True if region match for id
    """
    status = int(str(id)[0]) in rList
    return status


def countryInclude(id: int, cList: list) -> bool:
    """
    Check if id is a wanted dmr user according to country list
    Args:
        id: DMR ID to check
        cList: List of country codes
    Returns:
        status: True if country match for id
    """
    status = int(str(id)[:3]) in cList
    return status


def countryExclude(id: int, cList: list) -> bool:
    """
    Check if id is an unwanted dmr user according to list of excluded countries
    Args:
        id: DMR ID to check
        cList: List of country codes
    Returns:
        status: True if country exclude match for id
    """
    status = -int(str(id)[:3]) in cList
    return status


def dmrSelection(cList: list, rList: list) -> list[dict]:
    """
    Returns a list of dmr data from selection criteria
    Args:
        None
    Returns:
        selection: A list of dictionaries with dmr data
    """
    selection: list = []
    dmrDB = jsonLoad(os.path.basename(DMR_URL))
    for i in dmrDB["users"]:
        if regionInclude(i["radio_id"], rList) and not countryExclude(
            i["radio_id"], cList
        ):
            selection.append(i)
        if not regionInclude(i["radio_id"], rList) and countryInclude(
            i["radio_id"], cList
        ):
            selection.append(i)
    return selection


def dmrTouchup(data: list) -> list[dict]:
    """
    Returns a list of dmr data from selection criteria that is converted from
    utf-8 to ascii, since radioes do not like to display utf-8 on screen.
    So: æ -> ae, ø -> o, å -> a, ü -> u and so on.
    Args:
        data: A list of data to touch up
    Returns:
        dataToucup: A list of dictionaries with dmr data
    """
    dataToucup: list = []
    for x in data:
        x["fname"] = unidecode(x["fname"])
        x["fname"] = x["fname"].title()
        x["name"] = unidecode(x["name"])
        x["name"] = x["name"].title()
        x["country"] = unidecode(x["country"])
        x["country"] = x["country"].title()
        x["callsign"] = x["callsign"].upper()
        x["city"] = unidecode(x["city"])
        x["city"] = x["city"].title()
        x["surname"] = unidecode(x["surname"])
        x["surname"] = x["surname"].title()
        x["state"] = unidecode(x["state"])
        x["state"] = x["state"].title()
        dataToucup.append(x)
    return dataToucup


def dmrExportAnytone(data: list, file: str) -> None:
    """
    Creates csv file formatted for AnyTone D878/D578 for export
    Args:
        Data: List of selected DMR IDs
        File: Filename for exported file
    Returns:
        None
    """
    # dataWidth AnyTone D878/D578: list = [8, 8, 16, 16, 16, 16, 16, 12, 4]
    csvHead: list = [
        "Radio ID",
        "Callsign",
        "Name",
        "City",
        "State",
        "Country",
        "Remarks",
        "Call Type",
        "Call Alert",
    ]
    csvRows: list = []
    csvRows.append(csvHead)

    for x in data:
        csvRow: list = [
            x["radio_id"],
            x["callsign"],
            x["fname"],
            x["city"],
            x["state"],
            x["country"],
            "",
            "Private Call",
            "None",
        ]
        csvRows.append(csvRow)

    with open(file, "wt", newline="", encoding="utf-8") as csvfile:
        cswriter = csv.writer(csvfile)
        cswriter.writerows(csvRows)
        print(f"DMRID file ({file}) exported with {len(data):,} IDs")
    return None


def dmrExportText(data: list, file: str) -> None:
    """
    Creates txt file formatted as text for export
    Args:
        Data: List of selected DMR IDs
        File: Filename for exported file
    Returns:
        None
    """
    dataWidth: list = [30, 30, 30, 10, 30, 30, 10, 10, 30]
    txtRow: str = ""
    txtRows: list = []

    txtHead = [
        "fname",
        "name",
        "country",
        "callsign",
        "city",
        "surname",
        "radio_id",
        "id",
        "state",
    ]

    for x in range(len(txtHead)):
        txtRow += strLeftJust(txtHead[x], dataWidth[x])
    txtRows.append(txtRow + "\n\n")

    for x in data:
        txtRow = (
            strLeftJust(x["fname"], dataWidth[0])
            + strLeftJust(x["name"], dataWidth[1])
            + strLeftJust(x["country"], dataWidth[2])
            + strLeftJust(x["callsign"], dataWidth[3])
            + strLeftJust(x["city"], dataWidth[4])
            + strLeftJust(x["surname"], dataWidth[5])
            + strLeftJust(str(x["radio_id"]), dataWidth[6])
            + strLeftJust(str(x["id"]), dataWidth[7])
            + strLeftJust(x["state"], dataWidth[8])
        )
        txtRows.append(txtRow + "\n")

    with open(file, "wt", encoding="utf-8") as txtFile:
        txtFile.writelines(txtRows)
        txtFile.close()

    print(f"DMRID file ({file}) exported with {len(data):,} IDs")
    return None


def main() -> None:
    dmrData: list = []
    argsOK: bool = False
    countryList: list = []
    regionList: list = []

    argsOK, fileFormat, countryList, regionList = argsHandle()

    if argsOK and fileExist(os.path.basename(DMR_URL)):
        dmrData = dmrSelection(countryList, regionList)
        dmrData = dmrTouchup(dmrData)

        if fileFormat[0] == "anytone":
            dmrExportAnytone(
                dmrData, os.path.basename(DMR_URL).replace(".json", "-anytone.csv")
            )

        if fileFormat[0] == "text":
            dmrExportText(
                dmrData, os.path.basename(DMR_URL).replace(".json", "-text.txt")
            )


if __name__ == "__main__":
    main()
