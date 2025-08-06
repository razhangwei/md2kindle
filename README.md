# Markdown to Kindle Converter

A simple Python script to convert Markdown files to Kindle-compatible format and send them to your Kindle device via email.

## Prerequisites

- Python 3.7+
- Pandoc (for document conversion)
- A Kindle device with an associated email address

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd md2kindle
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Pandoc (if not already installed):
   - macOS: `brew install pandoc`
   - Linux: `sudo apt-get install pandoc`
   - Windows: Download from [pandoc.org](https://pandoc.org/installing.html)

4. Create a `.env` file with your email configuration:
   ```
   EMAIL_ADDRESS=your-email@example.com
   EMAIL_PASSWORD=your-email-password-or-app-password
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   KINDLE_EMAIL=your-kindle-email@kindle.com
   ```

## Usage

```
bash md2kindle.sh path/to/markdown_file.md
```

Additional options:
- `--title "Your Book Title"` - Set a custom title (defaults to filename)
- `--author "Author Name"` - Set author name
- `--cover path/to/cover.jpg` - Add a cover image
- `--format epub` - Output format (default: epub)
- `--no-formatting-fix` - Skip Markdown formatting improvements for bullet points
- `--no-send` - Convert only, don't send via email

## Notes

- Ensure your sending email is added to the approved list in your Amazon Kindle settings.
- For Gmail, you'll need to use an App Password instead of your regular password. You can visit [Gmail App Passwords](https://myaccount.google.com/apppasswords) to generate one.
- Kindle supports EPUB format for optimal reading experience.
- The script automatically improves Markdown formatting by ensuring blank lines before and after lists and removing extra blank lines between bullet points for more compact Kindle rendering.

### Markdown Formatting Tips

For best results with Kindle conversion:

1. Leave blank lines before and after lists
2. Use indented bullet points under numbered lists (see `test_bullets.md` for examples)
3. Avoid blank lines between bullet points; the script removes them for compact Kindle rendering, though blank lines before and after the list are still required

Example of good formatting:
```markdown
### Primary Factors

1. **Work Stress**
   - Factor one
   - Factor two

2. **Environment**
   - Factor one
   - Factor two
```

## License

MIT
