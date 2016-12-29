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
