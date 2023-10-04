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
pip freeze > requirements.txt
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

細かいタスクを大量に並列化する場合は、luigi のタスクで並列化するよりも、concurrent.future を利用した方がオーバーヘッドが小さい。

#### luigi を利用した 10 並列

10 個のタスクを 2 並列で行った場合は、下記の通り。
1 タスクは run, output の両方で 0.001sec の sleep になるように修正している。

```sh
$ LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/foo.py                                                                                                                                                                                            ~/src/github.com/iimuz/scratchpad-til/src/til-20231004
NFO     2023-10-04 17:17:48 setup_logging:82 logging configured via config section
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_9_afea9c1ed4   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_8_446a6fadda   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_7_7a5655a70d   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_6_d94e6707b0   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_5_381f71ed51   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_4_3798ec54a0   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_3_40c49393a7   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_2_51dd7c7388   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_1_aebd9cb151   has status   PENDING
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_0_e0cbafafd8   has status   PENDING
INFO     2023-10-04 17:17:48 interface:172 Done scheduling tasks
INFO     2023-10-04 17:17:48 worker:1219 Running Worker with 2 processes
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_8_446a6fadda   has status   DONE
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_3_40c49393a7   has status   DONE
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_7_7a5655a70d   has status   DONE
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_4_3798ec54a0   has status   DONE
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_1_aebd9cb151   has status   DONE
INFO     2023-10-04 17:17:48 worker:630 Informed scheduler that task   examples.Bar_2_51dd7c7388   has status   DONE
INFO     2023-10-04 17:17:49 worker:630 Informed scheduler that task   examples.Bar_0_e0cbafafd8   has status   DONE
INFO     2023-10-04 17:17:49 worker:630 Informed scheduler that task   examples.Bar_6_d94e6707b0   has status   DONE
INFO     2023-10-04 17:17:49 worker:630 Informed scheduler that task   examples.Bar_5_381f71ed51   has status   DONE
INFO     2023-10-04 17:17:49 worker:630 Informed scheduler that task   examples.Bar_9_afea9c1ed4   has status   DONE
Running Foo
INFO     2023-10-04 17:17:49 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   DONE
INFO     2023-10-04 17:17:49 worker:523 Worker Worker(salt=1767022787, workers=2, host=hoge.local, username=hoge, pid=98308) was stopped. Shutting down Keep-Alive thread
INFO     2023-10-04 17:17:49 interface:175
===== Luigi Execution Summary =====

Scheduled 11 tasks of which:
* 11 ran successfully:
    - 10 examples.Bar(num=0...9)
    - 1 examples.Foo()

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```

#### luigi を利用した 1000 並列

タスク数を 1000 にした場合。

```sh
$ LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/foo.py                                                                                                                                                                                            ~/src/github.com/iimuz/scratchpad-til/src/til-20231004
INFO     2023-10-04 21:27:01 setup_logging:82 logging configured via config section
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_999_0b31b23a83   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_998_5900be3096   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_997_ac27458e6b   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_996_170def391d   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_995_a9856c11b4   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_994_def96d454c   has status   PENDING
# 省略
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_15_bf4e8d660b   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_14_76f9794a70   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_13_03eb002057   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_12_44b49d4a02   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_11_924e13a081   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_10_672153c373   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_9_afea9c1ed4   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_8_446a6fadda   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_7_7a5655a70d   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_6_d94e6707b0   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_5_381f71ed51   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_4_3798ec54a0   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_3_40c49393a7   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_2_51dd7c7388   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_1_aebd9cb151   has status   PENDING
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_0_e0cbafafd8   has status   PENDING
INFO     2023-10-04 21:27:03 interface:172 Done scheduling tasks
INFO     2023-10-04 21:27:03 worker:1219 Running Worker with 2 processes
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_244_20e0fb2448   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_84_8ae9783b6b   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_160_790b7c4461   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_410_0622f8635f   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_77_9b13859221   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_637_542563ef8c   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_544_ef0a08af3c   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_830_ee978b5cad   has status   DONE
INFO     2023-10-04 21:27:03 worker:630 Informed scheduler that task   examples.Bar_988_7c957c9b4d   has status   DONE
INFO     2023-10-04 21:27:04 worker:630 Informed scheduler that task   examples.Bar_884_b109f5de21   has status   DONE
INFO     2023-10-04 21:27:04 worker:630 Informed scheduler that task   examples.Bar_785_582cdf5556   has status   DONE
INFO     2023-10-04 21:27:04 worker:630 Informed scheduler that task   examples.Bar_944_68f0eb7e91   has status   DONE
# 省略
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_505_c8d41a6679   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_689_8392508121   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_728_dcf1d2443c   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_452_d2a5dc9e53   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_401_c76ffbac7a   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_440_f3d2bd966b   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_731_d2d30a6e8d   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_968_6e7f3f811b   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_554_e1a5a8acc9   has status   DONE
INFO     2023-10-04 21:28:20 worker:630 Informed scheduler that task   examples.Bar_258_e19e67ba71   has status   DONE
Running Foo
INFO     2023-10-04 21:28:22 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   DONE
INFO     2023-10-04 21:28:22 worker:523 Worker Worker(salt=6966258070, workers=2, host=hoge.local, username=hoge, pid=2619) was stopped. Shutting down Keep-Alive thread
INFO     2023-10-04 21:28:22 interface:175
===== Luigi Execution Summary =====

Scheduled 1001 tasks of which:
* 1001 ran successfully:
    - 1000 examples.Bar(num=0...999)
    - 1 examples.Foo()

This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```

#### `concurrent.future`で thread で 1000 並列

`concurrent.futures`を利用して thread 並列した場合。

```sh
$ LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/foo_multi_threads.py
INFO     2023-10-04 22:05:03 setup_logging:82 logging configured via config section
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=0
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=1
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=2
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=3
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=4
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=5
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=6
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=7
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=8
INFO     2023-10-04 22:05:03 foo_multi_threads:30 completed index=9
# 省略
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=989
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=990
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=991
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=992
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=993
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=994
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=995
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=996
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=997
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=998
INFO     2023-10-04 22:05:04 foo_multi_threads:30 completed index=999
INFO     2023-10-04 22:05:04 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   DONE
INFO     2023-10-04 22:05:04 interface:172 Done scheduling tasks
INFO     2023-10-04 22:05:04 worker:1219 Running Worker with 2 processes
INFO     2023-10-04 22:05:04 worker:523 Worker Worker(salt=7930369952, workers=2, host=hoge.local, username=hoge, pid=10790) was stopped. Shutting down Keep-Alive thread
INFO     2023-10-04 22:05:04 interface:175
===== Luigi Execution Summary =====

Scheduled 1 tasks of which:
* 1 complete ones were encountered:
    - 1 examples.Foo()

Did not run any tasks
This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```

#### `concurrent.future`で process で 1000 並列

`concurrent.futures`を利用して process 並列した場合。

```sh
$ LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/foo_multi_process.py
INFO     2023-10-04 18:06:19 setup_logging:82 logging configured via config section
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=0
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=1
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=2
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=3
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=4
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=5
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=6
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=7
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=8
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=9
INFO     2023-10-04 18:06:19 foo_multi_process:30 completed index=10
# 省略
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=991
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=992
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=993
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=994
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=995
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=996
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=997
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=998
INFO     2023-10-04 18:06:20 foo_multi_process:30 completed index=999
INFO     2023-10-04 18:06:20 worker:630 Informed scheduler that task   examples.Foo__99914b932b   has status   DONE
INFO     2023-10-04 18:06:20 interface:172 Done scheduling tasks
INFO     2023-10-04 18:06:20 worker:1219 Running Worker with 2 processes
INFO     2023-10-04 18:06:20 worker:523 Worker Worker(salt=2499021909, workers=2, host=hoge.local, username=hgoe, pid=11308) was stopped. Shutting down Keep-Alive thread
INFO     2023-10-04 18:06:20 interface:175
===== Luigi Execution Summary =====

Scheduled 1 tasks of which:
* 1 complete ones were encountered:
    - 1 examples.Foo()

Did not run any tasks
This progress looks :) because there were no failed tasks or missing dependencies

===== Luigi Execution Summary =====
```
