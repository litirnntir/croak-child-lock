# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['main.py'],
             pathex=['/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock'],
             binaries=[],
             datas=[('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/blocked_apps.json', 'jsons'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/codes.json', 'jsons'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/blocked_apps_for_percents.json', 'jsons'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/stats_apps.json', 'jsons'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/jsons/settings.json', 'jsons'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/background.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/background_settings.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/error1.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/error2.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/error3.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/error4.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/error5.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/error6.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/success1.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/success2.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/success3.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/success4.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/success5.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/success6.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/croak-logo.png', 'images'),
                    ('/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/key.key', '.')],

             hiddenimports=['PyQt6.Qt6Svg', 'PyQt6.Qt6Widgets', 'PyQt6.Qt6Gui', 'PyQt6.QtCore', 'PyQt6.QtWidgets'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Croak',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/croak-logo.ico')

app = BUNDLE(
    exe,
    name='Croak.app',
    icon='/Users/aleksandragorbuncova/PycharmProjects/croak-child-lock/images/croak-logo.icns',
    bundle_identifier=None,
)
