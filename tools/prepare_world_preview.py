"""Historical preview packaging is retired; use the separate World product."""


def prepare():
    raise RuntimeError('Use tools/prepare_editions.py --edition world --output <fresh-directory>')


if __name__ == '__main__':
    prepare()
