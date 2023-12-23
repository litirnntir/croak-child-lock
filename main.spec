# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/blocked_apps.json', 'jsons'),
    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/blocked_apps_for_percents.json', 'jsons'),
    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/stats_apps.json', 'jsons'),
    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/settings.json', 'jsons'),
    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/background.png', 'images'),
    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/key.key', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/croak-logo.icns'],
)
app = BUNDLE(
    exe,
    name='main.app',
    icon='/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/croak-logo.icns',
    bundle_identifier=None,
)
