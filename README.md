# op-xy auto sample slicer 

This script processes an input audio file (WAV or MP3), detects transients, splits the file into smaller slices, and organizes these slices into numbered presets with a `patch.json` file for each preset. You can drag the folder to your opxy 

---

## Prerequisites

### System Requirements
- Python 3.8 or later
- `ffmpeg` installed and added to your system's PATH

### Supported Platforms
- **Windows**
- **macOS**
- **Linux**

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/aliosa27/op-xy-slicer.git
cd audio-transient-splitter
```

### 2. Install Dependencies

#### Windows
```bash
pip install -r requirements.txt
```
Install `ffmpeg` via Chocolatey or manually:
```bash
choco install ffmpeg
```
Ensure `ffmpeg` is in your PATH.

#### macOS
```bash
pip install -r requirements.txt
```
Install `ffmpeg` via Homebrew:
```bash
brew install ffmpeg
```

#### Linux
```bash
pip install -r requirements.txt
sudo apt install ffmpeg
```
For non-Debian distributions, use your package manager to install `ffmpeg`.

---

## Usage

Run the script with the following command:

```bash
python xy.py <input_file> <output_directory>
```

### Example

```bash
python xy.py input_audio.mp3 output_folder
```

This command will:
1. Detect transients in `input_audio.mp3`.
2. Split the audio into smaller slices.
3. Organize the slices into folders named `output_folder1.preset`, `output_folder2.preset`, etc.
4. Generate a `patch.json` file for each preset.

---

## Features
- Detects transients in audio files.
- Slices audio into manageable segments.
- Organizes segments into folders.
- Generates metadata (`patch.json`) for each preset.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

