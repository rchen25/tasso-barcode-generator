# Tasso Barcode Generator

A Python package for generating barcode sticker sheets formatted for Tasso blood collection devices. Creates PDF files optimized for printing on Avery 5160 (or compatible) label sheets with 30 labels per page.

## Features

- 📊 **Native Code128 barcodes** - High-quality vector barcodes for reliable scanning
- 🏷️ **Avery 5160 format** - Standard 1" × 2-5/8" labels (30 per sheet)
- 📄 **Batch processing** - Generate multiple sheets from CSV files
- 🎯 **Optimized layout** - Properly positioned barcodes with 3.5mm margins
- 🔧 **Customizable output** - Control headers, IDs, and instructions
- 📦 **Easy installation** - Works with `uv`, `pip`, or `pipx`

## Latest Updates (v1.0.2)

- ✅ Enhanced barcode positioning (4mm left shift for optimal alignment)
- ✅ Centered header text for professional appearance
- ✅ Eliminated empty pages between participants
- ✅ Reduced page left margin to prevent indentation
- ✅ Adjusted barcode width to 2.349" (3.5mm margins on each side)

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/arq/tasso-barcode-generator.git
cd tasso-barcode-generator

# Run directly with uv
uv run tasso-barcode-generator --help
```

### Using pip

```bash
# Install from directory
pip install ./tasso-barcode-generator

# Or install in development mode
pip install -e ./tasso-barcode-generator
```

### Using pipx (for isolated installation)

```bash
pipx install ./tasso-barcode-generator
```

## Quick Start

### Basic Usage

Process a single CSV file:
```bash
uv run tasso-barcode-generator input.csv -o output.pdf
```

Process multiple CSV files:
```bash
uv run tasso-barcode-generator file1.csv file2.csv file3.csv -o combined.pdf
```

Process all CSV files in a directory:
```bash
uv run tasso-barcode-generator --dir ./csv_files/ -o all_barcodes.pdf
```

### CSV File Format

Your CSV files should have a header row with at least a `barcode` column:

```csv
batchId,barcode,generatedOn,redeemed,redeemedOn
batch1,ABC123-001,"11/21/2025, 4:55:27 PM",,
batch1,ABC123-002,"11/21/2025, 4:55:27 PM",,
batch1,ABC123-003,"11/21/2025, 4:55:27 PM",,
```

Only the `barcode` column is required - other columns are ignored.

## Command Line Options

```
usage: tasso-barcode-generator [-h] [-o OUTPUT] [-d DIRECTORY] [-p PATTERN]
                               [--no-header] [--no-id] [--no-instruction]
                               [csv_files ...]

Arguments:
  csv_files             CSV file(s) to process

Options:
  -o, --output OUTPUT   Output PDF file path (default: tasso_barcodes.pdf)
  -d, --dir DIRECTORY   Process all CSV files in this directory
  -p, --pattern PATTERN File pattern when using --dir (default: *.csv)
  --no-header          Don't include header text on pages
  --no-id              Don't include barcode ID text under barcodes
  --no-instruction     Don't include instruction text
```

## Python API

You can also use the package programmatically:

```python
from tasso_barcode_generator import TassoBarcodeGenerator

# Create generator instance
generator = TassoBarcodeGenerator("output.pdf")

# Process single file
generator.generate_from_csv_files(["input.csv"])

# Process multiple files
csv_files = ["file1.csv", "file2.csv", "file3.csv"]
generator.generate_from_csv_files(
    csv_files,
    include_header=True,
    include_id=True,
    include_instruction=True
)

# Process directory
generator.generate_from_directory(
    "./csv_files/",
    pattern="*.csv"
)
```

## Output Specifications

### Label Layout
Each label contains (from top to bottom):
1. **Barcode** - Wide format Code128 barcode
2. **Barcode ID** - The barcode string (6pt font)
3. **Instruction** - "scan in ARQ app after taking blood sample" (5.5pt font)

### Page Header
Each page includes:
- **Left**: "One barcode per Tasso foil pouch. To be scanned via the ARQ app."
- **Right**: Source CSV filename

### Dimensions
- **Label size**: 1" × 2-5/8" (Avery 5160 standard)
- **Barcode width**: 2.349" (with 3.5mm margins on each side)
- **Barcode position**: Shifted 4mm left from center for optimal alignment
- **Labels per page**: 30 (10 rows × 3 columns)
- **Page size**: US Letter (8.5" × 11")
- **Page margins**: Minimal left margin (0.05") to prevent indentation

## Examples

### Generate barcodes for multiple participants

```bash
# Process all participant CSV files
uv run tasso-barcode-generator \
    ChrisMason_*.csv \
    JordanWeiss_*.csv \
    RobertChen_*.csv \
    -o all_participants.pdf
```

### Generate minimal labels (just barcodes)

```bash
# Only barcodes, no headers or instructions
uv run tasso-barcode-generator input.csv \
    --no-header \
    --no-instruction \
    -o minimal_labels.pdf
```

### Batch processing with pattern matching

```bash
# Process all CSV files matching a pattern
uv run tasso-barcode-generator \
    --dir ./data/ \
    --pattern "*_barcodes_*.csv" \
    -o filtered_output.pdf
```

## Development

### Project Structure

```
tasso-barcode-generator/
├── pyproject.toml                    # Package configuration
├── README.md                         # This file
├── tasso_barcode_generator/
│   ├── __init__.py                  # Main module and CLI
│   └── __main__.py                  # Module runner
└── examples/                         # Example CSV files (optional)
```

### Running Tests

```bash
# Run the package directly
python -m tasso_barcode_generator --help

# Or use uv
uv run python -m tasso_barcode_generator --help
```

### Building the Package

```bash
# Build with uv
uv build

# Or build with pip
pip install build
python -m build
```

## Requirements

- Python 3.8+
- reportlab >= 4.0.0

## Printer Settings

When printing the generated PDFs:

1. **Paper size**: US Letter (8.5" × 11")
2. **Scale**: Set to "Actual Size" or "100%" (no scaling)
3. **Quality**: Use high quality/best setting for crisp barcodes
4. **Orientation**: Portrait
5. **Margins**: Use default printer margins

## Tips for Best Results

1. **Test first**: Print a test page on regular paper to verify alignment
2. **Clean printer**: Ensure print heads are clean for crisp barcodes
3. **Quality labels**: Use genuine Avery 5160 or high-quality compatible labels
4. **Storage**: Store printed labels in a cool, dry place
5. **Scanning**: Test scan a few barcodes before mass production

## Troubleshooting

### Barcodes won't scan
- Ensure printer is set to high quality
- Check that scaling is set to 100%
- Clean the scanner lens
- Verify barcode strings are valid

### Alignment issues
- Verify you're using the correct label sheets (Avery 5160)
- Check printer scaling is set to "Actual Size"
- Try printing a test page first

### Missing dependencies
```bash
# Install reportlab if not automatically installed
pip install reportlab
```

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Note**: This tool is designed specifically for Tasso blood collection devices and the ARQ app. Ensure you follow all medical device protocols and regulations when using this system for sample collection and tracking.
