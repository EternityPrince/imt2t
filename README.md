Markdown Image Embedder (Base64 Footer Edition)

This Python utility automates the process of embedding local images directly into Markdown (.md) files. To keep the document readable and avoid "walls of text" caused by long Base64 strings, the script moves the image data to the footer of the document using Markdown footnotes.
🚀 Features

    Clean Reading: Replaces image filenames in the text with short markers like [^fig_1].

    Base64 Conversion: Encodes .jpg, .jpeg, .png, .gif, and .webp files.

    Footer Storage: Appends all heavy data strings to the bottom of the file.

    Batch Processing: Supports multiple directories in one command.

    Auto-Cleanup: Deletes original image files after successful embedding to save space.

🛠 How it Works

The script follows a specific logic to link your files:

    It scans the target directory for one .md file and all images.

    It looks for mentions of the image filename (e.g., _page_9_Figure_0.jpeg) inside the Markdown text.

    It replaces the mention with a footnote reference [^fig_N].

    It defines that footnote at the end of the file:

    [^fig_N]: ![](data:image/jpg;base64,...)

📋 Requirements

    Python 3.x

    No external libraries required (uses standard os, re, base64, and pathlib).

💻 Usage

Run the script from your terminal by passing the paths to the directories you want to process.
Bash

python embed_to_footer.py "path/to/folder1" "path/to/folder2"

Example Input

Directory Structure:
Plaintext

/my_project/
├── layoff_trap.md
├── _page_9_Figure_0.jpeg
└── _page_11_Figure_3.jpeg

After Running the Script:

    The .jpeg files are deleted.

    layoff_trap.md text:

        "...as shown in the analysis [^fig_1]. The data continues..."

    layoff_trap.md footer:

        ---

        [^fig_1]: ![](data:image/jpg;base64,/9j/4AAQSkZJRg...)

⚠️ Notes

    Backup: Since the script deletes original images, it is recommended to have a backup of your data before running it.

    Compatibility: Footnote rendering depends on your Markdown viewer (Obsidian, VS Code, GitHub, and Pandoc support this syntax natively).

License

MIT License. Free to use and modify.
