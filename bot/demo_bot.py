#!/usr/bin/env python3
"""
Nyyo Automation — Telegram demo bot (FAQ + fake price helper).

Requires env TELEGRAM_BOT_TOKEN from @BotFather (client-owned token).
This repo does NOT ship a live token. Use simulator/ for a no-Telegram tryout.

  export TELEGRAM_BOT_TOKEN=...
  pip install -r requirements.txt
  python bot/demo_bot.py
"""
from __future__ import annotations

import os
import json
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlencode

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
API = f"https://api.telegram.org/bot{TOKEN}" if TOKEN else ""

FAQ = {
    "shipping": "Standard shipping: 5–8 business days in the EU. Express: 2–4 days.",
    "returns": "Unused items can be returned within 30 days in original packaging.",
    "pricing": "Chatbots from $149 · spreadsheet cleanup from $45 · n8n automations from $149. Available on LaborX.",
    "hours": "Support Mon–Fri 09:00–18:00 UTC.",
}

HELP = (
    "Nyyo demo bot commands:\n"
    "/start — welcome\n"
    "/help — this list\n"
    "/faq <topic> — shipping | returns | pricing | hours\n"
    "/price btc|eth|sol — public USD price (demo)\n"
    "/clean — what spreadsheet cleanup includes\n"
)


def api(method: str, **params):
    data = urlencode(params).encode()
    req = urllib.request.Request(f"{API}/{method}", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def handle_message(text: str) -> str:
    text = (text or "").strip()
    low = text.lower()
    if low.startswith("/start"):
        return (
            "Hi — this is a **Nyyo Automation** demo bot.\n"
            "Ask /faq shipping or /price btc.\n"
            "Available on LaborX: https://github.com/nyyoautomation"
        )
    if low.startswith("/help"):
        return HELP
    if low.startswith("/faq"):
        parts = low.split(maxsplit=1)
        topic = parts[1].strip() if len(parts) > 1 else ""
        if topic in FAQ:
            return FAQ[topic]
        return "Try: /faq shipping | returns | pricing | hours"
    if low.startswith("/price"):
        parts = low.split()
        coin = parts[1] if len(parts) > 1 else "bitcoin"
        mapping = {"btc": "bitcoin", "eth": "ethereum", "sol": "solana",
                   "bitcoin": "bitcoin", "ethereum": "ethereum", "solana": "solana"}
        cid = mapping.get(coin, "bitcoin")
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={cid}&vs_currencies=usd"
        req = urllib.request.Request(url, headers={"User-Agent": "NyyoDemoBot/1.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = json.load(r)
        price = raw[cid]["usd"]
        return f"{cid}: ${price} USD (public demo data — not advice)"
    if low.startswith("/clean"):
        return (
            "Spreadsheet cleanup package: dedupe, fix types, fill gaps, "
            "summary dashboard. From $45. Send your sheet to get started."
        )
    return "Unknown command. Try /help"


def poll_loop():
    if not TOKEN:
        raise SystemExit("Set TELEGRAM_BOT_TOKEN (from @BotFather). Or open simulator/index.html")
    offset = 0
    print("Nyyo demo bot polling…")
    while True:
        updates = api("getUpdates", offset=offset, timeout=30)
        for u in updates.get("result", []):
            offset = u["update_id"] + 1
            msg = u.get("message") or {}
            chat = msg.get("chat") or {}
            text = msg.get("text") or ""
            chat_id = chat.get("id")
            if not chat_id:
                continue
            reply = handle_message(text)
            api("sendMessage", chat_id=chat_id, text=reply)


if __name__ == "__main__":
    poll_loop()
