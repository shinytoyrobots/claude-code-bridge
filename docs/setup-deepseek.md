# DeepSeek Setup Guide

> **Recommended for first-time users.** DeepSeek is the most-validated provider path — the author ran complex multi-agent skills (including `/dr-research`) end-to-end against DeepSeek V4 Pro before building this kit.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- [LiteLLM](https://docs.litellm.ai/) installed: `pip install 'litellm[proxy]'`
- A DeepSeek API key from [platform.deepseek.com](https://platform.deepseek.com)

## API key setup

1. Sign up at [platform.deepseek.com](https://platform.deepseek.com) and generate an API key
2. Export it in your shell:

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

Add this to your `~/.zshrc` or `~/.bashrc` to persist across sessions.

## Install

```bash
git clone https://github.com/shinytoyrobots/claude-code-bridge.git
cd claude-code-bridge
./install.sh --providers deepseek
```

Or install all providers at once with `./install.sh`.

## First run

```bash
claude-deepseek
```

This starts the LiteLLM proxy (if not already running), exports the correct environment variables, and launches Claude Code. To verify the right model is answering:

```bash
claude-deepseek -p "What model are you? Reply with just your model name."
```

You should see a response identifying a DeepSeek model.

## Tier mapping

| Claude Code tier | DeepSeek model | Use case |
|------------------|----------------|----------|
| `opus` | deepseek-v4-pro | Flagship — complex reasoning, multi-step tasks |
| `sonnet` | deepseek-v4-flash | Workhorse — routine tasks, fast responses |
| `haiku` | deepseek-v4-flash | Cheap — same as Sonnet (DeepSeek has two tiers) |

Sonnet and Haiku both map to `deepseek-v4-flash` because DeepSeek V4 has two meaningful tiers. Using `v4-pro` for the Sonnet slot would roughly double the cost of most skill calls without meaningful quality improvement for routine work.

To override: edit `providers/deepseek.yaml` and change the `model_name` alias mappings. See [tier mapping](tier-mapping.md) for details.

## Additional models

The config also includes raw model names for direct use:

- `deepseek-chat` — general-purpose chat model
- `deepseek-reasoner` — reasoning-focused model

These are accessible when explicitly requested but not part of the tier mapping.

## Known limitations

- **Validated end-to-end**: This is the most-tested path. No known issues with standard skill execution.
- **Extended thinking**: DeepSeek models do not support Claude's extended thinking feature. Skills that rely on `thinking` blocks will degrade gracefully (the model simply skips them).
- **Parallel subagents**: Non-Claude models handle sequential subagent orchestration more reliably than parallel. The SessionStart hook advises the model to prefer sequential launches.

## Troubleshooting

See the [troubleshooting guide](troubleshooting.md) for common issues.
