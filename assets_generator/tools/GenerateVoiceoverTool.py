import os
from pathlib import Path
from typing import Optional

from agency_swarm.tools import BaseTool
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from pydantic import Field, field_validator

load_dotenv()


class GenerateVoiceoverTool(BaseTool):
    """
    Generate a voiceover audio file from text using the ElevenLabs Text-to-Speech API.
    """

    text: str = Field(..., description="Narration text to convert to speech.")
    voice_id: str = Field(
        "JBFqnCBsd6RMkjVDRZzb",
        description="ElevenLabs voice ID to use for synthesis.",
    )
    model_id: str = Field(
        "eleven_multilingual_v2",
        description="ElevenLabs TTS model ID.",
    )
    output_format: str = Field(
        "mp3_44100_128",
        description="Output audio format, e.g., mp3_44100_128 or pcm_16000.",
    )
    output_path: str = Field(
        ...,
        description="Local file path (including filename) where the audio will be saved.",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="Optional ElevenLabs API key; if omitted, uses ELEVENLABS_API_KEY env var.",
    )

    @field_validator("text")
    @classmethod
    def _validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Text must be non-empty.")
        return value

    @field_validator("output_path")
    @classmethod
    def _validate_output_path(cls, value: str) -> str:
        path = Path(value)
        if path.exists() and not path.is_file():
            raise ValueError("output_path must point to a file, not a directory.")
        return str(path)

    def run(self) -> str:
        key = self.api_key or os.getenv("ELEVENLABS_API_KEY")
        if not key:
            raise RuntimeError("ELEVENLABS_API_KEY is not set in the environment.")

        client = ElevenLabs(api_key=key)
        output_file = Path(self.output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            audio = client.text_to_speech.convert(
                voice_id=self.voice_id,
                model_id=self.model_id,
                text=self.text,
                output_format=self.output_format,
            )
        except Exception as exc:
            raise RuntimeError(f"ElevenLabs error: {exc}") from exc

        with open(output_file, "wb") as f:
            for chunk in audio:
                f.write(chunk)

        return f"Voiceover saved to {output_file}"


if __name__ == "__main__":
    tool = GenerateVoiceoverTool(
        text="This is a short synthesis test.",
        output_path="outputs/voiceovers/voiceover_demo.mp3",
    )
    print(tool.run())
