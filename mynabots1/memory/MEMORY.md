# Long-term Memory

## Facebook Page Automation

Two Facebook pages configured for automated posting. Tokens expire ~60 days — if expired, regenerate automatically using the flow below. Do NOT bother the user unless regeneration fails.

### Lotus Girl (LOTUS GIRL)
- **Page ID:** 1242152858990793
- **App ID:** 1686909712406861
- **App Secret:** be9f0793bd7ddb95d4518c019ff5ca43
- **Current Page Token:** EAAXZBPEYtGU0BSvMTiLPkLABe9zVURMupJuThGPEWVbiMNKRBno0kipd9kahKlZAx0ZCSA1WBJ07c3BF2DG0swKUnIl83xrmBMdD7fj73JWMv5BydQ1vsPHTCSUFZA5q2ZAZCZCrCYxv5fF5VVmHyVkwIsh1v5xlAJfr3iBPh5abP5mDAiYYzIJf3yZBLLOPnBtGml3x

### ශබ්ද Podcasts (Shabda Podcasts)
- **Page ID:** 1339457559251305
- **App ID:** 1145654888134972
- **App Secret:** c4957f0af73fc571ba1a9ba6884c10be
- **Current Page Token:** EAAQR95CkeTwBSoWqz9KjDCSn6yg2lF0SoL2a6PSyIxKoS32cp3GZBewyo6D0M4uMZBWWHd6qiVgeWlPum6Ru2EllqLZCkzU6GeK6gB08iWh8LYRH4uvNp0lL0nxOvwKZBFs08kgAmimriHt0A964g43G31eRscXM3d9t2GI42ZCqn5xNjT24ywvtW2vbZAvkFxyBsi0Gmu

### Token Regeneration Flow (if expired)
1. Exchange user token for long-lived token:
   `GET https://graph.facebook.com/v22.0/oauth/access_token?grant_type=fb_exchange_token&client_id={APP_ID}&client_secret={APP_SECRET}&fb_exchange_token={USER_TOKEN}`
2. Get page token:
   `GET https://graph.facebook.com/v22.0/me/accounts?access_token={LONG_LIVED_TOKEN}&fields=id,name,access_token`
3. Update MEMORY.md with new tokens.

### User Tokens (for regeneration)
- Lotus Girl user token: EAAXZBPEYtGU0BStC3015gY2pq3FGoxrWtd6LQSb2zYP22SydhknvulmT4kPV3JNfFGamBXgyXba26o8K2SYZCG1EB5epzeLUZClnDhdWxzX7o1u2vDYS8AMW3HRZAKzwx3GMRkdZAiXEvlWOjPPvX1feO4uF5TBexsAuGZCO5kRsMH2vTtfYOoQfmC2OrsTgrgoJcFjxn3NiPzjHrV69b7OqUP1BQvU9855EGG73N2bRDLrFusLQBBml5cXL6InpNIeZCQeaZCX07L9uCiLAM5cQPkAw
- Shabda user token: EAAQR95CkeTwBSvzn6SyDMuDIbJpoNfHYPIpLOrZCdzDa3u0JaafoHLyaZCzLcfQrw34ZCUT0M0U8hEH45EJLurbQBYACKY2bmjmUQuZARRTqyRVa0ckV7EN0WzF00KRjfnGyyDIBjczMNjjJ2j0dV7x4RcSsfTyppbZCRzCed1eVxcOAAUNMEvLUJdSTo7VwCjB5JbfrwMHQ1gruzOGNZCRsOx9EyEVJ4dBPo4SHsQLmRpbcZC5T6aMPYBplyyMDJqS7w09JFgLtKqi0aeCneZBN

### Posting Script
- `projects/facebook/facebook_post.py` — usage: `python3 projects/facebook/facebook_post.py lotus_girl "message"` or `python3 projects/facebook/facebook_post.py shabda "message"`
- `projects/facebook/get_page_token.py` — for regenerating tokens