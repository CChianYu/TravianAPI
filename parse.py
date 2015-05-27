def getStrBetween(s, fron, back):

    s = s.strip()
    if fron != '':
        i = s.find(fron)
        s = s[i+len(fron):]
    if back != '':
        i = s.find(back)
        s = s[:i]
    s = s.strip()

    return s
