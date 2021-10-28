import os
from pyubx2 import UBXReader
from logging import getLogger
import warnings


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
                ubr = UBXReader(stream=rec, ubxonly=False)
                try:
                    (raw_data, parsed_data) = ubr.read()
                except UBXParseError as e:
                    warnings.warn(str(e))
                    continue

                if not parsed_data:
                    break
                elif parsed_data.identity == "RXM-SFRBX":
                    # print_ubx_rxm_sfrbx(ubx_msg=parsed_data)
                    ubx_nav_msg_parser.add_raw_data(ubx_msg=parsed_data)

                if not ubx_nav_msg_parser.need_data:
                    decoded_msgs = ubx_nav_msg_parser.decode_nav_msgs()

                # exit conditions
                if idx > 15_000:
                    cond = False
                    decoded_msgs = ubx_nav_msg_parser.decode_nav_msgs()
            except UBXMessageError as e:
                logger.warning(f"UBXMessage Error: {e}")
            except StopIteration as _:
                logger.info(f"Iterator exhausted.")
                cond = False
    assert False, f"END - {idx}"
    pass
