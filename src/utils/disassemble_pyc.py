import sys
import marshal
import dis


def disassemble_pyc(filepath):
    try:
        with open(filepath, "rb") as f:
            # Skip magic number and timestamp/size (different for Python 3.x)
            # Python 3.13 .pyc format: magic (4 bytes), flags (4 bytes), hash (8 bytes), code object
            magic = f.read(4)
            flags = f.read(4)
            hash_value = f.read(8)  # for Python 3.7+

            code_object = marshal.load(f)
            print(f"Disassembly of {filepath}:")
            dis.dis(code_object)
    except Exception as e:
        print(f"Error disassembling {filepath}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python disassemble_pyc.py <path_to_pyc_file>")
        sys.exit(1)

    pyc_file = sys.argv[1]
    disassemble_pyc(pyc_file)
