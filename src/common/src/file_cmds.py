"""
Module for methods reading from and writing to the file system
"""

import os
import logging
import rascsi_constants
from rascsi_client import RaScsiClient


class FileTools:

    def __init__(self, rascsi_client:RaScsiClient):
        self._rascsi_client = rascsi_client

    # noinspection PyMethodMayBeStatic
    def list_config_files(self):
        """
        Finds fils with file ending CONFIG_FILE_SUFFIX in CFG_DIR.
        Returns a (list) of (str) files_list
        """
        files_list = []
        for root, dirs, files in os.walk(rascsi_constants.CFG_DIR):
            for file in files:
                if file.endswith("." + rascsi_constants.CONFIG_FILE_SUFFIX):
                    files_list.append(file)
        return files_list

    # noinspection PyMethodMayBeStatic
    def read_config(self, file_name):
        """
        Takes (str) file_name
        Returns (dict) with (bool) status and (str) msg
        """
        from json import load
        file_name = f"{rascsi_constants.CFG_DIR}/{file_name}"
        try:
            with open(file_name) as json_file:
                config = load(json_file)
                # If the config file format changes again in the future,
                # introduce more sophisticated format detection logic here.
                if isinstance(config, dict):
                    self._rascsi_client.detach_all()
                    ids_to_reserve = []
                    for item in config["reserved_ids"]:
                        ids_to_reserve.append(item["id"])
                        rascsi_constants.RESERVATIONS[int(item["id"])] = item["memo"]
                    self._rascsi_client.reserve_scsi_ids(ids_to_reserve)
                    for row in config["devices"]:
                        kwargs = {
                            "device_type": row["device_type"],
                            "image": row["image"],
                            "unit": int(row["unit"]),
                            "vendor": row["vendor"],
                            "product": row["product"],
                            "revision": row["revision"],
                            "block_size": row["block_size"],
                        }
                        params = dict(row["params"])
                        for param in params.keys():
                            kwargs[param] = params[param]
                        self._rascsi_client.attach_image(row["id"], **kwargs)
                # The config file format in RaSCSI 21.10 is using a list data type at the top level.
                # If future config file formats return to the list data type,
                # introduce more sophisticated format detection logic here.
                elif isinstance(config, list):
                    self._rascsi_client.detach_all()
                    for row in config:
                        kwargs = {
                            "device_type": row["device_type"],
                            "image": row["image"],
                            # "un" for backwards compatibility
                            "unit": int(row["un"]),
                            "vendor": row["vendor"],
                            "product": row["product"],
                            "revision": row["revision"],
                            "block_size": row["block_size"],
                        }
                        params = dict(row["params"])
                        for param in params.keys():
                            kwargs[param] = params[param]
                        self._rascsi_client.attach_image(row["id"], **kwargs)
                else:
                    return {"status": False, "msg": "Invalid configuration file format"}  # TODO:localization reversed!!
                return {
                    "status": True,
                    "msg": "Loaded configurations from: " + file_name,  # TODO:localization reversed!!!
                }
        except (IOError, ValueError, EOFError, TypeError) as error:
            logging.error(str(error))
            return {"status": False, "msg": str(error)}
        except:
            logging.error("Could not read file: %s", file_name)
            return {
                "status": False,
                "msg": "Could not read configuration file: " + file_name,  # TODO:localization reversed!!!
            }


