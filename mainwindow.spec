# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['mainwindow.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('mainwindow.ui','.'),
        ('rc_Resources.py', '.'),
        ('TrapCam.pyproject', '.'),
        ('TrapCam.pyproject.user', '.'),
        ('ui_form.py', '.'),
        ('ui_mainwindow.py', '.'),
        ('beta.db', '.'),
        ('Program', 'Program'),
        ('models', 'models'),
        ('md_visualization', 'md_visualization'),
        ('md_utils', 'md_utils'),
        ('input', 'input'),
        ('icons', 'icons'),
        ('exports', 'exports'),
        ('detectionLogs', 'detectionLogs'),
        ('detection', 'detection'),
        ('data_management', 'data_management'),
        ('cropped', 'cropped'),
    ],
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
    [],
    exclude_binaries=True,
    name='mainwindow',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mainwindow',
)
app = BUNDLE(
    coll,
    name='TrapCam.app',
    icon=None,
    bundle_identifier=None,
)
