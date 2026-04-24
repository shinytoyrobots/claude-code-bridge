"""claude-code-bridge — LiteLLM proxy handler that fixes tool schemas.

Some MCP servers emit JSON schemas that Anthropic tolerates but stricter
providers (OpenAI, Gemini) reject. The most common issue: array properties
missing the required `items` field.

This handler patches schemas in-transit before they reach the provider.
"""

import sys
from litellm.integrations.custom_logger import CustomLogger

_LOG_PREFIX = "[claude-code-bridge]"


class _ToolSchemaFixer(CustomLogger):
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        tools = data.get("tools")
        if not tools:
            return data

        fixed = 0
        for tool in tools:
            for schema in _extract_schemas(tool):
                fixed += _fix_array_schemas(schema)

        if fixed:
            print(f"{_LOG_PREFIX} Patched {fixed} array schema(s) missing 'items'", file=sys.stderr)

        return data


tool_schema_fixer = _ToolSchemaFixer()


def _extract_schemas(tool):
    # OpenAI Chat Completions format: tool.function.parameters
    func = tool.get("function")
    if isinstance(func, dict) and "parameters" in func:
        yield func["parameters"]
    # OpenAI Responses API format: tool.parameters (no function wrapper)
    elif "parameters" in tool:
        yield tool["parameters"]
    # Anthropic format: tool.input_schema
    if "input_schema" in tool:
        yield tool["input_schema"]


def _fix_array_schemas(schema):
    if not isinstance(schema, dict):
        return 0
    count = 0
    if schema.get("type") == "array" and "items" not in schema:
        schema["items"] = {}
        count += 1
    for val in schema.get("properties", {}).values():
        count += _fix_array_schemas(val)
    if isinstance(schema.get("items"), dict):
        count += _fix_array_schemas(schema["items"])
    if isinstance(schema.get("additionalProperties"), dict):
        count += _fix_array_schemas(schema["additionalProperties"])
    for combo_key in ("anyOf", "allOf", "oneOf"):
        for sub in schema.get(combo_key, []):
            count += _fix_array_schemas(sub)
    return count
