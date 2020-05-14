import gzip
import shutil
from pathlib import Path

data_dir = Path(__file__).parent / "country_data" / "data"
dest_dir = Path(__file__).parent / "country_list" / "country_data" / "data"

if __name__ == "__main__":
    for lang_dir in data_dir.iterdir():
        file_ = lang_dir / "country.csv"

        dest_lang_dir = dest_dir / lang_dir.name
        dest_lang_dir.mkdir(parents=True, exist_ok=True)
        gzip_file = dest_lang_dir / "country.csv.gz"

        if not file_.exists():
            continue
        print("{} -> {}".format(file_, gzip_file))
        with file_.open(mode="rb") as f_in:
            with gzip.open(gzip_file, mode="wb", compresslevel=9) as f_out:
                shutil.copyfileobj(f_in, f_out)
