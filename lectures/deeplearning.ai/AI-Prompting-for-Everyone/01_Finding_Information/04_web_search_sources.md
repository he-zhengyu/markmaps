---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Web Search Sources

## The Source Quality Problem
- **Web search is valuable but imperfect**
  - Just like manual searching, it may miss the mark
  - ⚠️ Limitations: outdated or inaccurate sources
- 💡 You can **steer the model** to work around these limits

## Example: "How safe are green market peptides?"
- **Without steering**
  - Pulls from social media, **Reddit**, **Quora**
  - ⚠️ May find peptide sellers (biased toward "safe")
  - Answers may or may not be accurate
- **With steering toward authoritative sources**
  - ✅ World Health Organization (**WHO**)
  - ✅ US Food and Drug Administration (**FDA**)
  - ✅ European Medicines Agency (**EMA**)
  - 💡 More reliable, scientifically credible answers

## Why Models Drift to Popular Sources
- 📊 Most-cited websites by AI models
  - **Reddit** (#1)
  - **Wikipedia**
  - **YouTube**
  - **Google**
  - **Yelp**
- **Root cause: volume vs. reliability**
  - Vast text from social media, blogs, forums
  - Much smaller pool of rigorous scientific text
- ⚠️ Without steering → model pulls what's *most available*, not *most reliable*

## Outdated Pages Pitfall
- AI may cite pages that are no longer current
- **Example:** "Places to run in Henderson, Nevada"
  - Pulled from a web page **20+ years old**
  - Suggested a school no longer open to public runners
- 📌 Always sanity-check time-sensitive results

## How AI Web Search Works Under the Hood
- 🔑 **Two-model customer service team**
  - **User-facing AI model** — what you talk to
  - **Assistant AI model** — does the searching
- **Step-by-step flow**
  - You send prompt to user-facing model
  - It calls assistant model to search
  - Assistant queries a search engine (Google/Bing-like)
  - Scans and **filters** results
  - **Downloads** most relevant pages
  - **Summarizes** them
  - Returns summaries to user-facing model
  - User-facing model generates your final answer
- ⚠️ **Key quirk**
  - User-facing model only sees **summaries**, not full pages
  - 💡 Can misinterpret what a cited page actually says
  - Why AI sometimes cites pages that don't support its claim

## Worked Example: "Hiking Machu Picchu"
- Assistant model issues queries like
  - `Machu Picchu permits`
  - `Machu Picchu weather`
  - `Machu Picchu social customs`
- Filters and summarizes top results
- User-facing model synthesizes the final answer

## When to Use Search Engine vs. AI Model
### ✅ Use a **web search engine** when
- Quickly scanning multiple sources
- Navigating to a specific site you can't recall
- Looking at data in its **original form**
  - e.g., buying a 2013 Honda Civic air filter

### ✅ Use an **AI model** when
- You want a **synthesis** across sources
- Weighing complex **pros and cons**
- Contrasting multiple sources for a thoughtful conclusion
- 💡 Saves time vs. reading many pages yourself

## Good Habits Carry Over
- ✅ Prefer reliable sources
- ✅ Double-check the sources cited
- 📌 Same instincts apply to AI search as to Google search

## Beyond Basic Web Search
- AI can do **Deep Research** — far more extensive
- 💡 A powerful, underused capability
- *(Covered in the next lesson)*

## Key Takeaways
- 💡 **Steer the sources**: tell the AI to use official/scientific sources for credible answers
- ⚠️ AI defaults to **popular** sources (Reddit, Wikipedia, YouTube), not necessarily reliable ones
- ⚠️ Web pages can be **outdated** — verify time-sensitive info
- 🔑 AI search uses a **two-model pipeline**; the user-facing model reads only **summaries**, which can cause misattribution
- ✅ **Search engine** for scanning, navigation, raw data; **AI model** for synthesis and weighing trade-offs
- 📌 Bring your existing **good search habits** — prefer and verify reliable sources