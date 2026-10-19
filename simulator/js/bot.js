const FAQ = {
  shipping: "Standard shipping: 5–8 business days in the EU. Express: 2–4 days.",
  returns: "Unused items can be returned within 30 days in original packaging.",
  pricing: "Starter $40–90 · Growth $120–250 · Automation $250–500. Crypto OK.",
  hours: "Support Mon–Fri 09:00–18:00 Europe/Madrid.",
};
const HELP =
  "Nyyo demo bot commands:\n/start — welcome\n/help — this list\n/faq <topic> — shipping | returns | pricing | hours\n/price btc|eth|sol — demo USD price\n/clean — spreadsheet cleanup pitch";

async function handleMessage(text) {
  const low = (text || "").trim().toLowerCase();
  if (low.startsWith("/start")) {
    return "Hi — this is a Nyyo Automation demo bot.\nAsk /faq shipping or /price btc.\nHire: https://laborx.com/freelancers/users/id475124";
  }
  if (low.startsWith("/help")) return HELP;
  if (low.startsWith("/faq")) {
    const topic = low.split(/\s+/)[1] || "";
    return FAQ[topic] || "Try: /faq shipping | returns | pricing | hours";
  }
  if (low.startsWith("/price")) {
    const coin = (low.split(/\s+/)[1] || "btc");
    const map = { btc: "bitcoin", eth: "ethereum", sol: "solana", bitcoin: "bitcoin", ethereum: "ethereum", solana: "solana" };
    const id = map[coin] || "bitcoin";
    try {
      const res = await fetch("https://api.coingecko.com/api/v3/simple/price?ids=" + id + "&vs_currencies=usd");
      const raw = await res.json();
      return id + ": $" + raw[id].usd + " USD (public demo data — not advice)";
    } catch (e) {
      return "Price fetch failed (network). Try /faq pricing instead.";
    }
  }
  if (low.startsWith("/clean")) {
    return "Spreadsheet cleanup package: dedupe, fix types, fill gaps, summary dashboard. From $35. Send your sheet for a free 100-row sample.";
  }
  return "Unknown command. Try /help";
}

window.NyyoDemoBot = { handleMessage };
