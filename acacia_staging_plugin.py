import os
import pathlib

from ngamsServer.ngamsServer import ngamsServer
from ngamsLib.ngamsReqProps import ngamsReqProps

from acacia_common import to_acacia_filename, rclone

def isFileOffline(filename: str) -> bool:
    """Returns 0 if file is online"""
    # Always retrieve from Acacia
    return 1


def stageFiles(filenames: list[str], requestObj: ngamsReqProps, serverObj: ngamsServer):
    assert len(filenames) == 1
    filename = filenames[0]
    volume_dir = serverObj.cfg.getVolumeDirectory()
    assert filename.startswith(volume_dir)
    filename = filename[len(volume_dir):]
    acacia_filename = to_acacia_filename(filename)
    os.makedirs(pathlib.Path(filename).parent, exist_ok=True)
    rclone("copy", acacia_filename, filename)
