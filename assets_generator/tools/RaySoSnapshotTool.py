import asyncio
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field, field_validator

from PIL import Image, ImageDraw, ImageFont
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatter import Formatter
from pygments.styles import get_style_by_name


class _ImageFormatter(Formatter):
    def __init__(self, style_name="monokai"):
        super().__init__()
        self.style = get_style_by_name(style_name)
        self.tokens = []

    def format(self, tokensource, outfile):
        for ttype, value in tokensource:
            style = self.style.style_for_token(ttype)
            color = style.get("color") or "f8f8f2"
            self.tokens.append((value, f"#{color}"))


class RaySoSnapshotTool(BaseTool):
    code: str = Field(..., description="Code snippet to render in the image.")
    output_path: str = Field(
        "outputs/snapshots/rayso_snapshot.png",
        description="Local path (including filename) where the PNG will be saved.",
    )
    language: str | None = Field(
        None,
        description="Optional language override (python, js, cpp, etc).",
    )

    @field_validator("code")
    @classmethod
    def _validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code must be non-empty.")
        return value

    def run(self) -> str:
        return asyncio.run(self._run_async())

    async def _run_async(self) -> str:
        output_file = Path(self.output_path).resolve()
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # === Styling ===
        bg_color = "#1e1e1e"
        padding = 48
        line_spacing = 12
        font_size = 28
        font_path = "C:/Windows/Fonts/consola.ttf"  # change if needed

        font = ImageFont.truetype(font_path, font_size)

        lexer = (
            get_lexer_by_name(self.language)
            if self.language
            else guess_lexer(self.code)
        )

        formatter = _ImageFormatter()
        highlight(self.code, lexer, formatter)

        dummy = Image.new("RGB", (1, 1))
        dummy_draw = ImageDraw.Draw(dummy)

        lines = "".join(t[0] for t in formatter.tokens).split("\n")
        max_width = max(
            dummy_draw.textlength(line, font=font) for line in lines
        )
        height = (font_size + line_spacing) * len(lines)

        img = Image.new(
            "RGB",
            (int(max_width + padding * 2), int(height + padding * 2)),
            bg_color,
        )
        draw = ImageDraw.Draw(img)

        x = padding
        y = padding

        for value, color in formatter.tokens:
            parts = value.split("\n")
            for i, part in enumerate(parts):
                if part:
                    draw.text((x, y), part, font=font, fill=color)
                    x += draw.textlength(part, font=font)
                if i < len(parts) - 1:
                    x = padding
                    y += font_size + line_spacing

        img.save(output_file)
        return f"Ray-style snapshot saved to {output_file}"
