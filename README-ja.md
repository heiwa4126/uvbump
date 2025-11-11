# uvbump

[![PyPI - Version](https://img.shields.io/pypi/v/uvbump.svg)](https://pypi.org/project/uvbump)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uvbump.svg)
![Last Commit](https://img.shields.io/github/last-commit/heiwa4126/uvbump)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](https://github.com/heiwa4126/uvbump/blob/main/README.md) | 日本語

`npm version` に似た CLI を Python で書いたもの。参考: [npm-version](https://docs.npmjs.com/cli/v11/commands/npm-version)

Astral uv (や poetry 等 PEP 621 準拠)の pyproject.toml に対して
`npm version`
同様の処理を行う。主に GitHub Actions の発火に使用する。

## インストールと実行方法

```sh
# uv を使用する場合
uv add uvbump --dev
uv run uvbump <オプション>

# または
uvx uvbump <オプション>

# または
uv tool install uvbump
uvbump

# pip を使用する場合
pip install uvbump
uvbump

# poetry の場合
poetry add --group dev uvbump
poetry run uvbump
```

## 使用法

```console
uvbump [<newversion> | major | minor | patch | bump] [-n|--dry-run] [-h|--help]
```

### バージョン更新タイプ

- `major`: メジャーバージョンを 1 つ上げる (1.2.3 → 2.0.0)
- `minor`: マイナーバージョンを 1 つ上げる (1.2.3 → 1.3.0)
- `patch`: パッチバージョンを 1 つ上げる (1.2.3 → 1.2.4)
- `bump`: デフォルト。通常版は patch と同じ、pre-release 版は番号を 1 つ上げる (1.2.3a1 → 1.2.3a2)
- `<newversion>`: 明示的なバージョン指定 (PEP 440 準拠に変換される)

### オプション

- `-n, --dry-run`: 実際の変更は行わず、何が実行されるかを表示。事前のコミット不要
- `-h, --help`: ヘルプメッセージを表示

## 使用例

### 基本的な使用例

```sh
# パッチバージョンを上げる (1.0.0 → 1.0.1)
uvbump patch

# マイナーバージョンを上げる (1.0.1 → 1.1.0)
uvbump minor

# メジャーバージョンを上げる (1.1.0 → 2.0.0)
uvbump major

# デフォルト動作 (bumpと同じ)
uvbump
```

### 明示的なバージョン指定

```sh
# 特定のバージョンに設定
uvbump 1.5.0

# pre-releaseバージョンに設定
uvbump 2.0.0a1

# リリース候補版
uvbump 1.0.0rc1
```

### pre-releaseバージョンの管理

```sh
# pre-release番号を上げる (1.0.0a1 → 1.0.0a2)
uvbump bump

# pre-releaseから正式版へ (明示的に指定)
uvbump 1.0.0
```

### dry-runモード

```sh
# 変更内容を確認 (実際の変更は行わない)
uvbump patch -n
uvbump minor --dry-run
```

### 出力例

```console
$ uvbump patch
Updated: /path/to/project/pyproject.toml
Version: 1.0.0 → 1.0.1
Commit: 1.0.1
Tag: v1.0.1

$ uvbump 2.0.0a1
Updated: /path/to/project/pyproject.toml
Version: 1.0.1 → 2.0.0a1
Commit: 2.0.0a1
Tag: test-2.0.0a1
```

## 仕様

### 基本動作

- デフォルトは `uvbump bump` に同じ
- PEP 440 準拠のバージョン管理
- 同じバージョンやダウングレードは不許可
  - ダウングレード例: `1.0.0` > `1.0.0a1`
- pre-release と通常版の切り替えは明示的なバージョン指定が必要
  - 例: `1.0.0` → `1.1.0a1` は `uvbump 1.1.0a1` で指定
  - 例: `1.0.0a1` → `1.0.0` は `uvbump 1.0.0` で指定

### Git統合

- **重要**: 事前にすべての変更がコミットされている必要がある
- カレントディレクトリの pyproject.toml を更新後、自動でコミット・タグ作成
  - コミットメッセージ: 新しいバージョン番号
  - タグ: 通常版は `v{version}`、pre-release 版は `test-{version}`
- `git push` は行わない。`git push` と `git push --tags` は手動で実行すること

### エラー条件

- カレントディレクトリに pyproject.toml が存在しない
- project.version が存在しない、または PEP 440 非準拠
- git リポジトリでない
- 未コミットの変更がある（dry-run モードでは警告のみ）

### 制限事項

- 設定ファイルは未対応
- monorepo 対応は未実装

## 似たツール

- [npm-version](https://docs.npmjs.com/cli/v11/commands/npm-version)
- [pybump](https://pypi.org/project/pybump/)
- [bump2version](https://pypi.org/project/bump2version/)
- [bump-my-version](https://pypi.org/project/bump-my-version/)
- [bumpver](https://pypi.org/project/bumpver/)
