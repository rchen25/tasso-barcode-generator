#!/usr/bin/env python3
"""
Tasso Barcode Generator
Generates barcode sticker sheets for Tasso blood collection devices
"""

import argparse
import csv
import glob
import os

from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Default directories
INPUT_DIR = "input"
OUTPUT_DIR = "output"
DEFAULT_OUTPUT = f"{OUTPUT_DIR}/tasso_barcodes.pdf"


class TassoBarcodeGenerator:
    """Generator for Tasso barcode sticker sheets in Avery 5160 format."""

    # Avery 5160 specifications
    PAGE_WIDTH, PAGE_HEIGHT = letter  # 8.5" x 11"
    LABEL_WIDTH = 2.625 * inch  # 2-5/8 inches
    LABEL_HEIGHT = 1.0 * inch

    # Layout
    COLS = 3
    ROWS = 10
    LABELS_PER_PAGE = COLS * ROWS  # 30 labels per page

    # Margins and spacing
    LEFT_MARGIN = 0.05 * inch
    TOP_MARGIN = 0.5 * inch
    HORIZONTAL_PITCH = 2.75 * inch
    VERTICAL_PITCH = 1.0 * inch

    # Barcode specifications
    SIDE_MARGIN = 0.138 * inch  # ~3.5mm margin on each side
    BARCODE_HEIGHT = 0.4 * inch
    BARCODE_X_OFFSET = -0.157 * inch  # 4mm left shift for alignment

    def __init__(self, output_path=DEFAULT_OUTPUT):
        """Initialize the generator with an output path."""
        self.output_path = output_path
        self.canvas = None
        self.total_pages = 0
        self.total_sheets = 0

    def _ensure_output_dir(self):
        """Create output directory if needed."""
        output_dir = os.path.dirname(self.output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

    def _read_barcodes_from_csv(self, csv_path):
        """Read barcode values from a CSV file."""
        barcodes = []
        with open(csv_path, "r", newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                barcode = row.get("barcode", "").strip()
                if barcode:
                    barcodes.append(barcode)
        return barcodes

    def _add_header(self, csv_filename):
        """Add header text to the current page."""
        y1 = self.PAGE_HEIGHT - 0.29 * inch
        y2 = self.PAGE_HEIGHT - 0.42 * inch
        center_x = self.PAGE_WIDTH / 2

        self.canvas.setFont("Helvetica-Bold", 8)
        self.canvas.drawCentredString(
            center_x, y1, "One barcode per Tasso foil pouch. To be scanned via the ARQ app."
        )

        self.canvas.setFont("Helvetica", 7)
        self.canvas.drawCentredString(center_x, y2, f"Source: {csv_filename}")

    def _add_barcode(self, x, y, barcode_text, include_id, include_instruction):
        """Add a barcode to a label position."""
        try:
            barcode_width = self.LABEL_WIDTH - 2 * self.SIDE_MARGIN
            barcode = code128.Code128(
                barcode_text,
                barWidth=barcode_width / len(barcode_text) / 11 * 0.9,
                height=self.BARCODE_HEIGHT,
                humanReadable=False,
            )

            # Position barcode (centered with left offset)
            bx = x + (self.LABEL_WIDTH - barcode_width) / 2 + self.BARCODE_X_OFFSET
            by = y + (self.LABEL_HEIGHT - self.BARCODE_HEIGHT) / 2 + 0.05 * inch
            barcode.drawOn(self.canvas, bx, by)

            # Barcode ID text
            if include_id:
                self.canvas.setFont("Helvetica", 6)
                self.canvas.drawCentredString(
                    x + self.LABEL_WIDTH / 2, by - 0.08 * inch, barcode_text
                )

            # Instruction text
            if include_instruction:
                self.canvas.setFont("Helvetica", 5.5)
                self.canvas.drawCentredString(
                    x + self.LABEL_WIDTH / 2,
                    y + 0.05 * inch,
                    "scan in ARQ app after taking blood sample",
                )

        except Exception as e:
            print(f"    Error generating barcode for '{barcode_text}': {e}")
            self.canvas.setFont("Helvetica", 6)
            self.canvas.drawString(
                x + 0.05 * inch, y + self.LABEL_HEIGHT / 2, f"Error: {barcode_text[:20]}"
            )

    def _process_csv(self, csv_path, include_header, include_id, include_instruction):
        """Process a single CSV file and add pages to the PDF."""
        filename = os.path.basename(csv_path)
        barcodes = self._read_barcodes_from_csv(csv_path)

        if not barcodes:
            return 0

        print(f"  Processing {filename}: {len(barcodes)} barcodes")

        idx = 0
        pages_added = 0

        while idx < len(barcodes):
            if self.total_pages > 0:
                self.canvas.showPage()

            pages_added += 1
            self.total_pages += 1

            if include_header:
                self._add_header(filename)

            for row in range(self.ROWS):
                for col in range(self.COLS):
                    if idx >= len(barcodes):
                        break

                    x = self.LEFT_MARGIN + col * self.HORIZONTAL_PITCH
                    y = self.PAGE_HEIGHT - self.TOP_MARGIN - row * self.VERTICAL_PITCH - self.LABEL_HEIGHT

                    self._add_barcode(x, y, barcodes[idx], include_id, include_instruction)
                    idx += 1

        return pages_added

    def generate(self, csv_files, include_header=True, include_id=True, include_instruction=True):
        """
        Generate a PDF from CSV files.

        Args:
            csv_files: List of CSV file paths
            include_header: Include header text on each page
            include_id: Include barcode ID text under each barcode
            include_instruction: Include instruction text
        """
        if not csv_files:
            print("No CSV files to process!")
            return

        print(f"Found {len(csv_files)} CSV files to process")
        print("=" * 60)

        self._ensure_output_dir()
        self.canvas = canvas.Canvas(self.output_path, pagesize=letter)

        for csv_file in csv_files:
            pages = self._process_csv(csv_file, include_header, include_id, include_instruction)
            self.total_sheets += pages
            print(f"    → {pages} page(s) / {pages} sheet(s) needed")

        self.canvas.save()

        print("=" * 60)
        print(f"\n✓ PDF created successfully: {self.output_path}")
        print(f"Total pages in PDF: {self.total_pages}")
        print(f"Total sticker sheets needed: {self.total_sheets}")
        print(f"Total CSV files processed: {len(csv_files)}")

    def generate_from_directory(self, directory, pattern="*.csv", **kwargs):
        """Generate PDF from all matching CSV files in a directory."""
        csv_files = sorted(glob.glob(os.path.join(directory, pattern)))
        self.generate(csv_files, **kwargs)

    # Backwards compatibility alias
    generate_from_csv_files = generate


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate Tasso barcode sticker sheets for Avery 5160 labels",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all CSV files in input/ directory (default)
  uv run tasso-barcode-generator

  # Process a single CSV file
  uv run tasso-barcode-generator data.csv -o output/barcodes.pdf

  # Process multiple CSV files
  uv run tasso-barcode-generator file1.csv file2.csv -o output/combined.pdf

  # Process all CSV files in a specific directory
  uv run tasso-barcode-generator --dir ./csv_files/ -o output/all_barcodes.pdf

  # Generate without headers or instructions (just barcodes and IDs)
  uv run tasso-barcode-generator --no-header --no-instruction
        """,
    )

    parser.add_argument("csv_files", nargs="*", help="CSV file(s) to process")
    parser.add_argument(
        "-o", "--output", default=None, help=f"Output PDF file (default: auto-named based on input)"
    )
    parser.add_argument("-d", "--dir", dest="directory", help="Process all CSV files in this directory")
    parser.add_argument("-p", "--pattern", default="*.csv", help="File pattern for --dir (default: *.csv)")
    parser.add_argument("--no-header", action="store_false", dest="include_header", help="Omit page headers")
    parser.add_argument("--no-id", action="store_false", dest="include_id", help="Omit barcode ID text")
    parser.add_argument("--no-instruction", action="store_false", dest="include_instruction", help="Omit instruction text")

    args = parser.parse_args()

    # Collect CSV files
    if args.directory:
        csv_files = sorted(glob.glob(os.path.join(args.directory, args.pattern)))
    elif args.csv_files:
        csv_files = args.csv_files
    else:
        # Default: use input/ directory
        os.makedirs(INPUT_DIR, exist_ok=True)
        csv_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.csv")))

    # Check for empty input
    if not csv_files:
        print(f"No CSV files found in '{INPUT_DIR}/' directory.\n")
        print("Usage options:")
        print(f"  1. Place CSV files in '{INPUT_DIR}/' and run again")
        print("  2. Specify files: tasso-barcode-generator file1.csv file2.csv")
        print("  3. Specify directory: tasso-barcode-generator --dir /path/to/csvs/")
        return

    # Auto-name output based on input files
    if args.output:
        output_path = args.output
    elif len(csv_files) == 1:
        # Single file: name output after input
        basename = os.path.splitext(os.path.basename(csv_files[0]))[0]
        output_path = f"{OUTPUT_DIR}/{basename}.pdf"
    else:
        # Multiple files: use default name
        output_path = DEFAULT_OUTPUT

    # Generate PDF
    generator = TassoBarcodeGenerator(output_path)
    generator.generate(
        csv_files,
        include_header=args.include_header,
        include_id=args.include_id,
        include_instruction=args.include_instruction,
    )

    print("\n✓ Complete!")
    print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
