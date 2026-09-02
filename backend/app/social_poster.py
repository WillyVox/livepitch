"""
Posts a short update to social channels whenever event_detector finds a
new goal/card. Each platform is a best-effort, independent call — one
failing should never block the others or the websocket broadcast.

Setup required per platform (do this once, outside this file):

X / Twitter
-----------
1. Apply for a developer account at https://developer.twitter.com
2. Create an app with "Read and Write" permission, generate API key/secret
   and an access token/secret for the account that will post.
3. `pip install tweepy` (already in requirements.txt).

Facebook
--------
1. Create a Facebook App at https://developers.facebook.com
2. Get a Page Access Token for the page you own (via Graph API Explorer,
   or a long-lived token through the standard OAuth flow) with the
   `pages_manage_posts` permission.
3. FACEBOOK_PAGE_ID is the numeric ID of your page.

TikTok
------
TikTok's public Content Posting API is built for *video* uploads, not
text posts — there is no equivalent of a tweet/FB status update. To post
live-score moments to TikTok you would need to render a short video/image
clip (e.g. with Pillow/ffmpeg) for each event and submit it via the
Content Posting API (https://developers.tiktok.com/doc/content-posting-api-get-started),
which requires app review before it works for non-sandbox accounts.
`post_to_tiktok` below is stubbed out with the request shape as a
starting point.
"""
from __future__ import annotations

import logging

import httpx

from app.config import settings

logger = logging.getLogger("social_poster")


def format_event_text(match: dict, event: dict) -> str:
    team = match["home"]["name"] if event["team"] == "home" else match["away"]["name"]
    score = f"{match['home']['score']}-{match['away']['score']}"

    if event["type"] == "goal":
        return f"⚽ GOAL! {event['player']} ({team}) — {match['home']['name']} {score} {match['away']['name']} [{event['minute']}']"
    if event["type"] == "red":
        return f"🟥 RED CARD — {event['player']} ({team}) sent off [{event['minute']}'] | {match['home']['name']} {score} {match['away']['name']}"
    if event["type"] == "yellow":
        return f"🟨 Yellow card — {event['player']} ({team}) [{event['minute']}']"
    return f"Update: {match['home']['name']} {score} {match['away']['name']}"


async def broadcast_to_social(match: dict, event: dict) -> None:
    if not settings.ENABLE_SOCIAL_POSTING:
        return

    text = format_event_text(match, event)

    for fn in (post_to_twitter, post_to_facebook):
        try:
            await fn(text)
        except Exception:
            logger.exception("Social post failed for %s", fn.__name__)


async def post_to_twitter(text: str) -> None:
    import tweepy  # local import so the app runs even if not installed yet

    client = tweepy.Client(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        access_token=settings.TWITTER_ACCESS_TOKEN,
        access_token_secret=settings.TWITTER_ACCESS_SECRET,
    )
    client.create_tweet(text=text[:280])


async def post_to_facebook(text: str) -> None:
    url = f"https://graph.facebook.com/v19.0/{settings.FACEBOOK_PAGE_ID}/feed"
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            url,
            params={
                "message": text,
                "access_token": settings.FACEBOOK_PAGE_ACCESS_TOKEN,
            },
        )
        resp.raise_for_status()


async def post_to_tiktok(video_path: str, caption: str) -> None:
    """
    Stub: TikTok requires an actual video file. A realistic pipeline is
    render_event_clip(match, event) -> mp4 (Pillow/ffmpeg) -> upload here.
    """
    raise NotImplementedError(
        "TikTok posting requires a rendered video clip and an app-reviewed "
        "Content Posting API integration — see module docstring."
    )
