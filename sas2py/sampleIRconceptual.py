SASProgram(
    statements=[
        DataStep(
            output_dataset='work.customer_summary',
            input_datasets=['raw.customers'],
            where_clause=BinaryOp('>', Variable('balance'), Literal(1000)),
            statements=[
                Assignment('risk_score', 
                    BinaryOp('/', Variable('balance'), Literal(1000))),
                IfElse(
                    condition=BinaryOp('>', Variable('risk_score'), Literal(5)),
                    then_stmt=Assignment('risk_level', Literal('HIGH')),
                    else_stmt=Assignment('risk_level', Literal('LOW'))
                )
            ]
        ),
        ProcMeans(
            dataset='work.customer_summary',
            variables=['risk_score'],
            statistics=['mean', 'std'],
            class_vars=['risk_level']
        )
    ]
)
