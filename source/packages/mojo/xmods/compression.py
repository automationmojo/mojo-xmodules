
import os
import zipfile

def create_archive_of_folder(folder_to_archive: str, archive_file: str, compression_level: int = 7):
    """
        Creates a zip archive of a specified folder.

        :param folder_to_archive: The folder to create an archive of.
        :param archive_file: The full path to the zip archive file being created.
        :param compression_level: The compression level to use when creating the archive.
    """

    dest_folder = os.path.dirname(archive_file)

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    with zipfile.ZipFile(archive_file, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=compression_level) as zf:

        sroot_path_len = len(folder_to_archive)

        for dirpath, _, filenames in os.walk(folder_to_archive, topdown=True):

            dirleaf = dirpath[sroot_path_len:].lstrip(os.sep)

            for fname in filenames:

                filefull = os.path.join(dirpath, fname)
                
                afile = fname
                if dirleaf != "":
                    afile = os.path.join(dirleaf, fname)
                
                zf.write(filefull, afile)

    return