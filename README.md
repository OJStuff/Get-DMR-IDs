# Introduction

This program is intended for radio amateur use. It runs from the command-line, and creates and exports a selection of DMR IDs to a file in csv format, that can be imported to AnyTone D878/D578 DMR radios. You must, however, use the software provided by the radio manufacturer to import the file to your radio. The program can also export to an ordinary texfile (but this is not intended for any radio).

## Program

Downloaded data from [radioid.net](https:/radioid.net) (users.json) comes in json file format. The program uses country codes from the file [country_codes.py](country_codes.py) and region codes from the file [region_codes.py](region_codes.py) to identify selected regions and countries for export.

If you want to view a list of all available region codes, then try this shell command at the program location:

    more region_codes.py

If you want to view a list of all available country codes, then try this shell command at the program location:

    more country_codes.py

All data from radioid.net (users.json) is in UTF-8 format, which is not very radio device friendly. All data exported from the program will therefore be translated to ASCII format with the unidecode library. This library must therefore be installed before you can run the program. The installation of this library can be done with this shell command:

    pip install unidecode

## Basic use

### Example 1

This command shows how to get help using the prgram.

    >dmridget.py -h
    usage: .\dmridget.py [-h] [-d] [-f {anytone,text}] [-r [REGION ...]] [-c [COUNTRY ...]]

    program creates formatted file with dmr-id's based on users criteria that can be imported into a dmr trx, like AnyTone D878/D578

    options:
    -h, --help            show this help message and exit
    -d, --download        download DMR database from https://radioid.net
    -f {anytone,text}, --format {anytone,text}
                            file format for the formatted file
    -r [REGION ...], --region [REGION ...]
                            region codes added for the formatted file
    -c [COUNTRY ...], --country [COUNTRY ...]
                            country codes added/subtracted for the formatted file

    updated version and resources may be found at https://GitHub.com/OJStuff

### Example 2

This command specifies to download an updated DMR ID user database and then create export for region 2 (Europe). File format will be for default traceiver type (AnyTone D878/D578) and the file will be named "users-anytone.csv".

    >python3 dmridget.py -d -r 2

    downloading DMR database users.json (42,348 kB downloaded)

    options specified for production of the export file:
    -r 2 include region: Europe
    DMRID file (users-anytone.csv) exported with 94,705 IDs

### Example 3

This command specifies to create export for region 2 (Europe). Country 302 (Canada) will also be added to the collection, but Norway (242) will ble excluded. File format will be for default traceiver type (AnyTone D878/D578) and the file will be named "users-anytone.csv".

    >python3 dmridget.py -r 2 -c 302 -242

    options specified for production of the export file:
    -r 2 include region: Europe
    -c 302 include country: Canada
    -c -242 exclude country: Norway
    DMRID file (users-anytone.csv) exported with 99,661 IDs

### Example 4

This command specifies to create export for region 1, 2 and 3. File format will be for default traceiver type (AnyTone D878/D578) and the file will be named "users-anytone.csv".

    >python3 dmridget.py -r 1 2 3

    options specified for production of the export file:
    -r 1 include region: North America and Canada (DMARC)
    -r 2 include region: Europe
    -r 3 include region: North America and the Caribbean
    DMRID file (users-anytone.csv) exported with 218,264 IDs
