"""concurrent.futuresを利用した並列処理を行い時間計測を行うためのスクリプト.

Notes
-----
```sh
rm -rf '/tmp/bar'
LUIGI_CONFIG_PARSER=toml \
    LUIGI_CONFIG_PATH=src/config.toml \
    python src/foo_multi_process.py
```
"""
import concurrent.futures as confu
import logging
import time
from pathlib import Path

import luigi

logger = logging.getLogger("luigi-interface")


class Foo(luigi.WrapperTask):
    """並列タスクをよぶタスク."""

    task_namespace = "examples"

    def run(self):
        """実行."""
        print("Running Foo")

    def requires(self):
        """依存関係."""
        with confu.ProcessPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(bar, x) for x in range(1000)]
            for future in confu.as_completed(futures):
                logger.info(f"completed index={future.result()}")


def bar(index: int) -> int:
    """並列化されるタスク.foo.pyのBarクラスと同様の処理を実施."""
    output_filepath = Path("/tmp/bar") / f"{index}"
    if output_filepath.exists():
        return index

    time.sleep(0.001)
    time.sleep(0.001)

    output_filepath.parent.mkdir(exist_ok=True, parents=True)
    output_filepath.touch()

    return index


if __name__ == "__main__":
    luigi.run(["examples.Foo", "--workers", "2", "--local-scheduler"])
