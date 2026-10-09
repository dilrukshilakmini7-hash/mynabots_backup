#!/usr/bin/env python3
"""
Facebook Page Access Token retrieval script.
Run: python3 get_page_token.py --app-id <APP_ID> --app-secret <APP_SECRET> [--redirect-uri <URI>]
"""

import argparse
import json
import secrets
import sys
import urllib.parse
import urllib.request
import urllib.error
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler


REDIRECT_URI_DEFAULT = "http://localhost:8080"
SCOPES = "pages_manage_posts,pages_read_user_content,pages_show_list"


class OAuthHandler(BaseHTTPRequestHandler):
    """Catch the OAuth redirect and extract the auth code."""
    auth_code = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            OAuthHandler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Authorization received!</h1><p>You can close this window.</p></body></html>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code parameter.")

    def log_message(self, format, *args):
        pass  # silence logs


def exchange_code_for_token(app_id, app_secret, code, redirect_uri):
    """Exchange authorization code for a short-lived user access token."""
    url = (
        f"https://graph.facebook.com/v22.0/oauth/access_token"
        f"?client_id={app_id}"
        f"&redirect_uri={urllib.parse.quote(redirect_uri)}"
        f"&client_secret={app_secret}"
        f"&code={code}"
    )
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def get_page_access_token(user_token):
    """Call /me/accounts to get page access tokens."""
    url = (
        f"https://graph.facebook.com/v22.0/me/accounts"
        f"?access_token={urllib.parse.quote(user_token)}"
        f"&fields=id,name,access_token"
    )
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def main():
    parser = argparse.ArgumentParser(description="Get Facebook Page Access Token")
    parser.add_argument("--app-id", required=True)
    parser.add_argument("--app-secret", required=True)
    parser.add_argument("--redirect-uri", default=REDIRECT_URI_DEFAULT)
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    state = secrets.token_urlsafe(16)

    # Build OAuth URL
    auth_url = (
        f"https://www.facebook.com/v22.0/dialog/oauth"
        f"?client_id={args.app_id}"
        f"&redirect_uri={urllib.parse.quote(args.redirect_uri)}"
        f"&state={state}"
        f"&scope={urllib.parse.quote(SCOPES)}"
        f"&response_type=code"
    )

    print("\n" + "=" * 60)
    print("  Step 1: Open this URL in your browser to authorize:")
    print(f"  {auth_url}")
    print("=" * 60)
    print()

    # Try to open browser automatically
    try:
        webbrowser.open(auth_url)
        print("  → Browser opened automatically.")
    except Exception:
        print("  → Could not open browser. Please copy the URL above.")

    print("\n  Step 2: A local server will start on port", args.port)
    print("  Step 3: After authorization, the script will capture the code.\n")

    # Start local server
    server = HTTPServer(("localhost", args.port), OAuthHandler)
    server.handle_request()  # blocks until one request comes in

    if not OAuthHandler.auth_code:
        print("ERROR: No authorization code received.", file=sys.stderr)
        sys.exit(1)

    code = OAuthHandler.auth_code
    print(f"\n  → Got authorization code: {code[:20]}...")

    # Exchange code for user token
    print("\n  Exchanging code for user access token...")
    token_data = exchange_code_for_token(
        args.app_id, args.app_secret, code, args.redirect_uri
    )
    user_token = token_data.get("access_token")
    if not user_token:
        print("ERROR: No access token in response:", json.dumps(token_data, indent=2), file=sys.stderr)
        sys.exit(1)
    print(f"  → User token obtained ({len(user_token)} chars)")

    # Get page tokens
    print("\n  Fetching page access tokens...")
    pages_data = get_page_access_token(user_token)
    pages = pages_data.get("data", [])

    if not pages:
        print("ERROR: No pages found. Make sure your Facebook account has page admin access.", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  PAGE ACCESS TOKENS (save these!):")
    print("=" * 60)
    for page in pages:
        print(f"\n  Page: {page.get('name')}")
        print(f"  Page ID: {page.get('id')}")
        print(f"  Access Token:\n  {page.get('access_token')}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()