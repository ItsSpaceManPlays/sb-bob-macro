# Slap battles macro
This is a simple python script for macroing bob in a roblox game called slap battles

# Setup

1. **Run the script:** Execute the `auto e.py` file. This will generate a `settings.json` configuration file in the same directory.

2.**Configure the `settings.json` file:** The gernerated `settings.json` file will look like this:
```json
{
    "webhook": "",
    "userId": 1
}
```
- **webhook:** Create a Discord webhook and paste the URL here.
- **userId:**  Replace the `1` with your Roblox user ID.

# How to use
## Basic usage
- **Toggling**:
   - Press `F6` to toggle the script on or off during gameplay.

# Multi account support
The script allows for 2 accounts to be macroed at once. If you wish to use this feature, follow these steps:

1. **Hover over Roblox window**:
   - For your alt account, you will be prompted to hover your mouse over their Roblox windows.
2. **Skip alt account macroing**:
   - If you do not want to macro on your alt account, you can simply skip this step by running the script with the flag:
   `--no-alt-afk`

# Requirements
- A working python environment (Python 3.x)
- Install all dependencies with `pip install -r requirements.txt`