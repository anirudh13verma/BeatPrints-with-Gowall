# gowall.py
import subprocess
from pathlib import Path
import tempfile
import shutil

# map the beatprint themes to gowall themes (Light and Dark are where im not sure so wanna check)
themeMap = {
    "Light": "github-light",
    "Dark": "onedark", # may use dracula/arcdark/atomdark (not sure which one exactly replicates the theme)
    "Catppuccin": "catppuccin",
    "Gruvbox": "gruvbox",
    "Nord": "nord",
    "RosePine": "rose-pine",
    "Everforest": "everforest"
}


def gowallify(image_path: Path, theme: str = "Light") -> Path:
    """
    Applies a GoWall theme to the input image and returns path to the themed image.
    The result is saved in a temporary directory and should be cleaned up after use.
    """
    # Create temp directory for processed image
    temp_dir = Path(tempfile.mkdtemp(prefix="gowall_"))
    output_path = temp_dir / f"{image_path.stem}_gowall.png"

    # Check if GoWall is available
    if not shutil.which("gowall"):
        raise RuntimeError("GoWall CLI is not installed or not in PATH.")
    
    theme = themeMap[theme]

    # Build command
    command = [
        "gowall", "convert",
        str(image_path),
        "-t", theme,
        "--output", str(output_path)
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"GoWall command failed: {e}") from e

    return output_path


def cleanup_temp_dir(temp_path: Path):
    """
    Deletes the temporary directory and its contents.
    """
    if temp_path.exists() and temp_path.is_dir():
        shutil.rmtree(temp_path)
