"""Publishing must preserve an existing release across failures."""
import importlib.util
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('build_pc', Path('tools/build_pc.py'))
build_pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_pc)


class PublishTest(unittest.TestCase):
    def test_failure_boundaries_and_same_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, destination = root / 'source', root / 'release'
            source.write_bytes(b'new release')
            destination.write_bytes(b'existing release')
            destination.chmod(0o751)
            unrelated = root / '.txra-build-unrelated'
            unrelated.write_bytes(b'keep')
            for module, operation, error, stripper in (
                (build_pc.shutil, 'copy2', OSError('copy failed'), None),
                (build_pc.subprocess, 'run', subprocess.CalledProcessError(1, 'strip'), 'strip'),
                (build_pc.os, 'replace', OSError('publish failed'), None),
            ):
                def fail(*args, **kwargs):
                    if operation == 'copy2':
                        Path(args[1]).write_bytes(b'partial copy')
                    elif operation == 'run':
                        Path(args[0][-1]).write_bytes(b'partial strip')
                    raise error

                with self.subTest(operation=operation):
                    with patch.object(module, operation, side_effect=fail):
                        with self.assertRaises(type(error)):
                            build_pc.publish(source, destination, stripper)
                    self.assertEqual(destination.read_bytes(), b'existing release')
                    self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o751)
                    self.assertEqual(set(root.iterdir()), {source, destination, unrelated})
            build_pc.publish(destination, destination)
            self.assertEqual(destination.read_bytes(), b'existing release')
            self.assertEqual(stat.S_IMODE(destination.stat().st_mode), 0o751)
            self.assertEqual(unrelated.read_bytes(), b'keep')
            self.assertEqual(set(root.iterdir()), {source, destination, unrelated})


if __name__ == '__main__':
    unittest.main()
