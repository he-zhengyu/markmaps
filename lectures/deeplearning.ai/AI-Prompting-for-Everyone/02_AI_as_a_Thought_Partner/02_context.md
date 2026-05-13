---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# AI Context

## Human vs AI Memory
- **Human working memory**
  - 📊 ~7 items at a time
  - Grocery list of 7 → barely doable
  - Grocery list of 15–20 → very hard
- **AI context capacity**
  - Hundreds of thousands of words
  - 📊 Up to ~750,000 words in leading models
  - ≈ First 4–5 Harry Potter books
  - ≈ Several days of continuous speech
  - 💡 People underestimate how much you can give

## What Is Context?
- 🔑 **Context** = all text & files the model uses to generate a response
- Shapes how custom and high-quality the output is
- **Sparse prompt** → generic answer
  - *e.g.* "Pros and cons of physics vs zoology"
- **Rich prompt** → tailored answer
  - Add career assessment results
  - Add high school schedule
- 💡 **Trusted advisor test**
  - What info would a smart advisor need to reason well and answer you?

## What Fills the Context
- **System prompt** *(built-in)*
  - Current date
  - Model name & basic capabilities
  - General instructions to be helpful
- **Tool definitions**
  - Descriptions of available tools
  - *e.g.* how to use web search
- **User prompt**
  - Your written question
  - Uploaded files & documents
- **Chat history**
  - Prior prompts + AI responses
  - 📌 Incrementally added every turn
  - Why the AI "remembers" earlier turns

## Example: Apartment Choice
- Upload hundreds of pages of lease contracts
- Upload tenant reviews
- Upload neighborhood statistics
- Prompt: *"Pros and cons of each apartment, read everything, and think really hard"*
  - 💡 "Think hard" / "think really hard" is a common prompting pattern

## Managing Context Well
- ✅ More context is usually better
- ✅ Relevant context is better
- ⚠️ Irrelevant context can distract the model
  - May degrade answer quality
  - Hard to tell if prior context biased the response
- ✅ Upload supporting files when useful
- 📌 **Switch topics → start a new conversation**
  - *e.g.* Your workout plan → Mom's workout plan
  - Empties stale context
  - Keeps only relevant info
- 💡 Models tolerate *some* irrelevant context, but don't overload

## Extending Context Further
- Let AI access your computer
- Pulls relevant files into context **only as needed**
- Handles loss of context gracefully
- 📌 Covered in the next video

## Key Takeaways
- 🔑 **Context** = everything the model sees: system prompt, tools, your prompt, uploads, chat history
- 📊 Modern models accept up to **~750,000 words** of context
- 💡 More *relevant* context → more custom, higher-quality answers
- ⚠️ More *irrelevant* context → distraction and worse answers
- ✅ **Start a new chat** when switching to an unrelated topic
- 📌 Ask yourself: *"What would a trusted advisor need to know?"*