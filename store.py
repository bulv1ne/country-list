import bz2
import lzma
import zipfile
from contextlib import ExitStack
from pathlib import Path

archives = [
    ("country_list.store.zip", zipfile.ZIP_STORED),
    ("country_list.zip", zipfile.ZIP_DEFLATED),
    ("country_list.bz2.zip", zipfile.ZIP_BZIP2),
    ("country_list.xz.zip", zipfile.ZIP_LZMA),
]


with ExitStack() as stack:
    files = [
        stack.push(bz2.open("country_list.zip.bz2", "wb")),
        stack.push(lzma.open("country_list.zip.xz", "wb")),
    ]
    zip_files = [
        stack.push(zipfile.ZipFile(f, mode="w", compression=zipfile.ZIP_STORED))
        for f in files
    ]
    files = [
        stack.push(bz2.open("country_list.def.zip.bz2", "wb")),
        stack.push(lzma.open("country_list.def.zip.xz", "wb")),
    ]
    zip_files.extend(
        [
            stack.push(zipfile.ZipFile(f, mode="w", compression=zipfile.ZIP_DEFLATED))
            for f in files
        ]
    )
    zip_files.extend(
        [
            stack.push(zipfile.ZipFile(zip_name, mode="w", compression=compression))
            for zip_name, compression in archives
        ]
    )
    for f in Path().glob("country_list/country_data/**/country.csv"):
        archname = f"{f.parent.name}/{f.name}"
        data = f.read_text()
        for zf in zip_files:
            try:
                zf.writestr(archname, data)
            except Exception:
                print(zf)
                raise
