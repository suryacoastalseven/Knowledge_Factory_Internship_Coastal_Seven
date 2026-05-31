# Day 1: Introduction to LLMs & AI Ecosystem

## 📌 Concepts Learned & Implemented

### 1. System vs User Prompts (`01_prompt_basics.py`)
- **System Prompt:** Instructs the LLM on its persona, tone, and boundaries (e.g., "You are a helpful assistant").
- **User Prompt:** The actual instruction or question provided by the user.

### 2. Temperature (`02_temperature_test.py`)
- **Low Temperature (0.0 - 0.3):** Makes the output more focused, deterministic, and strict. Best for coding or factual answers.
- **High Temperature (0.7 - 1.0):** Makes the output more creative and random. Best for storytelling or brainstorming.

### 3. Context Windows & Few-Shot Prompting (`03_context_and_few_shot.py`)
- **Context Window:** The maximum amount of text (tokens) an LLM can remember and process in a single request. 
- **Few-Shot Prompting:** Providing a few examples inside the context window before asking the final question. It drastically improves the accuracy of the LLM.

### 4. Tokens
- LLMs don't read words; they read "Tokens" (chunks of characters). 
- Generally, 1 Token ≈ 4 English characters. 
- API pricing and Context Windows are strictly measured in tokens.