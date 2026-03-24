# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-03-24

### Added
- Full download functionality for study data ([e6d9fe9](https://github.com/areias03/SPIREpy/commit/e6d9fe9))
- Sample contig depths feature ([a972e4f](https://github.com/areias03/SPIREpy/commit/a972e4f))
- Disk caching for cluster and genome metadata ([700d693](https://github.com/areias03/SPIREpy/commit/700d693))
- Comprehensive unit and integration tests for data functions ([b61a145](https://github.com/areias03/SPIREpy/commit/b61a145))
- Docstring and type hint for `get_contig_depths()` method ([0603ef6](https://github.com/areias03/SPIREpy/commit/0603ef6))

### Changed
- Improved type hints: updated return type annotations to use `pl.DataFrame` instead of `pl.dataframe.DataFrame` ([072f10b](https://github.com/areias03/SPIREpy/commit/072f10b))
- Added `Union` type hint for `get_amr_annotations()` to properly handle `None` return ([072f10b](https://github.com/areias03/SPIREpy/commit/072f10b))
- Use more Polars-style code patterns ([35e460d](https://github.com/areias03/SPIREpy/commit/35e460d))
- Use "SPIREpy" as logger name ([5ec51a7](https://github.com/areias03/SPIREpy/commit/5ec51a7))
- Only import pandas when needed to improve performance ([4b9fc13](https://github.com/areias03/SPIREpy/commit/4b9fc13))
- Improved code formatting and consistency in test files ([072f10b](https://github.com/areias03/SPIREpy/commit/072f10b))

### Fixed
- Sample and study metadata URL handling ([c73b09d](https://github.com/areias03/SPIREpy/commit/c73b09d))
- Unit testing calls and expected URL ([d3e7ec3](https://github.com/areias03/SPIREpy/commit/d3e7ec3))
- Adapted unit tests to new function signatures ([e9e9e8c](https://github.com/areias03/SPIREpy/commit/e9e9e8c))
- `sample.get_mags()` now correctly reads genome metadata ([eaec357](https://github.com/areias03/SPIREpy/commit/eaec357))
- Import error resolution ([0e71aa4](https://github.com/areias03/SPIREpy/commit/0e71aa4))
- Double calls on methods ([febefaf](https://github.com/areias03/SPIREpy/commit/febefaf))
- Added pyarrow as required dependency for pandas to Polars conversion ([d96b148](https://github.com/areias03/SPIREpy/commit/d96b148))

### Removed
- Multithreading utilities ([e06f92a](https://github.com/areias03/SPIREpy/commit/e06f92a))
- Unnecessary comments in view.py ([072f10b](https://github.com/areias03/SPIREpy/commit/072f10b))

### Documentation
- Added comprehensive docstring for `get_contig_depths()` method ([0603ef6](https://github.com/areias03/SPIREpy/commit/0603ef6))
- Added function docstrings for better code documentation ([2f682f4](https://github.com/areias03/SPIREpy/commit/2f682f4))
- Better docstrings throughout the codebase ([6e4d027](https://github.com/areias03/SPIREpy/commit/6e4d027))
- Major improvements to documentation ([4424408](https://github.com/areias03/SPIREpy/commit/4424408))
- Fixes to Sphinx documentation generation ([b8f2314](https://github.com/areias03/SPIREpy/commit/b8f2314))
- Improvements to ReadTheDocs configuration ([afb917e](https://github.com/areias03/SPIREpy/commit/afb917e))
- Formatting improvements for Sphinx docstrings ([e25d7b7](https://github.com/areias03/SPIREpy/commit/e25d7b7))
- Added reference to Sample class ([77b684b](https://github.com/areias03/SPIREpy/commit/77b684b))
- Added citation to README with syntax fixes ([567c92e](https://github.com/areias03/SPIREpy/commit/567c92e))
- Improvements to README.md ([dac542a](https://github.com/areias03/SPIREpy/commit/dac542a))
- Added badges to README.md ([15ac08b](https://github.com/areias03/SPIREpy/commit/15ac08b))

### Testing
- Better unit and integration tests ([8d22854](https://github.com/areias03/SPIREpy/commit/8d22854))

## [0.1.0] - 2025-06-24

### Added
- Initial release of SPIREpy
- SPIRE wrapper and command-line tool for interacting with global microbiome data
- Study class for managing study-level data
- Sample class for managing sample-level data
- Genome class for managing genome-level data
- CLI interface with `spire` command
- Support for downloading MAGs (Metagenome-Assembled Genomes)
- AMR (Antimicrobial Resistance) annotations support
- Disk caching for large SPIRE data
- Comprehensive documentation with Sphinx
- Unit and integration tests with pytest
- Support for Python 3.9, 3.10, 3.11, 3.12, and 3.13

### Dependencies
- polars
- pandas
- rich
- joblib
- platformdirs

[Unreleased]: https://github.com/areias03/SPIREpy/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/areias03/SPIREpy/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/areias03/SPIREpy/releases/tag/v0.1.0
