# OpenAI Setup Guide

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- [LiteLLM](https://docs.litellm.ai/) installed: `pip install 'litellm[proxy]==1.63.2'`
- An OpenAI API key from [platform.openai.com](https://platform.openai.com/account/api-keys)

## API key setup

1. Sign up at [platform.openai.com](https://platform.openai.com) and generate an API key
2. Export it in your shell:

```bash
export OPENAI_API_KEY="your-key-here"
```

Add this to your `~/.zshrc` or `~/.bashrc` to persist across sessions.

## Install

```bash
git clone https://github.com/shinytoyrobots/claude-code-provider-kit.git
cd claude-code-provider-kit
./install.sh --providers openai
```

Or install all providers at once with `./install.sh`.

## First run

```bash
claude-openai
```

This starts the LiteLLM proxy, exports the correct environment variables, and launches Claude Code. To verify:

```bash
claude-openai -p "What model are you? Reply with just your model name."
```

## Tier mapping

| Claude Code tier | OpenAI model | Use case |
|------------------|-------------|----------|
| `opus` | gpt-5 | Flagship — highest quality |
| `sonnet` | gpt-5-mini | Workhorse — balanced cost and quality |
| `haiku` | gpt-5-nano | Cheap — fast, lowest cost |

### A note on the Sonnet slot

The Sonnet tier mapping is the most contested choice in the OpenAI lineup. `gpt-5-mini` is a defensible default for general-purpose work, but if your skills are reasoning-heavy (complex multi-step planning, code generation with strict correctness requirements), consider one of these alternatives:

- Swap Opus to `o3` or `o4-mini` and shift `gpt-5` down to Sonnet
- Use `o4-mini` directly for Sonnet-tier tasks

Edit `providers/openai.yaml` to change the mapping. See [tier mapping](tier-mapping.md) for details.

### Model ID verification

The model IDs in this template (`gpt-5`, `gpt-5-mini`, `gpt-5-nano`) were pinned based on available information at the time of release. OpenAI's model naming changes frequently. If you get model-not-found errors on first run:

1. Check [OpenAI's model list](https://platform.openai.com/docs/models) for current IDs
2. Update the `litellm_params.model` values in `providers/openai.yaml`

## Known limitations

- **Validated end-to-end**: OpenAI provider has been tested with the ASGI middleware (schema fixing, tool stripping, thinking override).
- **Sonnet-slot ambiguity**: There is no single right answer for the Sonnet mapping. Benchmark against your own skill library.
- **Extended thinking**: OpenAI models don't support Claude's extended thinking. Skills relying on `thinking` blocks will degrade gracefully.
- **o-series reasoning models**: If you need strong reasoning, consider swapping the Opus tier to `o3` or `o4-mini` instead of `gpt-5`.
- **Custom agents**: OpenAI models may not follow the launch convention (`subagent_type: general-purpose`) and instead choose a different subagent type (e.g. `Explore`). This can cause failures in non-git directories. If custom agent invocation fails, try running in a git-initialized directory.

## Troubleshooting

See the [troubleshooting guide](troubleshooting.md) for common issues.
