import os
from logging import getLogger
from collections import namedtuple
import warnings

import pytest

from pyubx2.pyubx_nav_msg_decoder.ubx_nav_message_parser import UbxNavMessageParserHandle
from pyubx2.ubxreader import UBXReader
from pyubx2.exceptions import UBXMessageError, UBXParseError

ubx_cfg = namedtuple("ubx_cfg", ('folder', 'record_file'))
glo_cfg = ubx_cfg("data", "COM3_211031_144044_glo.ubx")
gps_cfg = ubx_cfg("data", "COM3_211031_135504_raw_gps.ubx")
gal_cfg = ubx_cfg("data", "COM3_211031_171502_raw_gal.ubx")


def test_gnss_nav_msg_offline(ubx_offline_config):
    """Parse navigation message of recorded .ubx file with ubx-rxm-sfrbx messages."""
    logger = getLogger()
    logger.info(f"Reading record-file: {ubx_offline_config.record_file}")
    record_path = os.path.join(ubx_offline_config.folder, ubx_offline_config.record_file)
    idx = 0
    cond = True
    assert os.path.isfile(record_path), f"File: {record_path} is no valid file."

    ubx_nav_msg_parser = UbxNavMessageParserHandle()

    with open(record_path, "rb") as rec:
        while cond:
            try:
                idx += 1
                ubr = UBXReader(stream=rec, ubxonly=False, decodenavdata=False)
                try:
                    (_, parsed_data) = ubr.read()
                except UBXParseError as e:
                    warnings.warn(str(e))
                    continue

                if not parsed_data:
                    break
                elif parsed_data.identity == "RXM-SFRBX":
                    # print_ubx_rxm_sfrbx(ubx_msg=parsed_data)
                    ubx_nav_msg_parser.add_subframe(ubx_msg=parsed_data)

            except UBXMessageError as e:
                logger.warning(f"UBXMessage Error: {e}")
            except StopIteration as _:
                logger.info(f"Iterator exhausted.")
                cond = False
    assert False, f"END - {idx}"
    pass


if __name__ == '__main__':
    test_gnss_nav_msg_offline(glo_cfg)
    pass
