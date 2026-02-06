from SASVisitor import SASVisitor
from ir_nodes import *  # Your IR classes

class SASToIRVisitor(SASVisitor):
    
    def visitProgram(self, ctx):
        statements = []
        for stmt in ctx.statement():
            statements.append(self.visit(stmt))
        return SASProgram(statements=statements)
    
    def visitDataStep(self, ctx):
        output_ds = ctx.dataset().getText()
        
        # Find SET statement
        input_datasets = []
        statements = []
        
        for stmt in ctx.dataStepBlock().statement():
            if stmt.setStatement():
                input_datasets.append(stmt.setStatement().dataset().getText())
            elif stmt.assignment():
                statements.append(self.visit(stmt.assignment()))
        
        return DataStep(
            output_dataset=output_ds,
            input_datasets=input_datasets,
            statements=statements
        )
    
    def visitAssignment(self, ctx):
        var = ctx.IDENTIFIER().getText()
        expr = self.visit(ctx.expression())
        return Assignment(variable=var, expression=expr)
    
    def visitExpression(self, ctx):
        # Handle binary operations, function calls, etc.
        if ctx.binaryOp():
            return Expression(
                type='binop',
                operator=ctx.binaryOp().getText(),
                left=self.visit(ctx.expression(0)),
                right=self.visit(ctx.expression(1))
            )
        elif ctx.IDENTIFIER():
            return Expression(
                type='variable',
                value=ctx.IDENTIFIER().getText()
            )
        # ... handle other cases
