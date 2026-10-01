from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict


CallableTool = Callable[..., Any]


@dataclass
class Tool:
    name: str
    func: CallableTool


class SimpleAgent:
    def __init__(self) -> None:
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, name: str, func: CallableTool) -> Tool:
        tool = Tool(name=name, func=func)
        self.tools[name] = tool
        return tool

    def run(self, tool_name: str, *args: Any, **kwargs: Any) -> Any:
        tool = self.tools.get(tool_name)
        if tool is None:
            raise ValueError(f"Unknown tool: {tool_name}")
        return tool.func(*args, **kwargs)
