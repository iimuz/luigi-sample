---
title: luigiを利用したタスク実行サンプル
date: 2023-10-04
lastmod: 2023-10-04
---

## 概要

[luigi](https://github.com/spotify/luigi)を利用してタスク実行を行う環境を構築した時のサンプルです。

## ファイル構成

- フォルダ
  - `.vscode`: VSCode の基本設定を記述します。
  - `src`: 開発するスクリプトを格納します。
- ファイル
  - `.gitignore`: [python 用の gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore) です。
  - `.sample.env`: 環境変数のサンプルを記載します。利用時は `.env` に変更して利用します。
  - `LICENSE`: ライセンスを記載します。 MIT ライセンスを設定しています。
  - `pyproject.toml`/`setup.py`/`setup.cfg`: python バージョンなどを明記します。
  - `README.md`: 本ドキュメントです。

## 実行方法

## 仮想環境の構築

仮想環境の構築には python 標準で付属している venv の利用を想定しています。
スクリプトで必要なパッケージは `requirements.txt` に記載します。
実際にインストール後は、 `requirements-freeze.txt` としてバージョンを固定します。

```sh
# create virtual env
python -m venv .venv

# activate virtual env(linux)
source .venv/bin/activate
# or (windows)
source .venv/Scripts/activate.ps1

# install packages
pip install -e .[dev,test]

# freeze version
pip freeze > constraint.txt
pip install -e .[dev,test] -c constraint.txt
```

## code style

コードの整形などはは下記を利用しています。

- [black](https://github.com/psf/black): python code formmater.
- [flake8](https://github.com/PyCQA/flake8): style checker.
- [isort](https://github.com/PyCQA/isort): sort imports.
- [mypy](https://github.com/python/mypy): static typing.
- docstirng: [numpy 形式](https://numpydoc.readthedocs.io/en/latest/format.html)を想定しています。
  - vscode の場合は [autodocstring](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring) 拡張機能によりひな型を自動生成できます。

## Tips

### タスク数による実行時間

10 個のタスクを 2 並列で行った場合は、下記の通り。
1 タスクは 0.001sec の sleep になるように修正している。

```sh
$ LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/foo.py                                                                                                                                                                                            ~/src/github.com/iimuz/scratchpad-til/src/til-20231004
INFO     2023-10-04 16:50:49 setup_logging:82 logging configured via config section
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_9_afea9c1ed4   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_8_446a6fadda   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_7_7a5655a70d   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_6_d94e6707b0   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_5_381f71ed51   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_4_3798ec54a0   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_3_40c49393a7   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_2_51dd7c7388   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_1_aebd9cb151   has status   PENDING
INFO     2023-10-04 16:51:00 worker:630 Informed scheduler that task   examples.Bar_0_e0cbafafd8   has status   PENDING
INFO     2023-10-04 16:51:00 interface:172 Done scheduling tasks
INFO     2023-10-04 16:51:00 worker:1219 Running Worker with 2 processes
INFO     2023-10-04 16:51:01 worker:630 Informed scheduler that task   examples.Bar_5_381f71ed51   has status   DONE
INFO     2023-10-04 16:51:01 worker:630 Informed scheduler that task   examples.Bar_8_446a6fadda   has status   DONE
INFO     2023-10-04 16:51:02 worker:630 Informed scheduler that task   examples.Bar_9_afea9c1ed4   has status   DONE
INFO     2023-10-04 16:51:02 worker:630 Informed scheduler that task   examples.Bar_6_d94e6707b0   has status   DONE
INFO     2023-10-04 16:51:03 worker:630 Informed scheduler that task   examples.Bar_4_3798ec54a0   has status   DONE
INFO     2023-10-04 16:51:03 worker:630 Informed scheduler that task   examples.Bar_1_aebd9cb151   has status   DONE
INFO     2023-10-04 16:51:05 worker:630 Informed scheduler that task   examples.Bar_7_7a5655a70d   has status   DONE
INFO     2023-10-04 16:51:05 worker:630 Informed scheduler that task   examples.Bar_2_51dd7c7388   has status   DONE
INFO     2023-10-04 16:51:06 worker:630 Informed scheduler that task   examples.Bar_3_40c49393a7   has status   DONE
INFO     2023-10-04 16:51:06 worker:630 Informed scheduler that task   examples.Bar_0_e0cbafafd8   has status   DONE
Running Foo
INFO     2023-10-04 16:51:16 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   DONE
INFO     2023-10-04 16:51:16 worker:523 Worker Worker(salt=5922022424, workers=2, host=hoge.local, username=hoge, pid=92536) was stopped. Shutting down Keep-Alive thread
INFO     2023-10-04 16:51:16 interface:175
===== Luigi Execution Summary =====

Scheduled 11 tasks of which:
* 11 ran successfully:
    - 10 examples.Bar(num=0...9)
    - 1 examples.Foo()

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```

```sh
$ LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/foo.py                                                                                                                                                                                            ~/src/github.com/iimuz/scratchpad-til/src/til-20231004
INFO     2023-10-04 17:01:13 setup_logging:82 logging configured via config section
INFO     2023-10-04 17:02:55 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   PENDING
INFO     2023-10-04 17:02:55 worker:630 Informed scheduler that task   examples.Bar_99_5ea8bbd38d   has status   PENDING
# 省略
INFO     2023-10-04 17:02:55 worker:630 Informed scheduler that task   examples.Bar_0_e0cbafafd8   has status   PENDING
INFO     2023-10-04 17:02:55 interface:172 Done scheduling tasks
INFO     2023-10-04 17:02:55 worker:1219 Running Worker with 2 processes
INFO     2023-10-04 17:02:56 worker:630 Informed scheduler that task   examples.Bar_10_672153c373   has status   DONE
INFO     2023-10-04 17:02:56 worker:630 Informed scheduler that task   examples.Bar_41_3647875df1   has status   DONE
INFO     2023-10-04 17:02:57 worker:630 Informed scheduler that task   examples.Bar_34_e55cdb34d8   has status   DONE
INFO     2023-10-04 17:02:57 worker:630 Informed scheduler that task   examples.Bar_82_301473214d   has status   DONE
INFO     2023-10-04 17:02:58 worker:630 Informed scheduler that task   examples.Bar_12_44b49d4a02   has status   DONE
INFO     2023-10-04 17:02:58 worker:630 Informed scheduler that task   examples.Bar_3_40c49393a7   has status   DONE
INFO     2023-10-04 17:02:59 worker:630 Informed scheduler that task   examples.Bar_39_3db6e98623   has status   DONE
INFO     2023-10-04 17:02:59 worker:630 Informed scheduler that task   examples.Bar_8_446a6fadda   has status   DONE
# 省略
INFO     2023-10-04 17:03:45 worker:630 Informed scheduler that task   examples.Bar_90_47415d3462   has status   DONE
INFO     2023-10-04 17:03:45 worker:630 Informed scheduler that task   examples.Bar_37_36d95f0ce5   has status   DONE
INFO     2023-10-04 17:03:46 worker:630 Informed scheduler that task   examples.Bar_83_9de327ef56   has status   DONE
INFO     2023-10-04 17:03:46 worker:630 Informed scheduler that task   examples.Bar_76_0ee3dfe0df   has status   DONE
INFO     2023-10-04 17:03:47 worker:630 Informed scheduler that task   examples.Bar_93_f8dbb00546   has status   DONE
INFO     2023-10-04 17:03:47 worker:630 Informed scheduler that task   examples.Bar_22_624c63d93f   has status   DONE
INFO     2023-10-04 17:03:49 worker:630 Informed scheduler that task   examples.Bar_87_a7f37b3127   has status   DONE
INFO     2023-10-04 17:03:49 worker:630 Informed scheduler that task   examples.Bar_30_e7fef72c80   has status   DONE
INFO     2023-10-04 17:03:50 worker:630 Informed scheduler that task   examples.Bar_16_6d159a70a5   has status   DONE
INFO     2023-10-04 17:03:50 worker:630 Informed scheduler that task   examples.Bar_13_03eb002057   has status   DONE
INFO     2023-10-04 17:03:51 worker:630 Informed scheduler that task   examples.Bar_86_87db27985e   has status   DONE
INFO     2023-10-04 17:03:51 worker:630 Informed scheduler that task   examples.Bar_53_72dc9bb967   has status   DONE
Running Foo
INFO     2023-10-04 17:05:31 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   DONE
INFO     2023-10-04 17:05:31 worker:523 Worker Worker(salt=1717662583, workers=2, host=hoge.local, username=hoge, pid=93581) was stopped. Shutting down Keep-Alive thread
INFO     2023-10-04 17:05:31 interface:175
===== Luigi Execution Summary =====

Scheduled 101 tasks of which:
* 101 ran successfully:
    - 100 examples.Bar(num=0...99)
    - 1 examples.Foo()

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```
