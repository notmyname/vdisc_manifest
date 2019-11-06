#!/usr/bin/env python3.7

"""
given a container name, build a vdisc csv manifest for every object
 * use the swiftclient sdk service module for this

eventually, allow passing in same parameters as swiftclient for listing filters
"""

import sys
from urllib.parse import quote
import string
import re

from swiftclient import service

vdisc_csv_template = '"%s","%s",%d'

good_chars = string.ascii_letters + string.digits + "/" + "-" + "_" + "."

svc = service.SwiftService()  # will pull auth creds from env vars
c = service.get_conn(svc._options)
storage_url = c.get_auth()[0].replace("https", "swift").replace("http", "swift")
storage_url = storage_url[: storage_url.index("/v1")]
for container in sys.argv[1:]:
    l = svc.list(container=container)
    for result in l:
        for item in result["listing"]:
            clean_name = re.sub("[^a-zA-Z0-9/_.-]", "-", item["name"])
            local_name = "/%s/%s" % (container, clean_name)
            local_name = local_name.replace(" ", "_")
            url = "%s/%s/%s/%s" % (storage_url, c.user, container, quote(item["name"]))
            print(vdisc_csv_template % (local_name, url, item["bytes"]))
