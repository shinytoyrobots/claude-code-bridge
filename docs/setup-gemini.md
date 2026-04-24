# Gemini Setup Guide

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- [LiteLLM](https://docs.litellm.ai/) installed: `pip install 'litellm[proxy]'`
- A Google Gemini API key from [aistudio.google.com](https://aistudio.google.com/app/apikey)

## API key setup

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and generate an API key
2. Export it in your shell:

```bash
export GEMINI_API_KEY="your-key-here"
```

Add this to your `~/.zshrc` or `~/.bashrc` to persist across sessions.

## Install

```bash
git clone https://github.com/shinytoyrobots/claude-code-bridge.git
cd claude-code-bridge
./install.sh --providers gemini
```

Or install all providers at once with `./install.sh`.

## First run

```bash
claude-gemini
```

This starts the LiteLLM proxy, exports the correct environment variables, and launches Claude Code. To verify:

```bash
claude-gemini -p "What model are you? Reply with just your model name."
```

## Tier mapping

| Claude Code tier | Gemini model | Use case |
|------------------|-------------|----------|
| `opus` | gemini-2.5-pro | Flagship — best quality, 1M+ token context |
| `sonnet` | gemini-2.5-flash | Workhorse — fast, capable |
| `haiku` | gemini-2.5-flash | Cheap — same as Sonnet (Gemini has two tiers) |

Sonnet and Haiku both map to `gemini-2.5-flash` because Gemini has two meaningful tiers. To override: edit `providers/gemini.yaml`. See [tier mapping](tier-mapping.md) for details.

## Why Gemini?

Gemini's primary differentiator is the **long context window** — Gemini 2.5 Pro supports 1M+ tokens. This makes it especially useful for:

- **Research-heavy skills** that process large documents or codebases in a single pass
- **Codebase analysis** across many files simultaneously
- **Long conversation sessions** that would exceed other models' context limits

If your workflow involves large context, Gemini is the strongest choice for the Opus tier.

## Known limitations

- **Validated end-to-end**: Gemini provider has been tested with the ASGI middleware (schema fixing, tool stripping, thinking override).
- **Two-tier mapping**: Like DeepSeek, Gemini has two meaningful tiers rather than three. Sonnet and Haiku collapse to the same model.
- **Extended thinking**: Gemini models do not support Claude's extended thinking. Skills relying on `thinking` blocks will degrade gracefully.
- **Parallel subagents**: Non-Claude models handle sequential subagent orchestration more reliably. The SessionStart hook advises sequential launches.

## Troubleshooting

See the [troubleshooting guide](troubleshooting.md) for common issues.
