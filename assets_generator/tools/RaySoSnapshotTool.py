import re
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field, field_validator
from playwright.sync_api import Error as PlaywrightError, sync_playwright


class RaySoSnapshotTool(BaseTool):
    """
    Render code into a ray.so-styled image and save it locally (Playwright-based export).
    """

    code: str = Field(..., description="Code snippet to render in the image.")
    output_path: str = Field(
        "outputs/snapshots/rayso_snapshot.png",
        description="Local path (including filename) where the PNG will be saved.",
    )
    headless: bool = Field(
        True, description="Whether to run the browser in headless mode."
    )

    @field_validator("code")
    @classmethod
    def _validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code must be non-empty.")
        return value

    def run(self) -> str:
        output_file = Path(self.output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context(accept_downloads=True)
                page = context.new_page()
                page.goto("https://ray.so/", wait_until="domcontentloaded")
                page.locator("textarea").dblclick()
                page.locator("textarea").fill(self.code)

                with page.expect_download() as download_info:
                    page.get_by_role(
                        "button", name=re.compile("Export as PNG", re.IGNORECASE)
                    ).click()
                download = download_info.value
                download.save_as(str(output_file))

                context.close()
                browser.close()
        except PlaywrightError as exc:
            raise RuntimeError(
                "Playwright error during ray.so export. Ensure browsers are installed "
                "with `python -m playwright install chromium`. Details: "
                f"{exc}"
            ) from exc

        return f"Ray.so snapshot saved to {output_file}"


if __name__ == "__main__":
    tool = RaySoSnapshotTool(
        code="console.log('Hello Ray.so');",
        output_path="outputs/snapshots/rayso.png",
    )
    print(tool.run())
