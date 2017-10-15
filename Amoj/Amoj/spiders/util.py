

def safeget(l, index, default=None):
    try:
        return l[index]
    except (IndexError, TypeError):
        return default


def info_to_dict(info):
    if 'Kindle电子书' in info:
        kindle = safeget(info, info.index('Kindle电子书') + 1)
        if kindle == '\n    ':
            kindle = None
    else:
        kindle = None
    if '平装' in info:
        papercover = safeget(info, info.index('平装') + 1)
        if papercover == '\n    ':
            papercover = None
    else:
        papercover = None
    if '精装' in info:
        hardcover = safeget(info, info.index('精装') + 1)
        if hardcover == '\n    ':
            hardcover = None
    else:
        hardcover = None
    if '更多购买选择' in info:
        morechoices = safeget(info, info.index('更多购买选择') + 1)
        if morechoices == '\n    ':
            morechoices = None
    else:
        morechoices = None
    if '\n\n' in info:
        comments = safeget(info, info.index('\n\n') + 1)
    else:
        comments = None

    return {'kindle': kindle, 'papercover': papercover, 'hardcover': hardcover, 'morechoices': morechoices,
            'comments': comments}