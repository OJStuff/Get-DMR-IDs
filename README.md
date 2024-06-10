# Introduction

This program is intended for radio amateur use. It runs from the command-line, and creates and exports a selection of DMR IDs to a file in csv format, that can be imported to AnyTone D878/D578 DMR radios. You must, however, use the software provided by the radio manufacturer to import the file to your radio. The program can also export to an ordinary texfile (but this is not intended for any radio).

## Program

Downloaded data from [radioid.net](https://radioid.net) (users.json) comes in json file format. The program uses country codes from the file [country_codes.py](country_codes.py) and region codes from the file [region_codes.py](region_codes.py) to identify selected regions and countries for export.

If you want to view a list of all available region codes, then try this shell command at the program location:

    more region_codes.py

If you want to view a list of all available country codes, then try this shell command at the program location:

    more country_codes.py

All data from radioid.net (users.json) is in UTF-8 format, which is not very radio device friendly. All data exported from the program will therefore be translated to ASCII format with the unidecode library. This library must therefore be installed before you can run the program. The installation of this library can be done with this shell command:

    pip install unidecode

## Basic use

### Example 1

This command shows how to get help using the prgram.

    >getdmrids.py -h
    usage: getdmrids.py [-h] [-s] [-d] [-f {anytone,text}] [-r [REGION ...]]
                    [-c [COUNTRY ...]]

    Program exports a formatted file with dmr-id's based on users criteria. This
    file can be imported into a radio, like AnyTone D878/D578, as digital contact
    list

    options:
    -h, --help            show this help message and exit
    -s, --statistics      show statistics for formatted file with dmr-id's
    -d, --download        download raw dmr database from https://radioid.net
    -f {anytone,text}, --format {anytone,text}
                            file format for the formatted file
    -r [REGION ...], --region [REGION ...]
                            region codes added for the formatted file
    -c [COUNTRY ...], --country [COUNTRY ...]
                            country codes added/subtracted for the formatted file

    Updated version and resources may be found at https://GitHub.com/OJStuff

### Example 2

This command specifies to download an updated raw DMR ID user database, and then create formatted export file for region 2 (Europe). File format will be for default traceiver type (AnyTone D878/D578) and the file will be named "users-anytone.csv".

    >python3 getdmrids.py -d -r 2

    Downloading DMR database users.json (42,597 kB downloaded)

    Options specified for export of formatted file:
    -r 2 include region: Europe
    DMR ID file (users-anytone.csv) was exported with 95,125 IDs

### Example 3

This command specifies to create formatted export file for region 2 (Europe). Country 302 (Canada) will also be added to the collection, but Norway (242) will ble excluded. File format will be for default traceiver type (AnyTone D878/D578) and the file will be named "users-anytone.csv".

    >python3 getdmrids.py -r 2 -c 302 -242

    Options specified for export of formatted file:
    -r 2 include region: Europe
    -c 302 include country: Canada
    -c -242 exclude country: Norway
    DMR ID file (users-anytone.csv) was exported with 100,106 IDs

### Example 4

This command specifies to create formatted export file for region 1, 2 and 3 with statistics. File format will be for default traceiver type (AnyTone D878/D578) and the file will be named "users-anytone.csv".

    >python3 getdmrids.py -r 1 2 3 -s

    Options specified for export of formatted file:
    -r 1 include region: North America and Canada
    -r 2 include region: Europe
    -r 3 include region: North America and the Caribbean
    DMR ID file (users-anytone.csv) was exported with 219,251 IDs

    Statistics for exported formatted file:
            0 IDs from region 0: Test networks
        8,863 IDs from region 1: North America and Canada
       95,125 IDs from region 2: Europe
      115,263 IDs from region 3: North America and the Caribbean
            0 IDs from region 4: Asia and the Middle East
            0 IDs from region 5: Australia and Oceania
            0 IDs from region 6: Africa
            0 IDs from region 7: South and Central America
            0 IDs from region 8: Not used
            0 IDs from region 9: Worldwide (Satellite, Aircraft, Maritime, Antarctica)
