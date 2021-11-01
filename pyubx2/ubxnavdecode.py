"""
TODO WORK IN PROGRESS 

Helper methods for decoding RXM-SFRBX navigation data.

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
    :return: dict of navdata attributes
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

    :param list dwrds: array of navigation data dwrds
    :return: dict of navdata attributes
    :rtype: dict

    """

    svid = 0
    pre = dwrds[0] >> 22 & 0b11111111
    sfr = dwrds[1] >> 8 & 0b111
    if sfr in [4, 5]:
        svid = dwrds[2] >> 22 & 0b111111
    # print(
    #     f"DEBUG gps_decode: num words = {len(dwrds)}, preamble = {pre},  subframe = {sfr}, almanac svid = {svid}"
    # )
    return {"subframe": sfr, "svidAlm": svid, "dwrds": dwrds}


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
