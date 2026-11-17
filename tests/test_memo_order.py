import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import app


class MemoOrderTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        db_patch = patch.object(app, 'DB', str(Path(self.directory.name) / 'memo.db'))
        db_patch.start()
        self.addCleanup(db_patch.stop)
        app.init_db()

    def insert(self, content, created_at):
        with app.get_db() as conn:
            conn.execute('INSERT INTO memos (content, created_at) VALUES (?, ?)',
                         (content, created_at))

    def test_same_second_places_latest_insert_first(self):
        for content in ['first', 'second', 'third']:
            self.insert(content, '2026-11-17 10:00:00')
        self.assertEqual([m['content'] for m in app.get_all_memos()],
                         ['third', 'second', 'first'])

    def test_timestamp_still_takes_priority_over_id(self):
        self.insert('newer timestamp', '2026-11-17 10:00:01')
        self.insert('older timestamp', '2026-11-17 10:00:00')
        self.assertEqual([m['content'] for m in app.get_all_memos()],
                         ['newer timestamp', 'older timestamp'])

    def test_empty_database(self):
        self.assertEqual(app.get_all_memos(), [])


if __name__ == '__main__':
    unittest.main()
