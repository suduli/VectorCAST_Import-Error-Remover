# VectorCAST Test File Content Cleaner

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust Python utility designed to clean VectorCAST C test files by removing import failure blocks while preserving file structure and integrity. This tool is essential for VectorCAST test environment maintenance and automated test processing workflows.

## 🚀 Features

- **Smart Content Removal**: Precisely removes `TEST.IMPORT_FAILURES:` to `TEST.END_IMPORT_FAILURES:` blocks
- **File Integrity**: Preserves original file structure and formatting
- **Backup Protection**: Automatic backup creation before file modification
- **Batch Processing**: Support for cleaning multiple files simultaneously
- **Error Handling**: Comprehensive error handling with detailed logging
- **CLI Interface**: Both interactive and command-line modes
- **Unicode Support**: Handles various text encodings gracefully

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Standard Python libraries (no additional dependencies required)

### Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/vectorcast-content-cleaner.git
cd vectorcast-content-cleaner

# Make the script executable (optional)
chmod +x content_cleaner.py
```

## 📖 Usage

### Interactive Mode
```bash
python content_cleaner.py
```

### Command Line Mode
```bash
# Clean a single file
python content_cleaner.py test_file.c

# Clean multiple files
python content_cleaner.py file1.c file2.c file3.c

# Clean without creating backups
python content_cleaner.py test_file.c --no-backup

# Enable verbose logging
python content_cleaner.py test_file.c --verbose
```

### Command Line Options
```
positional arguments:
  files              File(s) to clean. If not provided, will prompt for input

optional arguments:
  -h, --help         Show help message and exit
  --no-backup        Don't create backup files
  --verbose, -v      Enable verbose logging
  --version          Show program's version number and exit
```

## 🔧 How It Works

The cleaner uses advanced regular expressions to identify and remove content blocks that match the VectorCAST import failure pattern:

```c
// This content will be removed:
TEST.IMPORT_FAILURES:
    Any content here including
    multiple lines and special characters
TEST.END_IMPORT_FAILURES:
```

### Algorithm Details
1. **Pattern Recognition**: Uses regex with multiline and dotall flags for accurate matching
2. **Content Preservation**: Maintains surrounding code structure and whitespace
3. **Cleanup Process**: Removes excessive whitespace that might result from block removal
4. **Validation**: Checks file permissions and encoding before processing

## 🎯 VectorCAST Integration

### Why This Tool Is Important for VectorCAST

VectorCAST is a comprehensive C/C++ software testing platform used for:
- **Unit Testing**: Automated test case generation and execution
- **Integration Testing**: Component-level testing with coverage analysis
- **Certification**: DO-178B/C, ISO 26262, and other safety-critical standards compliance

#### The Problem This Tool Solves

During VectorCAST test execution, import failure blocks are automatically generated when:
- Header files cannot be properly parsed
- Dependencies are missing or misconfigured
- Compilation issues occur during test environment setup

These blocks accumulate in test files and can cause:
- **Test Environment Corruption**: Preventing proper test regeneration
- **Build Failures**: Interfering with subsequent test compilation
- **Maintenance Issues**: Making test files difficult to manage and version control
- **CI/CD Pipeline Breaks**: Causing automated testing workflows to fail

#### Business Impact

| Challenge | Impact | Solution with This Tool |
|-----------|---------|-------------------------|
| **Manual Cleanup** | Hours of manual editing | **Automated Processing** |
| **Error-Prone Process** | Risk of removing critical code | **Precise Pattern Matching** |
| **Team Productivity** | Delayed test cycles | **Batch Processing Capability** |
| **Quality Assurance** | Inconsistent test environments | **Reliable, Repeatable Cleaning** |

### Use Cases in VectorCAST Workflows

1. **Test Environment Reset**: Clean corrupted test files before regeneration
2. **CI/CD Integration**: Automated cleanup in build pipelines
3. **Migration Projects**: Prepare test files when moving between VectorCAST versions
4. **Maintenance Scripts**: Regular cleanup of test repositories
5. **Development Workflows**: Quick cleanup during active test development

## 📊 Performance & Reliability

- **Fast Processing**: Optimized regex patterns for quick file processing
- **Memory Efficient**: Processes files without loading entire content into memory unnecessarily
- **Error Recovery**: Graceful handling of encoding issues and file permission problems
- **Backup Safety**: Automatic backup creation prevents data loss

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=content_cleaner --cov-report=html
```

## 📁 Project Structure

```
vectorcast-content-cleaner/
│
├── content_cleaner.py          # Main application
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_content_cleaner.py
│   └── test_data/             # Test files
├── .github/
│   └── workflows/
│       └── python-package.yml # CI/CD pipeline
├── .gitignore                 # Git ignore rules
├── LICENSE                    # CC0 License
├── README.md                  # This file
└── requirements-dev.txt       # Development dependencies
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linting
flake8 content_cleaner.py

# Run tests
pytest
```

### Code Style
This project follows PEP 8 guidelines and uses `flake8` for linting.

## 📈 Use in Professional Profile

This project demonstrates several key technical competencies:

### Technical Skills Demonstrated
- **Python Development**: Advanced string processing, regex, and file handling
- **Software Testing**: Experience with VectorCAST and test automation
- **DevOps Integration**: CI/CD pipeline setup and automated testing
- **Error Handling**: Robust error management and logging practices
- **Documentation**: Professional-grade documentation and code comments

### Industry Applications
- **Automotive**: Safety-critical software testing (ISO 26262)
- **Aerospace**: DO-178B/C compliance testing
- **Medical Devices**: IEC 62304 software lifecycle processes
- **Industrial Control**: Functional safety testing and validation

## 📄 License

This project is released into the public domain under the CC0 1.0 Universal license. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission.

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/suduli/vectorcast-content-cleaner/issues) section
2. Create a new issue with detailed description
3. For urgent matters, contact: [suduli.office@gmail.com]

---

**⭐ If this tool helped you, please consider giving it a star!**

*Built with ❤️ for the VectorCAST testing community*
