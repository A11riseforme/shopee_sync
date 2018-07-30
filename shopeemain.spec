# -*- mode: python -*-

block_cipher = None


a = Analysis(['shopeemain.py'],
             pathex=['C:\\Users\\woon.zhenhao\\.spyder-py3\\shopee'],
             binaries=[],
             datas=[(".\\log.py","."),('.\\apiconnector.py','.'),('.\\keys.py','.'),('.\\masterReader.py','.'),('.\\prodmanagement.py','.'),('.\\ordermanagement.py','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='shopeemain',
          debug=True,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='shopeemain')
