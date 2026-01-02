import re
import time
from pathlib import Path

from agency_swarm.tools import BaseTool
from pydantic import Field, field_validator

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class RaySoSnapshotTool(BaseTool):
    """
    Render code into a ray.so-styled image and save it locally (Selenium-based export).
    """

    code: str = Field(..., description="Code snippet to render in the image.")
    output_path: str = Field(
        "outputs/snapshots/rayso_snapshot.png",
        description="Local path (including filename) where the PNG will be saved.",
    )
    headless: bool = Field(True, description="Whether to run Chrome headless.")

    @field_validator("code")
    @classmethod
    def _validate_code(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Code must be non-empty.")
        return value

    def run(self) -> str:
        output_file = Path(self.output_path).resolve()
        download_dir = output_file.parent
        download_dir.mkdir(parents=True, exist_ok=True)

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")

        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1400,900")

        chrome_options.add_experimental_option(
            "prefs",
            {
                "download.default_directory": str(download_dir),
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True,
            },
        )

        driver = webdriver.Chrome(options=chrome_options)
        wait = WebDriverWait(driver, 20)

        try:
            driver.get("https://ray.so/")

            # Wait for editor textarea
            textarea = wait.until(
                EC.presence_of_element_located((By.TAG_NAME, "textarea"))
            )

            textarea.clear()
            textarea.send_keys(self.code)

            # Click "Export as PNG"
            export_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Export as PNG')]")
                )
            )
            export_button.click()

            # Wait for download to complete
            timeout = time.time() + 30
            downloaded_file = None

            while time.time() < timeout:
                pngs = list(download_dir.glob("*.png"))
                if pngs:
                    downloaded_file = pngs[0]
                    break
                time.sleep(0.5)

            if not downloaded_file:
                raise RuntimeError("PNG export failed or timed out.")

            downloaded_file.rename(output_file)

        finally:
            driver.quit()

        return f"Ray.so snapshot saved to {output_file}"


if __name__ == "__main__":
    tool = RaySoSnapshotTool(
        code="console.log('Hello Ray.so');",
        output_path="outputs/snapshots/rayso.png",
        headless=True,
    )
    print(tool.run())
