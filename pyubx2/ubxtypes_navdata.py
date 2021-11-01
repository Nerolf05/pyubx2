"""
UBX RXM-SFRBX Navigation Data Subframe Definitions

*** TODO WORK IN PROGRESS ***

Created on 31 Oct 2021

GPS information sourced from https://www.gps.gov/technical/icwg/IS-GPS-200L.pdf

:author: semuadmin
"""

from pyubx2.ubxtypes_core import (
    U1,
    U2,
    U3,
    U4,
    U5,
    U6,
    U7,
    U8,
    U22,
    X2,
    X4,
)

U10 = "U010"  # Unsigned Int 10 bytes
U11 = "U011"  # Unsigned Int 11 bytes
U14 = "U014"  # Unsigned Int 14 bytes
U16 = "U016"  # Unsigned Int 16 bytes
U17 = "U017"  # Unsigned Int 17 bytes
U23 = "U023"  # Unsigned Int 23 bytes
U24 = "U024"  # Unsigned Int 24 bytes


GPS_SUBFRAMES = {
    "RXM-SFRBX": {
        "gnssId": U1,
        "svId": U1,
        "reserved0": U1,
        "freqId": U1,
        "numWords": U1,
        "chn": U1,
        "version": U1,
        "reserved1": U1,
        "dword_01": (
            X4,
            {
                "padding1": U2,
                "preamble": U8,  # = 139 (0b10001011)
                "tlm": U14,
                "isf": U1,
                "reserved1": U1,
                "word1_parity": U6,
            },
        ),
        "dword_02": (
            X4,
            {
                "padding2": U2,
                "tow": U17,
                "alert": U1,
                "antispoof": U1,
                "sfrid": U3,  # subframe id 1 - 5
                "word2_paritycomp": U2,
                "word2_parity": U6,
            },
        ),
        "dword_03": X4,
        "dword_04": X4,
        "dword_05": X4,
        "dword_06": X4,
        "dword_07": X4,
        "dword_08": X4,
        "dword_09": X4,
        "dword_10": X4,
    },
    "GPS_SFR_HDR": {
        "preamble": U8,  # = 139 (0b10001011)
        "tlm": U14,
        "isf": U1,
        "reserved1": U1,
        "word1_parity": U6,
        "tow": U17,
        "alert": U1,
        "antispoof": U1,
        "sfrid": U3,  # subframe id 1 - 5
        "word2_paritycomp": U2,
        "word2_parity": U6,
    },
    "GPS_SFR_1": {
        "week_no": U10,
        "l2code": U2,
        "uraIndex": U4,
        "svHealth1": U1,
        "svHealth2": U5,
        "iodc_msb": U2,
        "word3_parity": U6,
        "l2p": U1,
        "reserved0": U23,
        "word4_parity": U6,
        "reserved1": U24,
        "word5_parity": U4,
        "reserved2": U24,
        "word6_parity": U6,
        "word7": U16,
        "tgd": U8,
        "word7_parity": U6,
        "iodc_lsb": U8,
        "toc": U16,
        "word8_parity": U6,
        "af2": U8,
        "af1": U16,
        "word9_parity": U6,
        "af0": U22,
        "word10_paritycomp": U2,
        "word10_parity": U6,
    },
    "GPS_SFR_2": {
        "iodc": U8,
        "crs": U16,
        "word3_parity": U6,
        "Δn": U16,
        "mg_msb": U8,
        "word4_parity": U6,
        "mg_lsb": U24,
        "word5_parity": U6,
        "cuc": U16,
        "e_msb": U8,
        "word6_parity": U6,
        "e_lsb": U24,
        "word7_parity": U6,
        "cus": U16,
        "sqra_msb": U8,
        "word8_parity": U6,
        "sqra_lsb": U24,
        "word9_parity": U6,
        "toe": U16,
        "fint": U1,
        "aodo": U5,
        "word10_paritycomp": U2,
        "word10_parity": U6,
    },
    "GPS_SFR_3": {
        "cic": U16,
        "Ω0_msb": U8,
        "word3_parity": U6,
        "Ω0_lsb": U24,
        "word4_parity": U6,
        "cis": U16,
        "i0_msb": U8,
        "word5_parity": U6,
        "i0_lsb": U24,
        "word6_parity": U6,
        "crc": U16,
        "ω_msb": U8,
        "word7_parity": U6,
        "ω_lsb": U24,
        "word8_parity": U6,
        "Ω.": U24,
        "word9_parity": U6,
        "iode": U8,
        "idot": U14,
        "word10_paritycomp": U2,
        "word10_parity": U6,
    },
    "GPS_SFR_4": {
        "dataid": U2,
        "svid": U6,
        "e": U16,
        "word3_parity": U6,
        "toa": U8,
        "Δi": U16,
        "word4_parity": U6,
        "Ω.": U16,
        "svhealth": U8,
        "word5_parity": U6,
        "sqra": U24,
        "word6_parity": U6,
        "Ω0": U24,
        "word7_parity": U6,
        "ω": U24,
        "word8_parity": U6,
        "m0": U24,
        "word9_parity": U6,
        "af0_msb": U8,
        "af1": U11,
        "af0_lsb": U3,
        "word10_paritycomp": U2,
        "word10_parity": U6,
    },
    "GPS_SFR_5": {
        "dataid": U2,
        "svid": U6,
        "toa": U8,
        "wna": U8,
        "word3_parity": U6,
        "svhealth01": U6,
        "svhealth02": U6,
        "svhealth03": U6,
        "svhealth04": U6,
        "word4_parity": U6,
        "svhealth05": U6,
        "svhealth06": U6,
        "svhealth07": U6,
        "svhealth08": U6,
        "word5_parity": U6,
        "svhealth09": U6,
        "svhealth10": U6,
        "svhealth11": U6,
        "svhealth12": U6,
        "word6_parity": U6,
        "svhealth13": U6,
        "svhealth14": U6,
        "svhealth15": U6,
        "svhealth16": U6,
        "word7_parity": U6,
        "svhealth17": U6,
        "svhealth18": U6,
        "svhealth19": U6,
        "svhealth20": U6,
        "word8_parity": U6,
        "svhealth21": U6,
        "svhealth22": U6,
        "svhealth23": U6,
        "svhealth24": U6,
        "word9_parity": U6,
        "reserved0": U6,
        "reserved1": U16,
        "word10_paritycomp": U2,
        "word10_parity": U6,
    },
}

GLONASS_SUBFRAMES = {}  # TODO

GALILEO_SUBFRAMES = {}  # TODO

BEIDOU_SUBFRAMES = {}  # TODO
