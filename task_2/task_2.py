"""
Find value by keys in json file
"""
import json


def read_file(path_to_file):
    """
    Read information from file
    :return: content of file
    """
    with open(path_to_file, encoding='utf-8') as file:
        content = file.read()
    content = json.loads(content)
    return content


def get_values(content, key):
    """
    Get value from json file by key
    :param content: content of json file
    :param key: key by which it find element
    :return: value
    >>> get_values(read_file("twitter_api.json"), "meta")
    """
    return content[key]


def main():
    """
    Main function
    :return:
    """
    path_to_file = input("Path to json file: ")
    content = read_file(path_to_file)
    key = input(f"Chose key ({', '.join(content)}): ")
    while True:
        if isinstance(get_values(content, key), list):
            content = get_values(content, key)
            key = int(input(f"Chose element from list of {len(content)} "
                            f"elements: "))
        elif isinstance(get_values(content, key), dict):
            content = get_values(content, key)
            key = input(f"Chose key one more time ({', '.join(content)}): ")
        else:
            print(get_values(content, key))
            break


if __name__ == "__main__":
    main()
