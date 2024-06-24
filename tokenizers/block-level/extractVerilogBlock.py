import pyslang


def getBlocks(filestring, target):
    """
    parse filestring to extract block data for sourcererCC
    """
    tree = pyslang.SyntaxTree.fromText(filestring)
    # make sure we got a syntax node back (didn't error out)
    assert isinstance(tree.root, pyslang.SyntaxNode)

    # visit and store every block statement
    def handle_blocks(obj):
        if isinstance(obj, pyslang.BlockStatementSyntax):
            blocks.append(obj)
            block_strings.append(str(obj))

    def handle_cont_assigns(obj):
        if isinstance(obj, pyslang.ContinuousAssignSyntax):
            blocks.append(obj)
            block_strings.append(str(obj))

    def handle_hier_insts(obj):
        if isinstance(obj, pyslang.HierarchyInstantiationSyntax):
            blocks.append(obj)
            block_strings.append(str(obj))

    def handle_assign_expr(obj):
        if isinstance(obj, pyslang.BinaryExpressionSyntax) \
                and obj.operatorToken.kind == pyslang.TokenKind.Equals:
            blocks.append(obj)
            block_strings.append(str(obj))

    def handle_if_stmt(obj):
        if isinstance(obj, pyslang.ConditionalStatementSyntax):
            blocks.append(obj)
            block_strings.append(str(obj))

    blocks = []
    block_strings = []
    block_names = []

    sm = tree.sourceManager
    if target == 'IfStmt':
        tree.root.visit(handle_if_stmt)
    elif target == 'SeqBlock':
        tree.root.visit(handle_blocks)
        block_names = [
            str(block.blockName.name).strip() if block.blockName is not None else ''
            for block in blocks
        ]
    elif target == 'AssignExpr':
        tree.root.visit(handle_assign_expr)
    elif target == 'ContAssign':
        tree.root.visit(handle_cont_assigns)
    elif target == 'HierInst':
        tree.root.visit(handle_hier_insts)
    else:
        raise ValueError('Invalid target')

    blocks_linenos = [
        (sm.getLineNumber(block.sourceRange.start), sm.getLineNumber(block.sourceRange.end))
        for block in blocks
    ]
    if len(block_names) == 0:
        block_names = [''] * len(blocks)

    return (blocks_linenos, block_strings, block_names)


def main():
    """
    main is not run when using SourcererCC
    """
    with open('tests/test/file1.v', 'r') as in_file:
        lines = in_file.readlines()
        filestring = ''.join(lines)
        (blocks_linenos, block_strings, block_names) = getBlocks(filestring)


# test
if __name__ == '__main__':
    main()
