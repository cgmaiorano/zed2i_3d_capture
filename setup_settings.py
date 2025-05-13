#!/usr/bin/env python3
"""One-time setup script to configure settings.py for this repository."""

import os
import pathlib as pl
import shutil

# Directory of the repo (adjust if needed)
DIR_REPO = pl.Path(__file__).resolve().parent


def prompt_for_path(prompt_text: str, default: str = "") -> str:
    """Prompt for a directory or file path.

    - If it's a directory path, create it if it doesn't exist.
    - If it's a file path, check that it exists.
    """
    while True:
        path_input = input(f"{prompt_text} [{default}]: ").strip() or default
        abs_path = os.path.abspath(path_input)

        if abs_path.endswith(os.sep) or not os.path.splitext(abs_path)[1]:
            # Treat as directory
            try:
                os.makedirs(abs_path, exist_ok=True)
                return abs_path
            except Exception as e:
                print(f"❌ Failed to create/access directory '{abs_path}': {e}")
        else:
            # Treat as file
            if os.path.isfile(abs_path):
                return abs_path
            else:
                print(f"❌ File does not exist: '{abs_path}'")


def prompt_from_choices(prompt_text: str, choices: list[str], default: str = "") -> str:
    """Prompt user to select from a list of options."""
    print(f"{prompt_text}:")
    for i, choice in enumerate(choices, 1):
        print(f"  {i}. {choice}")
    while True:
        choice = input(
            f"Choose [1-{len(choices)}] or type a custom value [{default}]: "
        ).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(choices):
            return choices[int(choice) - 1]
        elif choice:
            return choice
        elif default:
            return default
        print("❌ Invalid selection.")


def write_settings_file(settings_path: pl.Path, config: dict):
    """Write the collected config to a settings.py file."""
    with open(settings_path, "w") as f:
        f.write("# Auto-generated settings\n\n")
        for key, value in config.items():
            if isinstance(value, str) and os.path.isabs(value):
                f.write(f'{key} = r"{value}"\n')
            else:
                f.write(f'{key} = "{value}"\n')
    print(f"✅ Created {settings_path}")


def main() -> None:
    """Run setup prompts and write settings.py."""
    print("🔧 Setting up your repository configuration...")

    output_dir = prompt_for_path("Enter the path to the output folder")

    # Create sub directories for outputs
    svo_output = pl.Path(output_dir) / "svo"
    xlsx_output = pl.Path(output_dir) / "xlsx"
    try:
        os.makedirs(svo_output, exist_ok=True)
        os.makedirs(xlsx_output, exist_ok=True)
    except Exception as e:
        print(
            f"❌ Failed to create/access output-sub directories '{svo_output} & {xlsx_output}': {e}"
        )

    vlc_exe = prompt_for_path("Enter the path to the VLC executable file")

    depth_modes = ["NEURAL", "NEURAL_LIGHT", "NEURAL_PLUS"]
    depth_mode = prompt_from_choices(
        "Select the ZED depth mode", depth_modes, default="NEURAL"
    )

    detection_models = ["HUMAN_BODY_FAST", "HUMAN_BODY_MEDIUM", "HUMAN_BODY_ACCURATE"]
    detection_model = prompt_from_choices(
        "Select the ZED human body detection model",
        detection_models,
        default="HUMAN_BODY_ACCURATE",
    )

    # Collect configuration
    config = {
        "OUTPUT_DIR": output_dir,
        "VLC_EXE": vlc_exe,
        "DEPTH_MODE": depth_mode,
        "DETECTION_MODEL": detection_model,
    }

    # Save settings to a Python file
    settings_path = DIR_REPO / "settings.py"
    write_settings_file(settings_path, config)

    # Clean up: remove setup script and folder if inside a setup directory
    script_path = pl.Path(__file__)
    setup_dir = script_path.parent

    print("🧹 Cleaning up setup files...")

    try:
        script_path.unlink()
        if setup_dir.name == "setup" and setup_dir != DIR_REPO:
            shutil.rmtree(setup_dir)
        print("🗑️  Setup complete and setup files removed.")
    except Exception as e:
        print(f"⚠️  Cleanup failed: {e}")


if __name__ == "__main__":
    main()
