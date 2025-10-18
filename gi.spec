# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gi_standalone.py'],
    pathex=[],
    binaries=[],
    datas=[('gi', 'gi')],
    hiddenimports=[
        'gi.cli',
        'gi.combine', 
        'gi.fetch',
        'gi.names',
        'gi.util',
        'typer',
        'rich',
        'requests',
        'platformdirs',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['gi'],  # Exclude PyGObject gi module
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='gi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)