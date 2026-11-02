import difflib
import inspect
import json
import shutil
import textwrap
from dataclasses import asdict, is_dataclass
from itertools import zip_longest


class Viewer:
    """Display trajectories, messages, mappings, objects, and text in the terminal.

    Usage:
        Viewer(response).display()
        Viewer(agent.memory.get_messages()).display()
        Viewer(agent.trajectory).display()
    """

    def __init__(self, value):
        self.value = value

    def _format(self, value):
        if is_dataclass(value) and not isinstance(value, type):
            value = asdict(value)
        if isinstance(value, (dict, list, tuple)):
            return json.dumps(value, indent=2, ensure_ascii=False, default=str)
        return str(value)

    def _render_fields(self, fields):
        lines = []
        for label, value in fields.items():
            label = str(label).replace("_", " ").capitalize()
            lines.append(f"{label}:")
            lines.append(textwrap.indent(self._format(value), "  "))
        return "\n".join(lines) or "{}"

    def _render_step(self, step_index, step):
        if step.answer is not None:
            kind = "Final answer"
        elif step.action is not None:
            action = step.action.get("function") or step.action
            kind = action.get("name", "action")
        else:
            kind = "Thinking"

        lines = [f"  Step {step_index} - {kind}"]
        for label, value in vars(step).items():
            if value is None or value == "":
                continue
            lines.append(f"    {label.capitalize()}:")
            lines.append(textwrap.indent(self._format(value), "      "))
        return "\n".join(lines)

    def _render_run(self, run_index, run):
        lines = [f"Run {run_index}", "  Query:"]
        lines.append(textwrap.indent(str(run["query"]), "    "))
        if not run["steps"]:
            lines.append("  No steps recorded.")
        for step_index, step in enumerate(run["steps"], start=1):
            lines.append(self._render_step(step_index, step))
        return "\n".join(lines)

    def _render_item(self, index, item):
        if isinstance(item, dict) and "role" in item:
            heading = f"Message {index} - {str(item['role']).capitalize()}"
            item = {key: value for key, value in item.items() if key != "role"}
        else:
            heading = f"Item {index}"
        return heading + "\n" + textwrap.indent(Viewer(item).render(), "  ")

    def render(self) -> str:
        """Return a plain-text view suited to the supplied value."""
        value = self.value
        if isinstance(getattr(value, "runs", None), list):
            return "\n\n".join(
                self._render_run(index, run)
                for index, run in enumerate(value.runs, start=1)
            ) or "No runs recorded."
        if is_dataclass(value) and not isinstance(value, type):
            return self._render_fields(asdict(value))
        if isinstance(value, dict):
            return self._render_fields(value)
        if isinstance(value, (list, tuple)):
            return "\n\n".join(
                self._render_item(index, item)
                for index, item in enumerate(value, start=1)
            ) or self._format(value)
        if hasattr(value, "__dict__") and not isinstance(value, type):
            return self._render_fields(vars(value))
        return self._format(value)

    def display(self, file=None) -> None:
        """Print the view to stdout or a supplied text stream."""
        print(self.render(), file=file)

    def __str__(self) -> str:
        return self.render()
