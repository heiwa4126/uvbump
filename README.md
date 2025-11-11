# uvbump

[![PyPI - Version](https://img.shields.io/pypi/v/uvbump.svg)](https://pypi.org/project/uvbump)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uvbump.svg)
![Last Commit](https://img.shields.io/github/last-commit/heiwa4126/uvbump)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 設計書

Astral uv (や poetry 等 PEP 621)の pyproject.toml に対して `npm version` に似た CLI "uvbump" を Python で作りたい。

usage:
uvbump[<newversion> | major | minor | patch | bump][-t][--dry-run][-h|--help]

- デフォルトは `uvbump bump` に等価
- cwd に pyproject.toml がない、または project.version がない、project.version が PEP440 でない場合はエラー
- 直接指定できるバージョン(<newversion>)は PEP440 に従う。従っていない場合はエラー。また同じバージョンとダウングレードは許可しない
  - ダウングレード例: `1.0.0` > `1.0.0a1`
- major | minor | patch はそれぞれの major バージョン、minor バージョン、patch バージョンを 1 つ増やす
- bump は元のバージョンが pre バージョンでない場合は patch と等価(例えば 0.0.1->0.0.2)
- bump は元のバージョンが pre バージョンの場合は pre-release number を 1 つ増やす。(例えば 1.2.3a4->1.2.3a5)
- pre バージョンから通常バージョン、あるいはその逆は major | minor | patch | bump ではできない。newversion を明示的に指定すること
- git の操作は GitPython を使う
- npm version 同様 、事前にコミットされていない場合はエラー。unstaged files, staged changes がある場合も安全のためエラー。
- git repositoryでない場合はエラー
- .gitignoreされたファイルは無視
- npm version 同様、pyproject.toml の project.version を書き換えたのちコミットしてタグをつける
  - コミットメッセージは `{新しいversion}`
  - タグは `-t` オプションで `test-{新しいversion}`, -t オプションがない場合は `v{新しいversion}`をつける
- git push はしない
- 対象となった pyproject.toml のパス、前バージョン文字列、変更後バージョン文字列、コミットメッセージ、タグを表示する
- `--dry-run` オプションがある。表示のみで変更を行わない
- uvbumpの設定ファイルはいまのところ無し
- monorepo対応はそのうち
