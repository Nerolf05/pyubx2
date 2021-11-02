"""
Helper methods for decoding RXM-SFRBX navigation data.

TODO WORK IN PROGRESS 

Created on 01 Nov 2021

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""
# pylint: disable=invalid-name

import pyubx2.ubxtypes_navdata as ubn

GPS = 0
SBAS = 1
GALILEO = 2
BEIDOU = 3
IMES = 4
QZSS = 5
GLONASS = 6


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
    TODO Helper function to decode parts of the RXM-SFRBX dwrds for GPS navigation data.

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

    # TODO parse dwrds from ubxtypes_navdata.py subframe definitions
    svid = 0

    # TOW & HOW header for all subframes (dwrds 0 & 1)
    sfr = dwrds[1] >> 8 & 0b111
    attd = {
        "preamble": dwrds[0] >> 22 & 0b11111111,
        "tlm": dwrds[0] >> 8 & 0b11111111111111,
        "isf": dwrds[0] >> 7 & 0b1,
        "tow": dwrds[1] >> 13 & 0b11111111111111111,
        "alert": dwrds[1] >> 12 & 0b1,
        "antispoof": dwrds[1] >> 11 & 0b1,
        "subframe": sfr,
    }

    # subframe 1
    if sfr == 1:
        pass  # TODO

    # subframes 2 & 3 - ephemeris data
    if sfr == 2:
        pass  # TODO
    if sfr == 3:
        pass  # TODO

    # subframes 4 and 5 all pages
    if sfr in [4, 5]:
        dataid = dwrds[2] >> 28 & 0b11
        svid = dwrds[2] >> 22 & 0b111111
        attd["dataid"] = dataid
        attd["svidAlm"] = svid

    # subframe 4 pages 2, 3, 4, 5, 7, 8, 9, 10 - Almanac data SV 25-32
    if sfr == 4 and svid in [25, 26, 27, 28, 29, 30, 31, 32]:
        pass  # TODO
    # subframe 4 pages 1, 6, 11, 16, 21 - Reserved
    if sfr == 4 and svid == 57:
        attd["dwrds"] = dwrds
    # subframe 4 pages 12, 19, 20, 22, 23, 24 - Reserved
    if sfr == 4 and svid in [58, 59, 60, 61, 62]:
        attd["dwrds"] = dwrds
    # subframe 4 pages 14, 15, 17 - Reserved & special messages
    if sfr == 4 and svid in [53, 54, 55]:
        attd["dwrds"] = dwrds
    # subframe 4 page 18 - Ionospheric and UTC data
    if sfr == 4 and svid == 56:
        pass  # TODO
    # subframe 4 page 25 - SV health SV 25-32, A-S flags, SV conf
    if sfr == 4 and svid == 63:
        pass  # TODO
    # subframe 4 page 13 - Navigation Message Correction Table (NMCT)
    if sfr == 4 and svid == 52:
        pass  # TODO

    # subframe 5 pages 1-24 - Almanac data SV 1-24
    if sfr == 5 and svid != 51:
        pass  # TODO
    # subframe 5 page 25 - SV health SV 1-24, Almanac ref time & week
    if sfr == 5 and svid == 51:
        pass  # TODO

    return attd


def galileo_nav_decode(dwrds: list) -> dict:
    """
    TODO Helper function to decode parts of the RXM-SFRBX dwrds for GALILEO navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}


def glonass_nav_decode(dwrds: list) -> dict:
    """
    TODO Helper function to decode parts of the RXM-SFRBX dwrds for GLONASS navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}


def beidou_nav_decode(dwrds: list) -> dict:
    """
    TODO Helper function to decode parts of the RXM-SFRBX dwrds for BEIDOU navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}


def sbas_nav_decode(dwrds: list) -> dict:
    """
    TODO Helper function to decode parts of the RXM-SFRBX dwrds for SBAS navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}


def imes_nav_decode(dwrds: list) -> dict:
    """
    TODO Helper function to decode parts of the RXM-SFRBX dwrds for IMES navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}


def qzss_nav_decode(dwrds: list) -> dict:
    """
    TODO Helper function to decode parts of the RXM-SFRBX dwrds for QZSS navigation data.

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    return {"dwrds": dwrds}
