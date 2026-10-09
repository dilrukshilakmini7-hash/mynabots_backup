#!/usr/bin/env python3
"""
Facebook Page Poster — reusable script for LOTUS GIRL and ශබ්ද Podcasts.
Usage:
  python3 facebook_post.py lotus_girl "Your message here"
  python3 facebook_post.py shabda "Your message here"
"""

import sys
import urllib.request
import urllib.parse
import json

PAGES = {
    "lotus_girl": {
        "page_id": "1242152858990793",
        "access_token": "EAAXZBPEYtGU0BSvMTiLPkLABe9zVURMupJuThGPEWVbiMNKRBno0kipd9kahKlZAx0ZCSA1WBJ07c3BF2DG0swKUnIl83xrmBMdD7fj73JWMv5BydQ1vsPHTCSUFZA5q2ZAZCZCrCYxv5fF5VVmHyVkwIsh1v5xlAJfr3iBPh5abP5mDAiYYzIJf3yZBLLOPnBtGml3x",
        "name": "LOTUS GIRL",
    },
    "shabda": {
        "page_id": "1339457559251305",
        "access_token": "EAAQR95CkeTwBSoWqz9KjDCSn6yg2lF0SoL2a6PSyIxKoS32cp3GZBewyo6D0M4uMZBWWHd6qiVgeWlPum6Ru2EllqLZCkzU6GeK6gB08iWh8LYRH4uvNp0lL0nxOvwKZBFs08kgAmimriHt0A964g43G31eRscXM3d9t2GI42ZCqn5xNjT24ywvtW2vbZAvkFxyBsi0Gmu",
        "name": "ශබ්ද Podcasts",
    },
}


def post(page_key, message):
    page = PAGES[page_key]
    data = urllib.parse.urlencode({"message": message}).encode()
    url = f"https://graph.facebook.com/v22.0/{page['page_id']}/feed?access_token={page['access_token']}"

    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read().decode())
        post_id = result.get("id", "unknown")
        print(f"✅ Posted to {page['name']}!")
        print(f"   Post ID: {post_id}")
        print(f"   View: https://www.facebook.com/{post_id}")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ Error posting to {page['name']}: HTTP {e.code}")
        print(f"   Response: {body[:300]}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 facebook_post.py <page> <message>")
        print("Pages:", ", ".join(PAGES.keys()))
        sys.exit(1)

    page_key = sys.argv[1].lower()
    message = " ".join(sys.argv[2:])

    if page_key not in PAGES:
        print(f"Unknown page '{page_key}'. Available: {', '.join(PAGES.keys())}")
        sys.exit(1)

    post(page_key, message)