from __future__ import annotations
from pandas import DataFrame

def main(dataFrame) -> list:
    """
    When working with extremely massive SQL data
    in Python, nothing stinks more than 
    iterating when pandas.DataFrame instance methods
    behave weirdly and steal your syntactic flexibility.
    
    Instead of using:
        pandas.DataFrame.{iterrows,itertuples}
    convert the container to JSON for a more intutive
    and readable program.
    """
    
    def convert(df: DataFrame) -> list:
        import json
        return json.loads(df.to_json(orient='records'))
    
    return convert(dataFrame)

            
            
