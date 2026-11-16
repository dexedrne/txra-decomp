#!/usr/bin/env python3
"""Write tools/ios/TXRA.xcodeproj/project.pbxproj (the iPhone app's Xcode project).

    python3 tools/ios/make_project.py          write the project
    python3 tools/ios/make_project.py --check  fail if the committed project is out of date

Standard library only. Object IDs are derived from names, so the output is stable and the
committed project can be diffed. The app compiles runtime/*.c, runtime/ios/* and the
ROM-derived build/generated.c (made by recomp/generate.py from your own ROM); SDL2 is linked as
the static library tools/ios/build.sh builds from SDL's own Xcode project.
"""
import argparse
import hashlib
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROJECT = HERE / 'TXRA.xcodeproj' / 'project.pbxproj'
FRAMEWORKS = ['AudioToolbox', 'AVFoundation', 'CoreAudio', 'CoreGraphics', 'CoreHaptics', 'CoreMotion',
              'Foundation', 'GameController', 'Metal', 'OpenGLES', 'QuartzCore', 'UIKit']


def oid(*parts):
    return hashlib.md5('/'.join(('txra',) + parts).encode()).hexdigest()[:24].upper()


def q(value):
    if isinstance(value, (list, tuple)):
        return '(\n' + ''.join(f'\t\t\t\t\t{q(v)},\n' for v in value) + '\t\t\t\t)'
    value = str(value)
    if re.fullmatch(r'[A-Za-z0-9_./]+', value):
        return value
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'


def settings(d):
    return '{\n' + ''.join(f'\t\t\t\t{k} = {q(v)};\n' for k, v in sorted(d.items())) + '\t\t\t}'


def file_type(name):
    return {'.c': 'sourcecode.c.c', '.h': 'sourcecode.c.h', '.m': 'sourcecode.c.objc',
            '.plist': 'text.plist.xml', '.xcassets': 'folder.assetcatalog'}[Path(name).suffix]


def generate():
    runtime = sorted(p.name for p in (ROOT / 'runtime').glob('*.[ch]'))
    ios = sorted(p.name for p in (ROOT / 'runtime/ios').glob('*.[chm]'))
    groups = [('Runtime', [('../../runtime/' + n, n) for n in runtime]),
              ('iOS', [('../../runtime/ios/' + n, n) for n in ios]),
              ('Generated (from your ROM, not committed)', [('../../build/generated.c', 'generated.c')]),
              ('App', [('Info.plist', 'Info.plist'), ('Assets.xcassets', 'Assets.xcassets')])]
    objects = {}  # section -> list of (id, comment, body)

    def add(section, ident, comment, body):
        objects.setdefault(section, []).append((ident, comment, body))

    app = oid('product')
    sources, resources, group_ids = [], [], []
    for title, files in groups:
        children = []
        for path, name in files:
            ref = oid('file', path)
            tree = '"<group>"' if not path.startswith('../') else 'SOURCE_ROOT'
            add('PBXFileReference', ref, name,
                f'{{isa = PBXFileReference; lastKnownFileType = {file_type(name)}; name = {q(name)}; '
                f'path = {q(path)}; sourceTree = {tree}; }}')
            children.append((ref, name))
            if name.endswith(('.c', '.m')):
                build = oid('build', path)
                # The generated code is huge; -O1 like the Linux build (Makefile).
                extra = ' settings = {COMPILER_FLAGS = "-O1"; };' if name == 'generated.c' else ''
                add('PBXBuildFile', build, f'{name} in Sources',
                    f'{{isa = PBXBuildFile; fileRef = {ref} /* {name} */;{extra} }}')
                sources.append((build, name))
            elif name.endswith('.xcassets'):
                build = oid('build', path)
                add('PBXBuildFile', build, f'{name} in Resources',
                    f'{{isa = PBXBuildFile; fileRef = {ref} /* {name} */; }}')
                resources.append((build, name))
        gid = oid('group', title)
        kids = ''.join(f'\t\t\t\t{r} /* {n} */,\n' for r, n in children)
        add('PBXGroup', gid, title,
            f'{{\n\t\t\tisa = PBXGroup;\n\t\t\tchildren = (\n{kids}\t\t\t);\n\t\t\tname = {q(title)};\n'
            f'\t\t\tsourceTree = "<group>";\n\t\t}}')
        group_ids.append((gid, title))
    add('PBXFileReference', app, 'TXRA.app',
        '{isa = PBXFileReference; explicitFileType = wrapper.application; includeInIndex = 0; '
        'path = TXRA.app; sourceTree = BUILT_PRODUCTS_DIR; }')
    products = oid('group', 'Products')
    add('PBXGroup', products, 'Products',
        f'{{\n\t\t\tisa = PBXGroup;\n\t\t\tchildren = (\n\t\t\t\t{app} /* TXRA.app */,\n\t\t\t);\n'
        '\t\t\tname = Products;\n\t\t\tsourceTree = "<group>";\n\t\t}')
    main = oid('group', 'main')
    kids = ''.join(f'\t\t\t\t{g} /* {t} */,\n' for g, t in group_ids + [(products, 'Products')])
    add('PBXGroup', main, None,
        f'{{\n\t\t\tisa = PBXGroup;\n\t\t\tchildren = (\n{kids}\t\t\t);\n\t\t\tsourceTree = "<group>";\n\t\t}}')

    def phase(section, ident, name, files):
        listing = ''.join(f'\t\t\t\t{b} /* {n} */,\n' for b, n in files)
        add(section, ident, name,
            f'{{\n\t\t\tisa = {section};\n\t\t\tbuildActionMask = 2147483647;\n\t\t\tfiles = (\n{listing}'
            '\t\t\t);\n\t\t\trunOnlyForDeploymentPostprocessing = 0;\n\t\t}')
    src_phase, fw_phase, res_phase = oid('phase', 'sources'), oid('phase', 'frameworks'), oid('phase', 'resources')
    phase('PBXSourcesBuildPhase', src_phase, 'Sources', sources)
    phase('PBXFrameworksBuildPhase', fw_phase, 'Frameworks', [])
    phase('PBXResourcesBuildPhase', res_phase, 'Resources', resources)

    common = {
        'ALWAYS_SEARCH_USER_PATHS': 'NO',
        'ARCHS': 'arm64',
        'CLANG_ENABLE_MODULES': 'YES',
        'CLANG_ENABLE_OBJC_ARC': 'YES',
        # No signing at all: a signature would carry the signer's identity. Sideloading tools
        # sign the app with the player's own Apple ID.
        'CODE_SIGNING_ALLOWED': 'NO',
        'CODE_SIGNING_REQUIRED': 'NO',
        'CODE_SIGN_IDENTITY': '',
        'CODE_SIGN_STYLE': 'Manual',
        'DEVELOPMENT_TEAM': '',
        'DEBUG_INFORMATION_FORMAT': 'dwarf',
        'ENABLE_BITCODE': 'NO',
        'ENABLE_USER_SCRIPT_SANDBOXING': 'NO',
        'GCC_C_LANGUAGE_STANDARD': 'gnu11',
        'IPHONEOS_DEPLOYMENT_TARGET': '15.0',
        'ONLY_ACTIVE_ARCH': 'NO',
        'SDKROOT': 'iphoneos',
        'SUPPORTED_PLATFORMS': 'iphoneos iphonesimulator',
        'TARGETED_DEVICE_FAMILY': '1',
    }
    target = {
        'ASSETCATALOG_COMPILER_APPICON_NAME': 'AppIcon',
        'CURRENT_PROJECT_VERSION': '1',
        'DEAD_CODE_STRIPPING': 'YES',
        'GCC_PREPROCESSOR_DEFINITIONS': ['TXRA_IOS=1'],
        'GCC_WARN_64_TO_32_BIT_CONVERSION': 'NO',
        'GENERATE_INFOPLIST_FILE': 'NO',
        'HEADER_SEARCH_PATHS': ['$(TXRA_REPO)/runtime', '$(TXRA_REPO)/runtime/ios', '$(TXRA_SDL_SRC)/include'],
        'INFOPLIST_FILE': 'Info.plist',
        'MARKETING_VERSION': '1.2.0',
        # Same arithmetic as the PC builds: no fused multiply-add contraction (x86-64 has none),
        # and no build-machine paths in the binary.
        'OTHER_CFLAGS': ['-ffp-contract=off', '-ffile-prefix-map=$(TXRA_REPO)/=txra/',
                         '-ffile-prefix-map=$(TXRA_DEPS)/=deps/'],
        'OTHER_LDFLAGS': ['$(TXRA_SDL_LIB)/libSDL2.a', '-liconv'] +
                         [x for f in FRAMEWORKS for x in ('-framework', f)],
        'PRODUCT_BUNDLE_IDENTIFIER': 'beer.vyvanse.txra',
        'PRODUCT_NAME': 'TXRA',
        # tools/ios/build.sh passes absolute paths for these; the defaults suit an Xcode build
        # after build.sh has fetched and built SDL into build/ios/deps.
        'TXRA_REPO': '$(SRCROOT)/../..',
        'TXRA_DEPS': '$(TXRA_REPO)/build/ios/deps',
        'TXRA_SDL_SRC': '$(TXRA_DEPS)/SDL2-2.30.12',
        'TXRA_SDL_LIB': '$(TXRA_DEPS)/sdl-build/sym/Release-$(PLATFORM_NAME)',
        'WARNING_CFLAGS': ['-Wall', '-Wextra', '-Wno-misleading-indentation', '-Wno-unused-parameter'],
    }
    debug = {'GCC_OPTIMIZATION_LEVEL': '0', 'GCC_GENERATE_DEBUGGING_SYMBOLS': 'YES'}
    release = {'GCC_OPTIMIZATION_LEVEL': '2', 'GCC_GENERATE_DEBUGGING_SYMBOLS': 'NO',
               'DEPLOYMENT_POSTPROCESSING': 'YES', 'STRIP_INSTALLED_PRODUCT': 'YES', 'STRIP_STYLE': 'all',
               'COPY_PHASE_STRIP': 'YES', 'VALIDATE_PRODUCT': 'NO'}
    configs = {}
    for scope, base in (('project', common), ('target', target)):
        for name, extra in (('Debug', debug), ('Release', release)):
            ident = oid('config', scope, name)
            values = dict(base, **(extra if scope == 'target' else {}))
            add('XCBuildConfiguration', ident, name,
                f'{{\n\t\t\tisa = XCBuildConfiguration;\n\t\t\tbuildSettings = {settings(values)};\n'
                f'\t\t\tname = {name};\n\t\t}}')
            configs.setdefault(scope, []).append((ident, name))
    lists = {}
    for scope, label in (('project', 'PBXProject "TXRA"'), ('target', 'PBXNativeTarget "TXRA"')):
        ident = oid('configlist', scope)
        items = ''.join(f'\t\t\t\t{i} /* {n} */,\n' for i, n in configs[scope])
        add('XCConfigurationList', ident, f'Build configuration list for {label}',
            f'{{\n\t\t\tisa = XCConfigurationList;\n\t\t\tbuildConfigurations = (\n{items}\t\t\t);\n'
            '\t\t\tdefaultConfigurationIsVisible = 0;\n\t\t\tdefaultConfigurationName = Release;\n\t\t}')
        lists[scope] = ident
    tgt = oid('target', 'TXRA')
    add('PBXNativeTarget', tgt, 'TXRA',
        f'{{\n\t\t\tisa = PBXNativeTarget;\n\t\t\tbuildConfigurationList = {lists["target"]};\n'
        f'\t\t\tbuildPhases = (\n\t\t\t\t{src_phase} /* Sources */,\n\t\t\t\t{fw_phase} /* Frameworks */,\n'
        f'\t\t\t\t{res_phase} /* Resources */,\n\t\t\t);\n\t\t\tbuildRules = (\n\t\t\t);\n'
        '\t\t\tdependencies = (\n\t\t\t);\n\t\t\tname = TXRA;\n\t\t\tproductName = TXRA;\n'
        f'\t\t\tproductReference = {app} /* TXRA.app */;\n'
        '\t\t\tproductType = "com.apple.product-type.application";\n\t\t}')
    proj = oid('project')
    add('PBXProject', proj, 'Project object',
        f'{{\n\t\t\tisa = PBXProject;\n\t\t\tattributes = {{\n\t\t\t\tBuildIndependentTargetsInParallel = 1;\n'
        '\t\t\t\tLastUpgradeCheck = 2700;\n\t\t\t};\n'
        f'\t\t\tbuildConfigurationList = {lists["project"]};\n\t\t\tcompatibilityVersion = "Xcode 14.0";\n'
        '\t\t\tdevelopmentRegion = en;\n\t\t\thasScannedForEncodings = 0;\n'
        '\t\t\tknownRegions = (\n\t\t\t\ten,\n\t\t\t\tBase,\n\t\t\t);\n'
        f'\t\t\tmainGroup = {main};\n\t\t\tproductRefGroup = {products} /* Products */;\n'
        '\t\t\tprojectDirPath = "";\n\t\t\tprojectRoot = "";\n'
        f'\t\t\ttargets = (\n\t\t\t\t{tgt} /* TXRA */,\n\t\t\t);\n\t\t}}')

    out = ['// !$*UTF8*$!\n{\n\tarchiveVersion = 1;\n\tclasses = {\n\t};\n\tobjectVersion = 56;\n\tobjects = {\n']
    for section in sorted(objects):
        out.append(f'\n/* Begin {section} section */\n')
        for ident, comment, body in sorted(objects[section]):
            label = f' /* {comment} */' if comment else ''
            out.append(f'\t\t{ident}{label} = {body};\n')
        out.append(f'/* End {section} section */\n')
    out.append(f'\t}};\n\trootObject = {proj} /* Project object */;\n}}\n')
    return ''.join(out)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--check', action='store_true')
    a = p.parse_args()
    text = generate()
    if a.check:
        if not PROJECT.is_file() or PROJECT.read_text() != text:
            sys.exit('tools/ios/TXRA.xcodeproj is out of date: run python3 tools/ios/make_project.py')
        print('Xcode project is up to date')
        return
    PROJECT.parent.mkdir(parents=True, exist_ok=True)
    PROJECT.write_text(text)
    print(PROJECT.relative_to(ROOT))


if __name__ == '__main__':
    main()
