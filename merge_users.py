# coding=utf-8
import os
import re
from distutils import dir_util


def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f


def movefiles(nls):
    while nls[0] != nls[-1]:
        dir_util.copy_tree(nls[-1][1], nls[0][1], verbose=1)
        dir_util.remove_tree(nls[-1][1], verbose=1)
        nls.pop(-1)


def dirmerge(top, ls):
    print len(ls), ls
    nls = []
    for l in ls:
        pn = os.path.join(top, l)
        mod = os.stat(pn).st_mtime
        nls.append((mod, pn))
    nls.sort(key=lambda tp: tp[0], reverse=True)
    movefiles(nls)


def merge_dup_users(top, d):
    m = re.compile(('(\d+)\s.+'))
    cur = next(d, None)
    ls = []
    count = 0
    while True:
        nex = next(d, None)
        if not nex:
            break
        ls.append(cur)
        if m.match(cur).group(1) != m.match(nex).group(1):
            if len(ls) > 1:
                count += len(ls)
                dirmerge(top, ls)
            ls = []
        cur = nex
    print 'Numbers of dupe folders:', count


def del_dup_files(top, d):
    matcher = re.compile('^(\d+)(.*p)*(\d*) -')
    while True:
        cur = next(d, None)
        if cur:
            print cur
            for root, dirs, files in os.walk(os.path.join(top, cur)):
                for f in files:
                    m = matcher.match(f)
                    if '.txt' in f:
                        print 'FILE [', f, ']'
                    if m:
                        print m.group(0), '|', m.group(1), '|', m.group(2), '|', m.group(3)
                        continue
                    else:
                        print '^NOTFOUND^NOTFOUND^NOTFOUND^NOTFOUND^NOTFOUND^'
        else:
            break


def main():
    top = os.path.join(os.getcwd(), 'Pixiv')
    d = listdir_nohidden(top)
    merge_dup_users(top, d)
    # del_dup_files(top2, d2)


if __name__ == "__main__":
    main()
