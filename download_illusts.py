#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
if sys.version_info >= (3, 0):
    import imp
    imp.reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

from pixivpy3 import *

_REQUESTS_KWARGS = {
  # 'proxies': {
  #   'https': 'http://127.0.0.1:8888',
  # },
  # 'verify': False,       # PAPI use https, an easy way is disable requests SSL verify
}

def main():
    # aapi = AppPixivAPI(**_REQUESTS_KWARGS)
    aapi = AppPixivAPI()
    aapi.login("lkfo415579", "")
    # aapi.login("gm0648", "")

    from_date = datetime.datetime.strptime(sys.argv[1], "%Y%m%d").date()
    TOP = 30
    r = 0
    while(1):
        c_date = from_date.strftime("%Y-%m-%d")
        print ("=" * 100)
        print ("Date : %s" % c_date)
        print ("=" * 100)
        json_result = aapi.illust_ranking('day', date=c_date)

        directory = "dl"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # download top3 day rankings to 'dl' dir
        for i, illust in enumerate(json_result.illusts[:TOP]):
            image_url = illust.meta_single_page.get('original_image_url', illust.image_urls.large)
            print("%d:%s" % (i, illust.title))
            # aapi.download(image_url)

            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1]
            name = "%d_%s%s" % (illust.id, illust.title.replace("/", ""), extension)
            aapi.download(image_url, path=directory, name=name)
        from_date = from_date + datetime.timedelta(days=1)
        r += 1
        if r >= 356:
            break

if __name__ == '__main__':
    main()
