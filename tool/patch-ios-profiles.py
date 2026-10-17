import re, sys
path, app, share, action = sys.argv[1:5]
s = open(path).read()
pattern = re.compile(r'(\w+ /\* (?:Debug|Release|Profile) \*/ = \{\s*isa = XCBuildConfiguration;.*?\n\t\t\};)', re.S)
def patch(m):
    block = m.group(1)
    mb = re.search(r'PRODUCT_BUNDLE_IDENTIFIER = ([^;]+);', block)
    if not mb:
        return block
    bundle = mb.group(1).strip().strip('"')
    uuid = None
    if bundle.endswith('.ShareExtension'): uuid = share
    elif bundle.endswith('.ActionExtension'): uuid = action
    elif bundle == 'cn.clawsouls.ficusvirens': uuid = app
    if not uuid:
        return block
    block = re.sub(r'\n\t\t\t\tPROVISIONING_PROFILE_SPECIFIER = [^;]*;', '', block)
    block = block.replace('CODE_SIGN_STYLE = Automatic;', 'CODE_SIGN_STYLE = Manual;')
    return block.replace('\n\t\t\t};', '\n\t\t\t\tPROVISIONING_PROFILE_SPECIFIER = ' + uuid + ';\n\t\t\t};', 1)
s2 = pattern.sub(patch, s)
open(path, 'w').write(s2)
print('patched specifiers:', s2.count('PROVISIONING_PROFILE_SPECIFIER'))
