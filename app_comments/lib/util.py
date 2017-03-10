import json


class Printer:

    def pp(s, data, keys=False):
        if keys:
            if isinstance(data, list):
                print('Is list...')
                print(data[0].keys())
            else:
                for k in sorted(list(data.keys())):
                    print(k)
        else:
            print(json.dumps(data, indent=4, sort_keys=True))

    def print_text(s, text, length=100, begin_tabs=0):
        if len(text) < length:
            print(('\t'*begin_tabs)+text)
            return

        while True:
            beg = text[:length]
            print(('\t'*begin_tabs)+beg)
            text = text[length:]
            if len(text) <= length:
                print(('\t'*begin_tabs)+text)
                break


# def get_json_link(url):
#     if not url:
#         raise Exception('No link provided.')
#     if url and url[-5:] != '.json':
#         return url[:-1] + '.json'
#     raise Exception('Wrong link format')


def get_json_link(url):
    if not url:
        raise Exception('No link provided.')

    if url[-1] == '/':
        new_url = url[:-1] + '.json'
    elif '?' in url:
        basic_url = get_basic_link(url)
        new_url = get_json_link(basic_url)
    else:
        new_url += '.json'
    return new_url


def get_basic_link(url):
    orig_url = url[:]
    if '?' in url:
        url = url.split('?')[0]
    return url
