#!/usr/bin/env python3
"""
VectorCAST Test File Content Cleaner

A utility for cleaning C test files by removing specific content blocks
between TEST.IMPORT_FAILURES: and TEST.END_IMPORT_FAILURES: markers.
This is particularly useful for VectorCAST test environments where
import failure sections need to be cleaned for reprocessing.

Author: [Your Name]
Version: 1.0.0
License: CC0 1.0 Universal
"""

import re
import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ContentCleaner:
    """
    A class to handle cleaning of C test files by removing specific content blocks.
    
    This cleaner is designed to work with VectorCAST test files, removing
    import failure sections while preserving file structure and formatting.
    """
    
    def __init__(self):
        """Initialize the ContentCleaner with default patterns."""
        self.start_pattern = r"TEST\.IMPORT_FAILURES:"
        self.end_pattern = r"TEST\.END_IMPORT_FAILURES:"
        self.full_pattern = rf"{self.start_pattern}[\s\S]*?{self.end_pattern}"
        
    def clean_content(self, content: str) -> str:
        """
        Remove content between TEST.IMPORT_FAILURES: and TEST.END_IMPORT_FAILURES: markers.
        
        Args:
            content (str): The file content to clean
            
        Returns:
            str: Cleaned content with import failure blocks removed
            
        Example:
            >>> cleaner = ContentCleaner()
            >>> content = "some code\\nTEST.IMPORT_FAILURES:\\nbad code\\nTEST.END_IMPORT_FAILURES:\\nmore code"
            >>> cleaner.clean_content(content)
            'some code\\nmore code'
        """
        try:
            # Remove the content blocks while preserving surrounding structure
            cleaned = re.sub(self.full_pattern, "", content, flags=re.MULTILINE | re.DOTALL)
            
            # Clean up any excessive whitespace that might result
            cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
            
            return cleaned
            
        except re.error as e:
            logger.error(f"Regex error during content cleaning: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during content cleaning: {e}")
            raise
    
    def validate_file(self, file_path: Path) -> bool:
        """
        Validate that the file exists and is readable.
        
        Args:
            file_path (Path): Path to the file to validate
            
        Returns:
            bool: True if file is valid, False otherwise
        """
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
            
        if not file_path.is_file():
            logger.error(f"Path is not a file: {file_path}")
            return False
            
        if not os.access(file_path, os.R_OK | os.W_OK):
            logger.error(f"File is not readable/writable: {file_path}")
            return False
            
        return True
    
    def count_blocks(self, content: str) -> int:
        """
        Count the number of import failure blocks in the content.
        
        Args:
            content (str): Content to analyze
            
        Returns:
            int: Number of blocks found
        """
        matches = re.findall(self.full_pattern, content, flags=re.MULTILINE | re.DOTALL)
        return len(matches)
    
    def clean_file(self, file_path: str, backup: bool = True) -> bool:
        """
        Clean a single file by removing import failure blocks.
        
        Args:
            file_path (str): Path to the file to clean
            backup (bool): Whether to create a backup before cleaning
            
        Returns:
            bool: True if cleaning was successful, False otherwise
        """
        path = Path(file_path)
        
        if not self.validate_file(path):
            return False
        
        try:
            # Read the original content
            logger.info(f"Reading file: {path}")
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                original_content = f.read()
            
            # Count blocks before cleaning
            block_count = self.count_blocks(original_content)
            if block_count == 0:
                logger.info("No import failure blocks found in file")
                return True
                
            logger.info(f"Found {block_count} import failure block(s)")
            
            # Create backup if requested
            if backup:
                backup_path = path.with_suffix(path.suffix + '.bak')
                logger.info(f"Creating backup: {backup_path}")
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
            
            # Clean the content
            cleaned_content = self.clean_content(original_content)
            
            # Write cleaned content back to file
            logger.info(f"Writing cleaned content to: {path}")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            logger.info(f"Successfully cleaned {block_count} import failure block(s)")
            return True
            
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error: {e}")
            return False
        except IOError as e:
            logger.error(f"IO error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False
    
    def clean_multiple_files(self, file_paths: List[str], backup: bool = True) -> dict:
        """
        Clean multiple files and return results.
        
        Args:
            file_paths (List[str]): List of file paths to clean
            backup (bool): Whether to create backups
            
        Returns:
            dict: Results summary with success/failure counts
        """
        results = {"success": 0, "failed": 0, "files": []}
        
        for file_path in file_paths:
            logger.info(f"Processing file: {file_path}")
            success = self.clean_file(file_path, backup)
            
            results["files"].append({
                "path": file_path,
                "success": success
            })
            
            if success:
                results["success"] += 1
            else:
                results["failed"] += 1
        
        return results


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Clean VectorCAST test files by removing import failure blocks",
        epilog="Example: python content_cleaner.py test_file.c --no-backup"
    )
    
    parser.add_argument(
        "files",
        nargs="*",
        help="File(s) to clean. If not provided, will prompt for input"
    )
    
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup files"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="VectorCAST Content Cleaner 1.0.0"
    )
    
    return parser


def interactive_mode() -> Optional[str]:
    """
    Run in interactive mode to get file path from user.
    
    Returns:
        Optional[str]: File path entered by user, or None if cancelled
    """
    try:
        print("\n=== VectorCAST Test File Content Cleaner ===")
        print("This tool removes TEST.IMPORT_FAILURES blocks from C test files\n")
        
        file_path = input("Enter the path to the C file to clean (or 'q' to quit): ").strip()
        
        if file_path.lower() in ['q', 'quit', 'exit']:
            print("Operation cancelled.")
            return None
            
        if not file_path:
            print("No file path provided.")
            return None
            
        return file_path
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return None


def main():
    """Main function to handle command line execution."""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    cleaner = ContentCleaner()
    
    # Determine files to process
    if args.files:
        file_paths = args.files
    else:
        # Interactive mode
        file_path = interactive_mode()
        if not file_path:
            sys.exit(0)
        file_paths = [file_path]
    
    # Process files
    backup = not args.no_backup
    
    if len(file_paths) == 1:
        # Single file processing
        success = cleaner.clean_file(file_paths[0], backup)
        sys.exit(0 if success else 1)
    else:
        # Multiple file processing
        results = cleaner.clean_multiple_files(file_paths, backup)
        
        print(f"\n=== Results Summary ===")
        print(f"Successfully processed: {results['success']} files")
        print(f"Failed to process: {results['failed']} files")
        
        if results['failed'] > 0:
            print("\nFailed files:")
            for file_info in results['files']:
                if not file_info['success']:
                    print(f"  - {file_info['path']}")
        
        sys.exit(0 if results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
