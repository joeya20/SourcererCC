'''
TODO: extract continuous assign statements?
TODO: extract one-line always?
'''

import pyslang


def getBlocks(filestring):
    """
    parse filestring to extract block data for sourcererCC
    """
    tree = pyslang.SyntaxTree.fromText(filestring)
    # make sure we got a syntax node back (didn't error out)
    assert isinstance(tree.root, pyslang.SyntaxNode)

    # visit and store every block statement
    def handle(obj):
        if isinstance(obj, pyslang.BlockStatementSyntax):
            blocks.append(obj)
            block_strings.append(str(obj))

    blocks = []
    block_strings = []
    sm = tree.sourceManager
    tree.root.visit(handle)

    # get needed block metadata
    blocks_linenos = [
        (sm.getLineNumber(block.begin.location), sm.getLineNumber(block.end.location))
        for block in blocks
    ]
    block_names = [
        str(block.blockName.name).strip() if block.blockName is not None else ''
        for block in blocks
    ]

    return (blocks_linenos, block_strings, block_names)


def main():
    """
    main is not run when using SourcererCC
    """
    with open('opentitan/hw/ip/aes/rtl/aes_control_fsm.sv', 'r') as in_file:
        lines = in_file.readlines()
        filestring = ''.join(lines)

        (blocks_linenos, block_strings, block_names) = getBlocks(filestring)
        print("\n".join(blocks_linenos))


# test
if __name__ == '__main__':
    main()
