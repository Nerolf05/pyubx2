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


def nav_decode(gnssId: int, dwrds: list) -> tuple:
    """
    Helper function to decode parts of the RXM-SFRBX dwrds for navigation data.

    :param gmssId: gnssId
    :param dwrds: Array of up to 10 x 32 bit nav data dwrds
    :return: tuple of (subframe, almanac svid)
    :rtype: tuple

    """

    if gnssId == 0:
        (sfr, svid) = gps_nav_decode(dwrds)
        return (sfr, svid)


def gps_nav_decode(dwrds: list) -> tuple:
    """
    Helper function to decode parts of the RXM-SFRBX dwrds for GPS navigation data.

    :param list: array of navigation data dwrds
    :return: tuple of (subframe, almanac svid)
    :rtype: tuple

    """

    svid = 0
    pre = dwrds[0] >> 22 & 0b11111111
    sfr = dwrds[1] >> 8 & 0b111
    if sfr in [4, 5]:
        svid = dwrds[2] >> 22 & 0b111111
    # print(
    #     f"DEBUG gps_decode: num words = {len(dwrds)}, preamble = {pre},  subframe = {sfr}, almanac svid = {svid}"
    # )
    return (sfr, svid)


def galileo_nav_decode(dwrds: list):
    """
    Helper function to decode parts of the RXM-SFRBX dwrds for GALILEO navigation data.

    :param list: array of navigation data dwrds

    """


def glonass_nav_decode(dwrds: list):
    """
    Helper function to decode parts of the RXM-SFRBX dwrds for GLONASS navigation data.

    :param list: array of navigation data dwrds

    """


def beidou_nav_decode(dwrds: list):
    """
    Helper function to decode parts of the RXM-SFRBX dwrds for BEIDOU navigation data.

    :param list: array of navigation data dwrds

    """
