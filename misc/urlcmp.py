# Author github.com/n0mi1k
# A simple tool to compare 2 txt files and return lines found in second_file but not in first file
# Great for comparing for new URLs
import sys

def read_file(file_path):
    with open(file_path, 'r') as f:
        urls = set(line.strip() for line in f.readlines())
    return urls

def main():
    first_file = sys.argv[1]
    second_file = sys.argv[2]

    urls_set_1 = read_file(first_file)
    urls_set_2 = read_file(second_file)

    difference = urls_set_2.difference(urls_set_1)

    if difference:
        print("\nURLs found in the second file but not in the first file:")
        for url in difference:
            print(url)
    else:
        print("No URLs were found in the second file that are not in the first file.")

if __name__ == "__main__":
    main()