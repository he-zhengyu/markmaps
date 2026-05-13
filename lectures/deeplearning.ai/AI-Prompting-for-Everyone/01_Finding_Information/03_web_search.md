---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Web Search in AI Models

## Knowledge Cutoff Problem
- 🔑 **Knowledge cutoff** — frozen "last date" of training data
- AI reads internet **only up to** that date
- World keeps moving after cutoff
  - New events, movies, memes, products
- Pretrained knowledge ≠ current reality

## The 6-7 Meme Example
- Pronounced *"six seveeen"*
- Viral internet slang on social media (2025)
- Why AI misses it
  - Long-standing knowledge: `6 × 7 = 42`
  - Old joke: *"Why was 6 afraid of 7? Because 7-8-9"*
  - 📌 Meme emerged **after** cutoff
- Trigger word: **"2025"** signals need for fresh info
- 📊 GPT-5.4 cutoff: **August 2025**
  - Google searches for *"what does 6 7 mean"* spiked after cutoff

## When AI Uses Pretrained Knowledge
- ✅ Common, stable knowledge questions
  - *"What to do if you drop your phone in soup?"*
  - *"Why do cats stare at walls?"*
  - *"What was on the Voyager 1 record?"*
- 💡 Topics widely represented online before cutoff

## When AI Triggers Web Search
- **Current events / recent happenings**
  - Real-time information needed
- **Location-specific queries**
  - *"Highly rated gym near Mountain View, CA"*
  - Ratings, hours, openings change over time
- **Niche / obscure topics**
  - *"What is the Marquette Mountain Cheese Roll?"*
    - AI-added: likely confusion with *Cooper's Hill Cheese-Rolling* (UK), where people chase a wheel of cheese downhill
- **Date-cued questions** (e.g. *"...from 2025"*)

## How Web Search Gets Triggered
- **Automatic**
  - Model self-decides based on question
- **Explicit / manual**
  - 🖱️ Click web search button in UI
  - ✍️ Prompt: *"Please do a web search for..."*
- ⚠️ Not all AI models support web search
  - Most popular ones do (ChatGPT, Gemini, Claude)

## Benefits & Caveats
- ✅ Augments pretrained knowledge with current info
- ✅ Better answers on many real-world tasks
- ⚠️ Can return **bad or unreliable sources**
- 📌 Source quality matters — covered next lesson

## Key Takeaways
- 🔑 Every AI model has a **knowledge cutoff** — anything after is invisible to pretrained memory
- 💡 Web search **augments** (not replaces) pretrained knowledge for fresh, local, or niche queries
- 📌 You can trigger search **automatically** or **explicitly** via prompt/button
- ⚠️ Web search ≠ truth — always consider **source reliability**
- ✅ Use search for: current events, location info, niche topics, post-cutoff references