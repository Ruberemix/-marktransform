# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('icon.ico', '.'),
        (
            r'C:\Users\RUben\AppData\Roaming\Python\Python313\site-packages\magika',
            'magika',
        ),
        (
            r'C:\Users\RUben\AppData\Roaming\Python\Python313\site-packages\customtkinter',
            'customtkinter',
        ),
    ],
    hiddenimports=[
        'markitdown',
        'markitdown.converters',
        'markitdown.converters._pdf_converter',
        'markitdown.converters._docx_converter',
        'markitdown.converters._xlsx_converter',
        'markitdown.converters._pptx_converter',
        'markitdown.converters._html_converter',
        'markitdown.converters._image_converter',
        'markitdown.converters._audio_converter',
        'markitdown.converters._csv_converter',
        'markitdown.converters._plain_text_converter',
        'markitdown.converters._epub_converter',
        'markitdown.converters._zip_converter',
        'markitdown.converters._youtube_converter',
        'markitdown.converters._rss_converter',
        'markitdown.converters._ipynb_converter',
        'markitdown.converters._markdownify',
        'customtkinter',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'pyperclip',
        'beautifulsoup4',
        'charset_normalizer',
        'defusedxml',
        'magika',
        'markdownify',
        'requests',
        'pdfminer',
        'pdfminer.high_level',
        'docx',
        'openpyxl',
        'pptx',
        'charset_normalizer.md__mypyc',
        'numpy',
        'numpy.core',
        'numpy.core._multiarray_umath',
        'onnxruntime',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas', 'scipy', 'jupyter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MarkTransform',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
    version_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MarkTransform',
)
