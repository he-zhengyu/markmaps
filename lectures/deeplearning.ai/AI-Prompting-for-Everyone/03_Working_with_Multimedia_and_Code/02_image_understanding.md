---
markmap:
  initialExpandLevel: -1
  maxWidth: 0
  colorFreezeLevel: 3
---

# Image Understanding with AI

## Why Add Images to Prompts
- 💡 *A picture is worth a thousand words*
- Enriches **context** for the AI
- Fastest way to convey complex info
- Use cases
  - Things hard to describe in words
  - Handwritten text
  - Visual scenes / objects
  - Brainstorm artifacts

## What AI Can See Well
- **Coarse, high-level interpretation**
  - Identifies overall scene
  - Recognizes distinct objects
- **Context inference**
  - Example: whiteboard photo
    - Detects `convolutional neural network`
    - Works even when word is *partially blocked*
  - Extracts drawn concepts
  - Guesses likely next steps
- **Visually distinct objects**
  - Example: human-sized hamster wheel treadmill
  - ✅ Good for generating sales ads
- **Text reading (OCR)**
  - Printed text on receipts
  - 📌 Decent but not perfect
  - ⚠️ Avoid for high-stakes use
  - Always double-check output
- **Handwritten text**
  - Transcribes cursive reasonably well
  - Example use: *archive family history from letters*
  - ⚠️ Won't be 100% accurate

## Where AI Struggles
- ⚠️ **Fine-grained details**
  - Sees images in a *coarse* way
  - Misses subtle distinguishing features
- **Visually similar objects**
  - Example: gym machines
    - Glute kickback vs hamstring curl
    - ❌ Often confidently wrong
- 📌 Confidence ≠ correctness

## Working with Multiple Images
- Upload **many images at once**
- Use cases
  - Brainstorming session recap
    - 📝 Notes
    - 🗒️ Post-it notes
    - 📋 Whiteboard photos
  - Ask AI to summarize ideas
- ✅ Accelerates note-taking
- ⚠️ Verify the summary

## Practical Examples
- **Whiteboard lecture photo**
  - Prompt: *what is this class about?*
  - Output: identifies AI technique taught
- **Gym machine photo**
  - Prompt: *what are these machines?*
  - ❌ Likely incorrect identification
- **Receipt photo**
  - Prompt: *what's my portion of the bill?*
  - Lists items → computes share
- **Handwritten letters**
  - Prompt: *build an archive of family history*
- **Brainstorm artifacts**
  - Prompt: *summarize today's meeting*

## Tips for Better Results
- 📌 Provide **clear, well-lit** images
- Give moderately complex instructions
- Combine images with text prompts
- Double-check extracted text & numbers
- ⚠️ Don't rely on AI for high-stakes reading

## Beyond Understanding
- AI can also **generate images**
- Works *differently* from text generation
- ➡️ Covered in the next lesson

## Key Takeaways
- 💡 Images give AI **rich context** fast — often faster than words
- ✅ AI is strong at **coarse scenes**, **distinct objects**, and **basic OCR**
- ⚠️ AI is weak at **fine-grained visual distinctions** (e.g., similar machines)
- 📌 Always **verify** transcriptions and summaries before trusting them
- 🔑 Use **multiple images** to give richer context for tasks like meeting recaps
- 💡 Great everyday uses: *digitize handwritten recipes*, *split a bill*, *summarize a brainstorm*