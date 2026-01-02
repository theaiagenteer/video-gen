import asyncio
import time
from pathlib import Path
from agency_swarm.tools import BaseTool
from pydantic import Field, field_validator
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

class RaySoSnapshotTool(BaseTool):
    code: str = Field(..., description="Code snippet to render in the image.")
    output_path: str = Field(
        "outputs/snapshots/rayso_snapshot.png",
        description="Local path (including filename) where the PNG will be saved.",
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
        download_dir = output_file.parent
        download_dir.mkdir(parents=True, exist_ok=True)

        # Browserless CDP endpoint with token
        token = "2TiZ4xXMjxj1FIM6fffda6f102ea737e6005371987c75cc7e"
        ws_endpoint = f"wss://production-sfo.browserless.io?token={token}"

        async with async_playwright() as p:
            # Connect to remote Browserless Chrome
            browser = await p.chromium.connect_over_cdp(ws_endpoint)

            # Use default context (Browserless starts a fresh one)
            context = browser.contexts[0] if browser.contexts else await browser.new_context()

            # New page for Ray.so
            page = await context.new_page()

            await page.goto("https://ray.so/", wait_until="networkidle")

            # Wait for textarea, type code
            try:
                textarea = await page.wait_for_selector("textarea", timeout=15000)
            except PlaywrightTimeoutError:
                await browser.close()
                raise RuntimeError("Editor textarea not found on Ray.so")

            await textarea.fill(self.code)

            # Click "Export as PNG"
            export_button = await page.wait_for_selector("//button[contains(., 'Export as PNG')]", timeout=15000)
            await export_button.click()

            # Wait for download to be triggered
            download = await page.wait_for_event("download", timeout=30000)
            # Save the downloaded PNG
            await download.save_as(str(output_file))

            # Close browser session
            await browser.close()

        return f"Ray.so snapshot saved to {output_file}"
