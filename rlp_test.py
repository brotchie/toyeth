import rlp
import unittest


class TestEncode(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(rlp.encode(b"dog"), b'\x83dog')
        self.assertEqual(rlp.encode([b"cat", b"dog"]), b'\xc8\x83cat\x83dog')
        self.assertEqual(rlp.encode(b""), b'\x80')
        self.assertEqual(rlp.encode([]), b'\xc0')
        self.assertEqual(rlp.encode(b"\x00"), b'\x00')
        self.assertEqual(rlp.encode(b"\x04\x00"), b'\x82\x04\x00')
        self.assertEqual(
                rlp.encode([ [], [[]], [ [], [[]] ] ]),
                b'\xc7\xc0\xc1\xc0\xc3\xc0\xc1\xc0')
        self.assertEqual(
                rlp.encode(b"Lorem ipsum dolor sit amet, consectetur adipisicing elit"),
                b'\xb88Lorem ipsum dolor sit amet, consectetur adipisicing elit')


class TestDecode(unittest.TestCase):
    def test_decode(self):
        self.assertEqual(b"dog", rlp.decode(b'\x83dog'))
        self.assertEqual([b"cat", b"dog"], rlp.decode(b'\xc8\x83cat\x83dog'))
        self.assertEqual(b"", rlp.decode(b'\x80'))
        self.assertEqual([], rlp.decode(b'\xc0'))
        self.assertEqual(b"\x00", rlp.decode(b'\x00'))
        self.assertEqual(b"\x04\x00", rlp.decode(b'\x82\x04\x00'))
        self.assertEqual(
                [ [], [[]], [ [], [[]] ] ],
                rlp.decode(b'\xc7\xc0\xc1\xc0\xc3\xc0\xc1\xc0'))
        self.assertEqual(
                b"Lorem ipsum dolor sit amet, consectetur adipisicing elit",
                rlp.decode(b'\xb88Lorem ipsum dolor sit amet, consectetur adipisicing elit'))


if __name__ == "__main__":
    unittest.main()
