#!/usr/bin/python

import re
import os
import os.path

def fix_qhp(cwd):
    keyword  = re.compile('^(\s*)\<keyword name="(.*\(C\+\+.+\))" ref="\(u\'(.+)\', u\'(.+)\'\)"\/>\s*$')
    refclean = re.compile('[^0-9a-zA-Z._\-#/\\\\~\[\]\=]')
    refrepl = '_'
    files = {} # files to fix

    def repl(m):
        indent, name, id, ref = m.groups()

        if '#' in ref:
            filename, refhash = ref.split('#', 1)

            refhash = refhash.replace('&', '&amp;')
            cleanhash = refclean.sub('_', refhash)
            ref = '#'.join([filename, cleanhash])

            if filename in files:
                files[filename] |= {(refhash, cleanhash)}
            else:
                files[filename] = {(refhash, cleanhash)}

        id = id.replace('<', '&lt;')
        id = id.replace('>', '&gt;')

        ret = '{0}<keyword name="{1}" id="cv::{2}" ref="{3}"/>\n'.format(indent, name, id, ref)
        ret += '{0}<keyword name="{1}" id="{2}" ref="{3}"/>\n'.format(indent, name, id, ref)
        return ret

    ret = ''
    qhp_path = os.path.join(cwd, 'OpenCV.qhp')
    with open(qhp_path, 'r') as f:
        for line in f:
            if '<keyword ' in line:
                line, n = keyword.subn(repl, line)
                if not n:
                    continue

            ret += line

    with open(qhp_path, 'w') as f:
        f.write(ret)

    for fn, fixset in files.items():
        fn = os.path.join(cwd, fn)
        tfn = fn + '.tmp'

        with open(fn, 'r') as f:
            with open(tfn, 'w') as out:
                data = f.read()
                for refhash, cleanhash in fixset:
                    data = data.replace(refhash, cleanhash)
                out.write(data)

        os.rename(tfn, fn)



def merge_css(src, dst, skip):
    if not os.path.exists(src):
        return

    with open(src, 'a') as fsrc:
        with open(dst, 'r') as fdst:
            # skip header and @import url('basic.css');
            for x in range(skip):
                fdst.readline()

            fsrc.write('\n')
            fsrc.write(fdst.read())

    os.rename(src, dst)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('targets',
            metavar = 'path',
            nargs = 1,
            help = 'path to generated qthelp docs')

    options = parser.parse_args()
    target = options.targets[0]
    docsdir = os.path.abspath(target)
    if os.path.exists(docsdir):
        bcss, dcss = [os.path.join(docsdir, '_static', f) for f in ['basic.css', 'default.css']]
        merge_css(bcss, dcss, skip=6)
        fix_qhp(docsdir)
