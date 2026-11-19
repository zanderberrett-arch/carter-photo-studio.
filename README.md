# CART3R Photo Studio

A Windows-friendly Python photo editor with:
- Local brightness, contrast, saturation, sharpness, grayscale, and sepia adjustments.
- Prompt-based AI image editing through the OpenAI Images API.
- Before/after previews and PNG downloads.
- A modular project layout and basic automated tests.

## Requirements

- Windows 10 or Windows 11
- Python 3.11 or newer (64-bit)
- An OpenAI API key for AI edits
- Internet access for AI edits and package installation

Local adjustments work without an API key. AI edits use your OpenAI API account and may incur charges. ChatGPT subscriptions and API billing are separate.

## 1. Open the project

Extract the ZIP. Open the extracted `python-project` folder in VS Code or File Explorer.

In VS Code choose **Terminal → New Terminal**.

## 2. Create a virtual environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use this for the current terminal only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Or use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## 3. Configure the API key

Copy `.env.example` and name the copy `.env`.

PowerShell:

```powershell
Copy-Item .env.example .env
notepad .env
```

Put your API key after `OPENAI_API_KEY=`. Do not share the key, commit `.env`, or paste it into source code. Create/manage API keys in your OpenAI platform account.

## 4. Run the app

```powershell
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## 5. Use it

1. Upload a PNG, JPG, JPEG, or WEBP image (maximum 20 MB).
2. Adjust local controls in the sidebar.
3. Download the local preview, or enter an AI edit instruction.
4. Select the AI model and click **Apply AI edit**.
5. Download the generated PNG.

For better preservation, say exactly what should change and what must remain unchanged. Example:

> Replace only the background with a softly lit studio. Keep the person's face, identity, hair, pose, clothes, and framing unchanged.

AI image editing is generative: it can alter details beyond the exact requested region. Inspect the result before using it.

## Project structure

```text
python-project/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── image_ops.py
│   ├── ai_editor.py
│   └── storage.py
└── tests/
    └── test_image_ops.py
```

## Run tests

```powershell
pytest -q
```

## Troubleshooting

- **`py` is not recognized:** reinstall Python from python.org and enable “Add Python to PATH”.
- **`OPENAI_API_KEY is missing`:** confirm `.env` is in the same folder as `app.py`, then restart Streamlit.
- **Authentication or quota error:** verify the key and API billing/limits in your OpenAI platform account.
- **Unsupported image:** save or export it as PNG, JPG, or WEBP.
- **Port already in use:** run `streamlit run app.py --server.port 8502`.

## Security notes

- `.env` contains a secret. Keep it private.
- Uploaded photos are sent to the OpenAI API only when you request an AI edit.
- Local adjustments are performed on your computer by this app.
- Generated images are saved under `outputs/`; do not put private images in a public repository.

## API reference

OpenAI Python image edit reference:
https://developers.openai.com/api/reference/python/resources/images/methods/edit
