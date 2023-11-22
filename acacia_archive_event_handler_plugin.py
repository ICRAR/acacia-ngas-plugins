from ngamsLib.ngamsDbCore import NGAS_FILES_FILE_NAME
from ngamsLib.ngamsDiskInfo import ngamsDiskInfo
from ngamsLib.ngamsFileInfo import ngamsFileInfo
from ngamsServer.ngamsServer import archive_event, ngamsServer

from acacia_common import to_acacia_filename, rclone

class AcaciaArchivingEventHandler:

    # The rclone remote could have been given as a plug-in parameter,
    # but I chose to use the same environment variable required by the
    # staging plug-in to avoid confusion on how to configure that value

    def handle_event(self, event: archive_event):
        # This works because we assume there's a single copy of a file
        # id/version in any of the disks in the system, which isn't *always*
        # the case.
        db = event.server.db
        file_info = ngamsFileInfo()
        file_info.read(event.server.host_id, db, event.file_id, fileVersion=event.file_version)

        disk_info = ngamsDiskInfo()
        disk_info.read(db, event.disk_id)

        volume_dir = event.server.cfg.getVolumeDirectory()
        disk_mount_point = disk_info.getMountPoint()
        assert disk_mount_point.startswith(volume_dir)
        disk_dir = disk_mount_point[len(volume_dir):]

        filename = f"{disk_mount_point}/{file_info.getFilename()}"
        relative_filename = f"{disk_dir}/{file_info.getFilename()}"
        acacia_filename = to_acacia_filename(relative_filename)

        rclone("copy", filename, acacia_filename)
