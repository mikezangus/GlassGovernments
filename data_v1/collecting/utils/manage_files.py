from .await_downloads import await_downloads
from .move_files import move_files
from .unzip_files import unzip_files


def manage_files(
    download_dir: str,
    election_year: str
) -> None:
    if not await_downloads(download_dir):
        return
    elif not move_files(
        download_dir,
        election_year
    ):
        return
    elif not unzip_files(election_year):
        return
    return
