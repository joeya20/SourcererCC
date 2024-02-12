import pyslang

def getBlocks(filestring):
    """
    parse filestring to extract block data for sourcererCC
    """
    tree = pyslang.SyntaxTree.fromText(filestring)
    # make sure we got a syntax node back (didn't error out)
    assert isinstance(tree.root, pyslang.SyntaxNode)

    # visit and store every block statement
    # def handle_blocks(obj):
    #     if isinstance(obj, pyslang.BlockStatementSyntax):
    #         blocks.append(obj)
    #         block_strings.append(str(obj))

    # def handle_cont_assigns(obj):
    #     if isinstance(obj, pyslang.ContinuousAssignSyntax):
    #         cont_assigns.append(obj)
    #         cont_assign_strings.append(str(obj))

    # def handle_hier_insts(obj):
    #     if isinstance(obj, pyslang.HierarchyInstantiationSyntax):
    #         insts.append(obj)
    #         inst_strings.append(str(obj))

    # def handle_assign_expr(obj):
    #     if isinstance(obj, pyslang.BinaryExpressionSyntax) \
    #             and obj.operatorToken.kind == pyslang.TokenKind.Equals:
    #         assign_exprs.append(obj)
    #         assign_expr_strings.append(str(obj))

    def handle_if_stmt(obj):
        if isinstance(obj, pyslang.ConditionalStatementSyntax):
            if_stmts.append(obj)
            if_stmts_strings.append(str(obj))

    blocks = []
    block_strings = []

    cont_assigns = []
    cont_assign_strings = []

    insts = []
    inst_strings = []

    assign_exprs = []
    assign_expr_strings = []

    if_stmts = []
    if_stmts_strings = []

    sm = tree.sourceManager
    tree.root.visit(handle_if_stmt)

    # blocks_linenos = [
    #     (sm.getLineNumber(block.sourceRange.start), sm.getLineNumber(block.sourceRange.end))
    #     for block in if_stmts
    # ]

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
    with open('tests/test/file1.v', 'r') as in_file:
        lines = in_file.readlines()
        filestring = ''.join(lines)
        (blocks_linenos, block_strings, block_names) = getBlocks(filestring)


# test
if __name__ == '__main__':
    main()
