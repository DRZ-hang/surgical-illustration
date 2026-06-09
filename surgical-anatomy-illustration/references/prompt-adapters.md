# Prompt Adapters

Use the universal prompt as the source of truth. Add only a short adapter for
the target image model.

## Universal

Best for ChatGPT, Gemini, Jimeng, and other image models.

- Keep the medical constraints near the top.
- Keep composition and label instructions explicit.
- Keep the negative prompt attached.
- Include a post-generation review checklist.

## ChatGPT / OpenAI Image Models

- Use direct, declarative instructions.
- Prefer one clear layout instruction over many alternatives.
- Avoid asking for too much long text inside the image.
- Ask for print-ready scientific layout and clean label hierarchy.

## Gemini / Nano Banana

- Emphasize exact panel structure and spatial relationships.
- Repeat critical anatomy constraints when errors would be serious.
- Specify background and label consistency.
- Keep references as abstract guidance, not image copying.

## Jimeng And Chinese Image Models

- Keep the natural-language brief in Chinese when useful.
- Include English anatomical terms for key structures.
- Use concise visual style phrases.
- Avoid relying on small text labels when the model struggles with typography.

## Midjourney-Like Tools

- Compress the visual style phrase.
- Put anatomy constraints before style.
- Use aspect ratio syntax only when the target tool supports it.
- Do not depend on exact label rendering; ask for label-safe blank space when needed.
