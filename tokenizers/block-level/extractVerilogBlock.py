import pyslang


def getBlocks(filestring):
    """
    parse filestring to extract block data for sourcererCC
    """

    tree = pyslang.SyntaxTree.fromText(filestring)
    assert isinstance(tree.root, pyslang.SyntaxNode)

    def handle(obj):
        if isinstance(obj, pyslang.BlockStatementSyntax):
            blocks.append(obj)
            block_strings.append(str(obj))

    blocks = []
    block_strings = []
    sm = tree.sourceManager
    tree.root.visit(handle)

    blocks_linenos = [
        (sm.getLineNumber(block.begin.location), sm.getLineNumber(block.end.location))
        for block in blocks
    ]
    block_names = [
        str(block.blockName.name).strip() if block.blockName is not None else ''
        for block in blocks
    ]
    print(blocks_linenos)
    print(block_strings)
    print(block_names)
    return (blocks_linenos, block_strings, block_names)


if __name__ == '__main__':
    with open('test.sv', 'r') as in_file:
        lines = in_file.readlines()
        line_count = len(lines)
        filestring = ''.join(lines)

        block_data = getBlocks(filestring)
