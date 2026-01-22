# Changelog

All notable changes to the Tasso Barcode Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.2] - 2025-12-05

### Changed
- Barcode position shifted additional 1mm to the left (now 4mm total left shift)
- Updated positioning calculation for better label alignment

### Technical Details
- Barcode x-position calculation: `x + (width - barcode_width) / 2 - 0.157"` (4mm left shift)

## [1.0.1] - 2025-12-05

### Fixed
- Barcode positioning - shifted 3mm to the left for proper alignment on labels
- Page indentation issue by reducing left margin to 0.05"
- Empty pages appearing between different CSV file outputs
- Header text alignment - now centered instead of left/right justified

### Changed
- Barcode width reduced to 2.349" (3.5mm margins instead of 1.5mm)
- Header text (both lines) now centered on the page
- Page break logic optimized to eliminate unnecessary blank pages

### Technical Details
- `LEFT_MARGIN` changed from 0.1875" to 0.05"
- `SIDE_MARGIN` changed from 0.059" to 0.138" (1.5mm to 3.5mm)
- Barcode x-position calculation includes 3mm left shift: `x + (width - barcode_width) / 2 - 0.118"`
- Removed redundant `showPage()` calls between CSV files

## [1.0.0] - 2025-12-04

### Initial Release
- Native Code128 barcode generation using reportlab
- Avery 5160 label format support (30 labels per sheet)
- Batch processing of multiple CSV files
- Customizable output (headers, IDs, instructions)
- Command-line interface with argparse
- Python package with `uv` support
- PDF generation optimized for Tasso blood collection devices
- ARQ app integration support
