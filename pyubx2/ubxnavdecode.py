"""
Helper methods for decoding RXM-SFRBX navigation data.

TODO WORK IN PROGRESS 

Created on 01 Nov 2021

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

# TODO might use these definitions if it makes code clearer:
# import pyubx2.ubxtypes_navdata as ubn

GPS = 0
SBAS = 1
GALILEO = 2
BEIDOU = 3
IMES = 4
QZSS = 5
GLONASS = 6

# bitshift flags for clarity
B2 = 0b11
B3 = 0b111
B4 = 0b1111
B5 = 0b11111
B6 = 0b111111
B8 = 0b11111111
B10 = 0b1111111111
B11 = 0b11111111111
B14 = 0b11111111111111
B16 = 0b1111111111111111
B17 = 0b11111111111111111
B22 = 0b1111111111111111111111
B24 = 0b111111111111111111111111


def nav_decode(gnssId: int, dwrds: list) -> dict:
    """
    Helper function to decode parts of the RXM-SFRBX dwrds for navigation data.

    :param int gmssId: gnssId (0 = GPS, etc.)
    :param list dwrds: array of up to 10 x 32-bit navdata dwrds
    :return: attd - dict of decoded navdata attributes
    :rtype: dict

    """

    # print(f"DEBUG nav_decode navdata = {dwrds}")
    if gnssId == GPS:
        attd = gps_nav_decode(dwrds)
    elif gnssId == SBAS:
        attd = sbas_nav_decode(dwrds)
    elif gnssId == GALILEO:
        attd = galileo_nav_decode(dwrds)
    elif gnssId == BEIDOU:
        attd = beidou_nav_decode(dwrds)
    elif gnssId == IMES:
        attd = imes_nav_decode(dwrds)
    elif gnssId == QZSS:
        attd = qzss_nav_decode(dwrds)
    elif gnssId == GLONASS:
        attd = glonass_nav_decode(dwrds)
    return attd


def gps_nav_decode(dwrds: list) -> dict:
    """
    TODO Helper function to decode RXM-SFRBX dwrds for GPS navigation data.

    The message structure shall utilize a basic format of a 1500 bit long frame made up
    of five subframes, each subframe being 300 bits long. Subframes 4 and 5 shall be
    subcommutated 25 times each, so that a complete data message shall require the
    transmission of 25 full frames. The 25 versions of subframes 4 and 5 shall be
    referred to herein as pages 1 through 25 of each subframe. Each subframe shall
    consist of ten words, each 30 bits long; the MSB of all words shall be transmitted first.

    :param list dwrds: array of navigation data dwrds
    :return: dict of decoded navdata attributes
    :rtype: dict

    """

    svid = 0

    # TOW & HOW header for all subframes (dwrds 0 & 1)
    sfr = dwrds[1] >> 8 & 0b111
    attd = {
        "preamble": dwrds[0] >> 22 & B8,
        "tlm": dwrds[0] >> 8 & B14,
        "isf": dwrds[0] >> 7 & 0b1,
        "tow": dwrds[1] >> 13 & B17,
        "alert": dwrds[1] >> 12 & 0b1,
        "antispoof": dwrds[1] >> 11 & 0b1,
        "subframe": sfr,
    }

    # subframe 1
    if sfr == 1:
        attd["week_no"] = dwrds[2] >> 20 & B10
        attd["l2code"] = dwrds[2] >> 18 & B2
        attd["uraIndex"] = dwrds[2] >> 14 & B4
        attd["svHealth1"] = dwrds[2] >> 13 & 0b1
        attd["svHealth2"] = dwrds[2] >> 8 & B5
        iodc_msb = dwrds[2] >> 1 & B2
        attd["l2p"] = dwrds[3] >> 29 & 0b1
        attd["tgd"] = dwrds[6] >> 6 & B8
        iodc_lsb = dwrds[7] >> 22 & B8
        attd["iodc"] = (iodc_msb << 8) + iodc_lsb
        attd["toc"] = dwrds[7] >> 6 & B16
        attd["af2"] = dwrds[8] >> 22 & B8
        attd["af1"] = dwrds[8] >> 6 & B16
        attd["af0"] = dwrds[9] >> 8 & B22

    # subframes 2 - ephemeris data
    if sfr == 2:
        attd["iodc"] = dwrds[2] >> 22 & B8
        attd["crs"] = dwrds[2] >> 6 & B16
        attd["Δn"] = dwrds[3] >> 14 & B16
        mg_msb = dwrds[3] >> 6 & B8
        mg_lsb = dwrds[4] >> 6 & B24
        attd["mg"] = (mg_msb << 24) + mg_lsb
        attd["cuc"] = dwrds[5] >> 14 & B16
        e_msb = dwrds[5] >> 6 & B8
        e_lsb = dwrds[6] >> 6 & B24
        attd["e"] = (e_msb << 24) + e_lsb
        attd["cus"] = dwrds[7] >> 14 & B16
        sqra_msb = dwrds[7] >> 6 & B8
        sqra_lsb = dwrds[8] >> 6 & B24
        attd["sqra"] = (sqra_msb << 24) + sqra_lsb
        attd["toe"] = dwrds[9] >> 14 & B16
        attd["fint"] = dwrds[9] >> 13 & 0b1
        attd["aodo"] = dwrds[9] >> 8 & B5

    # subframes 3 - ephemeris data
    if sfr == 3:
        attd["cic"] = dwrds[2] >> 14 & B16
        Ω0_msb = dwrds[2] >> 6 & B8
        Ω0_lsb = dwrds[3] >> 6 & B24
        attd["Ω0"] = (Ω0_msb << 24) + Ω0_lsb
        attd["cis"] = dwrds[4] >> 14 & B16
        i0_msb = dwrds[4] >> 6 & B8
        i0_lsb = dwrds[5] >> 6 & B24
        attd["i0"] = (i0_msb << 24) + i0_lsb
        attd["crc"] = dwrds[6] >> 14 & B16
        ω_msb = dwrds[6] >> 6 & B8
        ω_lsb = dwrds[7] >> 6 & B24
        attd["ω"] = (ω_msb << 24) + ω_lsb
        attd["Ω."] = dwrds[8] >> 6 & B24
        attd["iode"] = dwrds[9] >> 22 & B8
        attd["idot"] = dwrds[9] >> 6 & B14

    # subframes 4 and 5 all pages
    if sfr in [4, 5]:
        dataid = dwrds[2] >> 28 & B2
        svid = dwrds[2] >> 22 & B6
        attd["dataid"] = dataid
        attd["svidAlm"] = svid

    # subframe 4 pages 1, 6, 11, 16, 21 - Reserved
    if sfr == 4 and svid == 57:
        pass  # TODO no usable data?
    # subframe 4 pages 12, 19, 20, 22, 23, 24 - Reserved
    if sfr == 4 and svid in [58, 59, 60, 61, 62]:
        pass  # TODO no usable data?
    # subframe 4 pages 14, 15, 17 - Reserved & special messages
    if sfr == 4 and svid in [53, 54, 55]:
        pass  # TODO no usable data?

    # subframe 4 page 13 - Navigation Message Correction Table (NMCT)
    if sfr == 4 and svid == 52:
        pass  # TODO

    # subframe 4 page 18 - Ionospheric and UTC data
    if sfr == 4 and svid == 56:
        attd["α0"] = dwrds[2] >> 14 & B8
        attd["α1"] = dwrds[2] >> 6 & B8
        attd["α2"] = dwrds[3] >> 22 & B8
        attd["α3"] = dwrds[3] >> 14 & B8
        attd["β0"] = dwrds[3] >> 6 & B8
        attd["β1"] = dwrds[4] >> 22 & B8
        attd["β2"] = dwrds[4] >> 14 & B8
        attd["β3"] = dwrds[4] >> 6 & B8
        attd["a1"] = dwrds[5] >> 6 & B24
        a0_msb = dwrds[6] >> 6 & B24
        a0_lsb = dwrds[7] >> 22 & B8
        attd["a0"] = (a0_msb << 8) + a0_lsb
        attd["tot"] = dwrds[7] >> 14 & B8
        attd["wnt"] = dwrds[7] >> 6 & B8
        attd["Δtls"] = dwrds[8] >> 22 & B8
        attd["wnlsf"] = dwrds[8] >> 14 & B8
        attd["dn"] = dwrds[8] >> 6 & B8
        attd["Δtlsf"] = dwrds[9] >> 8 & B8

    # subframe 4 page 25 - SV health SV 25-32, A-S flags, SV conf
    if sfr == 4 and svid == 63:
        pass  # TODO

    # subframe 5 pages 1-24 - Almanac data SV 1-24
    # subframe 4 pages 2, 3, 4, 5, 7, 8, 9, 10 - Almanac data SV 25-32
    if (sfr == 5 and svid != 51) or (
        sfr == 4 and svid in [25, 26, 27, 28, 29, 30, 31, 32]
    ):
        attd["e"] = dwrds[2] >> 6 & B16
        attd["toa"] = dwrds[3] >> 22 & B8
        attd["δi"] = dwrds[3] >> 6 & B16
        attd["Ω."] = dwrds[4] >> 14 & B16
        attd["svhealth"] = dwrds[4] >> 6 & B8
        attd["sqra"] = dwrds[5] >> 6 & B24
        attd["Ω0"] = dwrds[6] >> 6 & B24
        attd["ω"] = dwrds[7] >> 6 & B24
        attd["m0"] = dwrds[8] >> 6 & B24
        af0_msb = dwrds[9] >> 22 & B8
        attd["af1"] = dwrds[9] >> 11 & B11
        af0_lsb = dwrds[9] >> 8 & B3
        attd["af0"] = (af0_msb << 3) + af0_lsb

    # subframe 5 page 25 - SV health SV 1-24, Almanac ref time & week
    if sfr == 5 and svid == 51:
        attd["toa"] = dwrds[2] >> 14 & B8
        attd["wna"] = dwrds[2] >> 6 & B8
        attd["svhealth01"] = dwrds[3] >> 24 & B6
        attd["svhealth02"] = dwrds[3] >> 18 & B6
        attd["svhealth03"] = dwrds[3] >> 12 & B6
        attd["svhealth04"] = dwrds[3] >> 6 & B6
        attd["svhealth05"] = dwrds[4] >> 24 & B6
        attd["svhealth06"] = dwrds[4] >> 18 & B6
        attd["svhealth07"] = dwrds[4] >> 12 & B6
        attd["svhealth08"] = dwrds[4] >> 6 & B6
        attd["svhealth09"] = dwrds[5] >> 24 & B6
        attd["svhealth10"] = dwrds[5] >> 18 & B6
        attd["svhealth11"] = dwrds[5] >> 12 & B6
        attd["svhealth12"] = dwrds[5] >> 6 & B6
        attd["svhealth13"] = dwrds[6] >> 24 & B6
        attd["svhealth14"] = dwrds[6] >> 18 & B6
        attd["svhealth15"] = dwrds[6] >> 12 & B6
        attd["svhealth16"] = dwrds[6] >> 6 & B6
        attd["svhealth17"] = dwrds[7] >> 24 & B6
        attd["svhealth18"] = dwrds[7] >> 18 & B6
        attd["svhealth19"] = dwrds[7] >> 12 & B6
        attd["svhealth20"] = dwrds[7] >> 6 & B6
        attd["svhealth21"] = dwrds[8] >> 24 & B6
        attd["svhealth22"] = dwrds[8] >> 18 & B6
        attd["svhealth23"] = dwrds[8] >> 12 & B6
        attd["svhealth24"] = dwrds[8] >> 6 & B6

    return attd


def galileo_nav_decode(dwrds: list) -> dict:
    """
    Helper function to decode RXM-SFRBX dwrds for GALILEO navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}  # TODO just a stub for now


def glonass_nav_decode(dwrds: list) -> dict:
    """
    Helper function to decode RXM-SFRBX dwrds for GLONASS navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}  # TODO just a stub for now


def beidou_nav_decode(dwrds: list) -> dict:
    """
    Helper function to decode RXM-SFRBX dwrds for BEIDOU navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}  # TODO just a stub for now


def sbas_nav_decode(dwrds: list) -> dict:
    """
    Helper function to decode RXM-SFRBX dwrds for SBAS navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}  # TODO just a stub for now


def imes_nav_decode(dwrds: list) -> dict:
    """
    Helper function to decode RXM-SFRBX dwrds for IMES navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}  # TODO just a stub for now


def qzss_nav_decode(dwrds: list) -> dict:
    """
    Helper function to decode RXM-SFRBX dwrds for QZSS navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}  # TODO just a stub for now
