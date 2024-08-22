from xdsl.pattern_rewriter import (
    PatternRewriter,
    RewritePattern,
    op_type_rewrite_pattern,
)
from xdsl.utils.hints import isa

from xuiua.dialect import TF64, AddOp


class AddOpShapeInferencePattern(RewritePattern):
    @op_type_rewrite_pattern
    def match_and_rewrite(self, op: AddOp, rewriter: PatternRewriter, /):
        assert isa((lhs_type := op.lhs.type), TF64)
        assert isa((rhs_type := op.rhs.type), TF64)

        assert lhs_type.get_shape() == rhs_type.get_shape()

        if lhs_type != op.res.type:
            rewriter.modify_value_type(op.res, lhs_type)
