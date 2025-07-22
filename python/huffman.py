from __future__ import annotations
from dataclasses import dataclass
from typing import Generator, List
import io
import pathlib

# Huffman Encoding/Decoding Algorithm
#
# Usage:
#  - Encode: `python huffman.py encode --input example.txt --output example.zhf`
#  - Decode: `python huffman.py decode --input example.zhf --output example.txt`
#
# File format:
#  - Binary file format
#  - Only ASCII is supported
#  - Uses extension .zhf
#  - The length of the arrays is described before the array
#  - The frequency table uses a (character, occurance_count) tuple
# 
# Layout:
#  - File format constant (int32)
#  - File format version (int8)
#  - Frequency table length (int32)
#  - Frequency table (tuple(int8, int32)[])
#  - Encoded message length (int32)
#  - Encoded message used bits (int8)
#  - Encoded message data (int8[])

FILE_FORMAT_CONSTANT = 0x5A4846
FILE_FORMAT_VERSION = 1

unique_node_identifier = -1
@dataclass
class Node:
    id: int
    parent: Node | None
    character: str | None
    weight: int
    children: List[Node]
    def __repr__(self): 
        return f"'{self.character}' (weight={self.weight}, has_parent={self.parent!=None})"
    def __str__(self):
        return ""
    @staticmethod
    def new_leaf(character: str | None, weight: int):
        global unique_node_identifier
        unique_node_identifier += 1
        return Node(unique_node_identifier, None, character, weight, [])
    @staticmethod
    def new_node(weight: int, left: Node, right: Node):
        global unique_node_identifier
        unique_node_identifier += 1
        return Node(unique_node_identifier, None, None, weight, [left, right])
    def __eq__(self, other):
        return not other or self.id == other.id

write_bit_buffer = 0
write_bit_position = 0
def write_bit(stream: io.BytesIO, value: int):
    global write_bit_buffer, write_bit_position
    assert value == 0 or value == 1
    mask = value << (8 - write_bit_position - 1)
    write_bit_buffer |= mask
    write_bit_position += 1
    if write_bit_position >= 8:
        write_int8(stream, write_bit_buffer)
        write_bit_buffer = 0
        write_bit_position = 0

def flush_bit_buffer(stream: io.BytesIO):
    global write_bit_buffer, write_bit_position
    if write_bit_position != 0:
        write_int8(stream, write_bit_buffer)

def write_int8(stream: io.BytesIO, value: int):
    stream.write(value.to_bytes(1, "big"))

def write_int32(stream: io.BytesIO, value: int):
    stream.write(value.to_bytes(4, "big"))

def read_int8(stream: io.BytesIO):
    return int.from_bytes(stream.read(1), "big")

def read_int32(stream: io.BytesIO):
    return int.from_bytes(stream.read(4), "big")

def frequency_table(text: str) -> list[tuple[str, int]]:
    characters = list(text)
    frequency_table = {}
    for character in characters:
        if character not in frequency_table:
            frequency_table[character] = 0
        frequency_table[character] += 1
    by_occurance = lambda tuple: tuple[1]
    return sorted(frequency_table.items(), key=by_occurance, reverse=True)

def pop_min_node(nodes: List[Node]) -> Node:
    min_index = 0
    min_weight = 1e99
    for i, node in enumerate(nodes):
        if node.weight < min_weight:
            min_index = i
            min_weight = node.weight
    return nodes.pop(min_index)

def print_nodes(node: Node, depth: int = 0) -> None:
    prefix = "".ljust(depth * 2, " ")
    char = str(node.character)
    if char == '\n': 
        char = '<new line>'
    print(f"{prefix}{char} ({node.weight})")
    for child_node in node.children:
        print_nodes(child_node, depth + 1)

class HuffmanTree:
    def __init__(self, root: Node, encoding_table: dict[str, Node]):
        self.root = root
        self.encoding_table = encoding_table
    @staticmethod
    def new(frequency_list: List[tuple[str, int]]):
        nodes = []
        encoding_table: dict[str, Node] = {}
        for character, occurance in frequency_list:
            node = Node.new_leaf(character, occurance)
            nodes.append(node)
            encoding_table[character] = node
        while len(nodes) >= 2:
            last_node = pop_min_node(nodes)
            second_last_node = pop_min_node(nodes)
            merged_weight = last_node.weight + second_last_node.weight
            merged_node = Node.new_node(merged_weight, left=second_last_node, right=last_node)
            last_node.parent = merged_node
            second_last_node.parent = merged_node
            nodes.append(merged_node)
        return HuffmanTree(nodes[0], encoding_table)

class HuffmanEncoder:
    def __init__(self, tree: HuffmanTree, stream: io.BytesIO):
        self.tree = tree
        self.stream = stream
        self.write_header()
    def write_header(self):
        write_int32(self.stream, FILE_FORMAT_CONSTANT)
        write_int8(self.stream, FILE_FORMAT_VERSION)
        encoding_table_size = len(self.tree.encoding_table)
        write_int32(self.stream, encoding_table_size)
        for character, node in self.tree.encoding_table.items():
            write_int8(self.stream, ord(character))
            write_int32(self.stream, node.weight)
        self.encoded_message_size_position = self.stream.tell()
        write_int32(self.stream, 0)
        self.encoded_message_used_bits_position = self.stream.tell()
        write_int8(self.stream, 0)
    def write(self, character) -> None:
        current: Node = self.tree.encoding_table[character]
        path: List[int] = []
        while current.parent:
            previous = current
            current = current.parent
            bit = current.children.index(previous)
            path.append(bit)
        while path:
            write_bit(self.stream, path.pop())
    def close(self):
        flush_bit_buffer(self.stream)
        total_bytes_written = self.stream.tell() - self.encoded_message_used_bits_position - 1
        self.stream.seek(self.encoded_message_size_position)
        write_int32(self.stream, total_bytes_written)
        self.stream.seek(self.encoded_message_used_bits_position)
        global write_bit_position
        write_int8(self.stream, write_bit_position)
        self.stream.seek(0)

class BitReader:
    def __init__(self, byte, max_length = 8):
        self.byte = byte
        self.position = 0
        self.max_length = max_length
    def read(self) -> Generator[int]:
        while self.position < self.max_length:
            shift = (8 - self.position - 1)
            mask = 1 << shift
            value = (self.byte & mask) >> shift
            yield value
            self.position += 1

class HuffmanDecoder:
    def __init__(self, tree: HuffmanTree, stream: io.BytesIO):
        self.tree = tree
        self.stream = stream
        self.encoded_message_size = read_int32(stream)
        self.encoded_message_used_bits = read_int8(stream)
        self.current_node = tree.root
    def read(self) -> Generator[str]:
        for i in range(self.encoded_message_size):
            length = 8 if i != self.encoded_message_size - 1 else self.encoded_message_used_bits
            byte = read_int8(self.stream)
            reader = BitReader(byte, length)
            for bit in reader.read():
                self.current_node = self.current_node.children[bit]
                if self.current_node.character:
                    yield self.current_node.character
                    self.current_node = self.tree.root

def encode(input_file_path, output_file_path):
    text = pathlib.Path(input_file_path).read_text()
    assert text.isascii()
    frequencies = frequency_table(text)
    tree = HuffmanTree.new(frequencies)
    stream = io.BytesIO()
    encoder = HuffmanEncoder(tree, stream)
    for character in text:
        encoder.write(character)
    encoder.close()
    pathlib.Path(output_file_path).write_bytes(stream.getbuffer().tobytes())

def assert_zhf_file_format(stream):
    file_format_constant = read_int32(stream)
    assert file_format_constant == FILE_FORMAT_CONSTANT

def decode(input_file_path, output_file_path):
    stream = io.BytesIO(pathlib.Path(input_file_path).read_bytes())
    assert_zhf_file_format(stream)
    file_format_version = read_int8(stream)
    assert file_format_version == 1
    frequency_table_length = read_int32(stream)
    frequencies = []
    for _ in range(frequency_table_length):
        character = chr(read_int8(stream))
        occurances = read_int32(stream)
        frequencies.append((character, occurances))
    tree = HuffmanTree.new(frequencies)
    decoder = HuffmanDecoder(tree, stream)
    text = io.StringIO()
    for character in decoder.read():
        print(character, end="")
        text.write(character)
    text.seek(0)
    pathlib.Path(output_file_path).write_text(text.read())

# # Test case: Hello world (super small)
# encode("hello_world.txt", "hello_world.zhf")
# decode("hello_world.zhf", "hello_world_decoded.txt")

# Text case: Lorem ipsum (big)
encode("lorem.txt", "lorem.zhf")
decode("lorem.zhf", "lorem_decoded.txt")
