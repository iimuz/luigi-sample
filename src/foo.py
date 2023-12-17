"""公式のサンプル実装.

Notes
-----
```sh
rm -rf '/tmp/bar'
LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/foo.py
```
"""
import time

import luigi


class Foo(luigi.WrapperTask):
    """並列タスクをよぶタスク."""

    task_namespace = "examples"

    def run(self):
        """実行."""
        print("Running Foo")

    def requires(self):
        """依存関係."""
        for i in range(1000):
            yield Bar(i)


class Bar(luigi.Task):
    """並列化されるタスク."""

    task_namespace = "examples"
    num = luigi.IntParameter()

    def run(self):
        """実行."""
        time.sleep(0.001)
        self.output().open("w").close()

    def output(self):
        """出力."""
        time.sleep(0.001)
        return luigi.LocalTarget("/tmp/bar/%d" % self.num)


if __name__ == "__main__":
    luigi.run(["examples.Foo", "--workers", "2", "--local-scheduler"])
