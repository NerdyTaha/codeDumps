from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum

# IR Node Types
@dataclass
class SASProgram:
    """Root node"""
    statements: List['Statement']
    
@dataclass
class DataStep:
    """Represents a DATA step"""
    output_dataset: str
    input_datasets: List[str]  # from SET/MERGE
    statements: List['DataStepStatement']
    where_clause: Optional['Expression'] = None
    
@dataclass  
class ProcStep:
    """Represents a PROC step"""
    proc_type: str  # 'MEANS', 'FREQ', 'SQL', etc.
    input_dataset: str
    options: Dict[str, Any]
    statements: List['ProcStatement']

@dataclass
class Assignment:
    """x = y + 1;"""
    variable: str
    expression: 'Expression'
    
@dataclass
class Expression:
    """Could be binary op, function call, literal, variable"""
    type: str  # 'binop', 'funcall', 'literal', 'variable'
    value: Any
    left: Optional['Expression'] = None
    right: Optional['Expression'] = None
    operator: Optional[str] = None

# Example for PROC MEANS
@dataclass
class ProcMeans:
    dataset: str
    variables: List[str]
    statistics: List[str]  # ['mean', 'std', 'min', 'max']
    class_vars: List[str]  # GROUP BY equivalent
    output_dataset: Optional[str] = None
