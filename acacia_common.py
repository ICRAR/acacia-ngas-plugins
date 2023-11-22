import logging
import os
import subprocess


logger = logging.getLogger(__name__)

# These could be given as plug-in parameters to the archive event handler
# plug-in, but not (currently) to the stating plug-in.
# Therefore we *only* taken them from the environment for the time being,
# avoiding confusion as to which configuration mechanism should be used.
_ACACIA_BUCKET = os.getenv("ACACIA_BUCKET", "ngas-files")
_RCLONE_ACACIA_REMOTE = os.getenv("RCLONE_ACACIA_REMOTE", "provide-a-RCLONE_ACACIA_REMOTE-env-variable")


def to_acacia_filename(filename: str) -> str:
    """Turns a filesystem name into an Acacia rclone reference"""
    return f"{_RCLONE_ACACIA_REMOTE}:{_ACACIA_BUCKET}/{filename}"


def rclone(*args, check=True, **popen_kwargs) -> None:
    """Runs rclone with the given arguments"""
    logger.info("Running: rclone %s", " ".join(args))
    subprocess.run(("rclone",) + args, check=check, **popen_kwargs)
