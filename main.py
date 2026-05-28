import argparse
from tkinter import *
from src.gui import PDFViewer


def parse_arguments(args=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Open the PDF viewer")

    parser.add_argument(
        "file",
        type=str,
        nargs="?",
        default=None,
        help="input pdf file"
    )

    parser.add_argument(
        "-e",
        "--extract",
        type=str,
        help="extract a range of pages inclusive x-y"
    )

    return parser.parse_args(args)


def main():
    args = parse_arguments()
    # print(args.file)
    # print(args.extract)

    root = Tk()
    root.option_add('*TCombobox*Listbox.font', ('Arial', 14))
    root.attributes('-zoomed', True)
    app = PDFViewer(root, args.file)
    root.mainloop()

if __name__ == '__main__':
    main()
