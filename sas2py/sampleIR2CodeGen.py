class PythonCodeGenerator:
    
    def __init__(self):
        self.output = []
        self.indent = 0
    
    def generate(self, ir: SASProgram) -> str:
        self.output = ["import pandas as pd", "import numpy as np", ""]
        
        for stmt in ir.statements:
            if isinstance(stmt, DataStep):
                self._generate_data_step(stmt)
            elif isinstance(stmt, ProcMeans):
                self._generate_proc_means(stmt)
        
        return "\n".join(self.output)
    
    def _generate_data_step(self, step: DataStep):
        # Generate pandas equivalent
        input_ds = step.input_datasets[0] if step.input_datasets else None
        output_var = step.output_dataset.replace('.', '_')
        
        if input_ds:
            input_var = input_ds.replace('.', '_')
            self.output.append(f"{output_var} = {input_var}.copy()")
        
        # Generate WHERE clause
        if step.where_clause:
            condition = self._generate_expression(step.where_clause)
            self.output.append(f"{output_var} = {output_var}[{condition}]")
        
        # Generate assignments
        for stmt in step.statements:
            if isinstance(stmt, Assignment):
                expr = self._generate_expression(stmt.expression)
                self.output.append(
                    f"{output_var}['{stmt.variable}'] = {expr}"
                )
        
        self.output.append("")
    
    def _generate_expression(self, expr: Expression) -> str:
        if expr.type == 'variable':
            return f"{expr.value}"
        elif expr.type == 'literal':
            if isinstance(expr.value, str):
                return f"'{expr.value}'"
            return str(expr.value)
        elif expr.type == 'binop':
            left = self._generate_expression(expr.left)
            right = self._generate_expression(expr.right)
            return f"({left} {expr.operator} {right})"
        # ... other cases
    
    def _generate_proc_means(self, proc: ProcMeans):
        dataset_var = proc.dataset.replace('.', '_')
        
        if proc.class_vars:
            group_by = "'" + "', '".join(proc.class_vars) + "'"
            agg_funcs = proc.statistics
            vars_str = "'" + "', '".join(proc.variables) + "'"
            
            self.output.append(
                f"summary = {dataset_var}.groupby([{group_by}])"
                f"[{vars_str}].agg({agg_funcs})"
            )
        else:
            # No grouping
            self.output.append(
                f"summary = {dataset_var}[{proc.variables}].describe()"
            )
        
        self.output.append("print(summary)")
        self.output.append("")

