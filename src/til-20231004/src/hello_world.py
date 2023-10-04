"""公式のサンプル実装.

Notes
-----
```sh
rm -rf '/tmp/bar'
LUIGI_CONFIG_PARSER=toml LUIGI_CONFIG_PATH=src/config.toml python src/hello_world.py
```
"""
import luigi


class HelloWorldTask(luigi.Task):
    """タスク."""

    task_namespace = "examples"

    def run(self):
        """実行."""
        print("{task} says: Hello world!".format(task=self.__class__.__name__))


if __name__ == "__main__":
    luigi.run(["examples.HelloWorldTask", "--workers", "1", "--local-scheduler"])
