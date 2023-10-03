import re


def clean_file_content(content):
    """Remove content between specific patterns without affecting surrounding lines."""
    # The regex captures everything between TEST.IMPORT_FAILURES: and TEST.END_IMPORT_FAILURES:
    # without removing the newline before TEST.IMPORT_FAILURES: and after TEST.END_IMPORT_FAILURES:
    regex = r"TEST.IMPORT_FAILURES:[\S\s]+?TEST.END_IMPORT_FAILURES:"
    return re.sub(regex, "", content, flags=re.MULTILINE)


def main():
    file_path = input("Enter the path of C file: ")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cleaned_content = clean_file_content(content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_content)


if __name__ == "__main__":
    main()
