import sys
import json
import hashlib
import time
from datetime import datetime as dt

PACKAGE=sys.argv[1]
VERSION=sys.argv[2]
DOWNLOAD_SHA256=sys.argv[3]
DOWNLOAD_SIZE=sys.argv[4]
DOWNLOAD_URL=sys.argv[5]
INSTALL_SIZE=sys.argv[6]

with open("packages.json", "r+") as f:
    data = json.load(f)
    info = {
          "version": VERSION,
          "status": "testing",
          "kicad_version": "7.0",
          "download_sha256": DOWNLOAD_SHA256,
          "download_size": int(DOWNLOAD_SIZE),
          "download_url": DOWNLOAD_URL, 
          "install_size": int(INSTALL_SIZE)
    }
    package_index = next((i for i, e in enumerate(data["packages"]) if e["identifier"] == PACKAGE), None)
    if package_index is None:
        raise Exception("package not found")
    index = None
    for i, version in enumerate(data["packages"][package_index]["versions"]):
        if version["version"] == VERSION:
            index = i
            break
    if index is not None:
        data["packages"][package_index]["versions"][index] = info
    else:
        data["packages"][package_index]["versions"].append(info)
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

with open("packages.json", "rb") as f:
    bytes = f.read()
    PACKAGES_SHA256 = hashlib.sha256(bytes).hexdigest();

with open("repository.json", "r+") as f:
    data = json.load(f)
    date = dt.utcnow()
    data["packages"]["sha256"] = PACKAGES_SHA256
    data["packages"]["update_time_utc"] = date.strftime("%Y-%m-%d %H:%M:%S") 
    data["packages"]["update_timestamp"] = int(time.mktime(date.timetuple()))
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()


