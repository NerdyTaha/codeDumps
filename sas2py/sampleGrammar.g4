// Typical structure in .g4 file
grammar SAS;

// Parser rules (lowercase)
program: statement+ EOF;
dataStep: DATA dataset SEMICOLON dataStepBlock RUN SEMICOLON;
dataset: IDENTIFIER (DOT IDENTIFIER)?;

// Lexer rules (uppercase)  
DATA: 'data' | 'DATA';
RUN: 'run' | 'RUN';
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
