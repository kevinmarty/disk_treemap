# -*- encoding: utf-8 -*-
import tarfile
import zipfile

from tqdm import tqdm


def scan_tarfile(archive_path):
    with tarfile.open(archive_path) as archive:
        for member in archive.getmembers():
            if member.isfile():
                yield member.name, member.size


def scan_zipfile(archive_path):
    with zipfile.ZipFile(archive_path) as archive:
        for member in archive.infolist():
            if not member.is_dir():
                yield member.filename, member.file_size


def scan_size_tree(archive_path):
    size_tree = dict()
    if tarfile.is_tarfile(archive_path):
        scanfunc = scan_tarfile
    elif zipfile.is_zipfile(archive_path):
        scanfunc = scan_zipfile

    for path, size in tqdm(scanfunc(archive_path), desc=archive_path):
        *directories, filename = path.lstrip('/').split('/')
        directories.insert(0, archive_path)
        current_size_tree = size_tree
        for directory in directories:
            if directory not in current_size_tree:
                current_size_tree[directory] = dict()
            current_size_tree = current_size_tree[directory]
        current_size_tree[filename] = size
    return size_tree
