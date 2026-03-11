# deepl-cli

A lightweight command-line tool for the [DeepL API](https://www.deepl.com/docs-api). Zero dependencies — just Python 3 standard library.

## Features

- Translate text between 30+ languages
- Auto-detect source language
- Formality control (formal/informal) for supported languages
- Translate files
- Check API usage stats
- List supported languages

## Quick Start

```bash
export DEEPL_API_KEY="your-api-key"

# Translate text
python deepl_cli.py "Hello, world!" --target DE

# Auto-detect source, translate to Czech
python deepl_cli.py "Привет мир" --target CS

# Formal German
python deepl_cli.py "Hey, what's up?" --target DE --formality more

# Translate a file
python deepl_cli.py --file input.txt --target FR

# Check usage
python deepl_cli.py --usage

# List languages
python deepl_cli.py --languages
```

## Usage

```
python deepl_cli.py <text> -t <target_lang> [-s <source_lang>] [--formality <level>]
python deepl_cli.py --file <path> -t <target_lang>
python deepl_cli.py --languages
python deepl_cli.py --usage
```

### Language codes

Common: `EN-US`, `EN-GB`, `DE`, `FR`, `ES`, `IT`, `CS`, `RU`, `PL`, `PT-BR`, `JA`, `ZH-HANS`, `KO`, `UK`

Source language is auto-detected if omitted.

### Formality

Supported for: DE, FR, ES, IT, NL, PL, PT, RU, JA

Options: `default`, `more`, `less`, `prefer_more`, `prefer_less`

## Requirements

- Python 3.6+
- DeepL API key ([get one here](https://www.deepl.com/pro-api))

## License

MIT
