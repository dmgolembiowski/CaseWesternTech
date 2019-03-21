#!/usr/bin/env python3
import numpy as np
import pandas as pd

def refineDict(_dict, *retainedKeys):
    try:
        rKeys = [k for k in retainedKeys]
        for key in list(_dict):
            if key not in rKeys:
                del _dict[key]
        if not len(_dict) == 0:
            return _dict
        else:
            raise KeyError('String arguments were not passed to `itercolumns` argument: *colName')
    except KeyError:
        print('Type `help(itercolumns)` for suggested usage')
        

def itercolumns(dataframe, *colName, _aslist=False, _asdict=True):
    """ 
    `itercolumns(pandas.DataFrame)` is a meaningful way to
    evaluate frames of pandas.DataFrame.itertuples() objects if
    the pandas.DataFrame gains or loses columns such that
    when iterating over pandas.DataFrame.itertuples()
    the pandas.core.frame in the iteration loses a previously
    accurate tuple position in the frame.

    In English:
        This method makes it possible to prepare data analysis 
        scripts that are resilient to fluctuating SQL databases 
        that keep the same column names, however their column
        slice can change as a result of adding or dropping a table.

    Example Usage:
        >>> # if `myDataframe` resembles:
        >>> myDataframe
            a   b   c   d   e
        0   2   8   8   3   4
        1   4   2   9   0   9
        2   1   0   7   8   0
        3   5   1   7   1   3
        4   6   0   2   4   2
        >>> # then a call like this to return the column number of 'e' for use in `myDataframe.itertuples()`
        >>> e = furtherProcessing.itercolumns(myDataframe, 'e')
        5
        >>> # Now, there is a simple way to run 
        >>> for frame in myDataframe.itertuples():
        >>>     if frame[e] == 3:
        >>>         print(frame)
        Pandas(Index=3, a=5, b=1, c=7, d=1, e=3)
    
    Advanced Usage:
        >>> # Suppose we wanted to extend this functionality to track map multiple
        >>> # column names for utility with the pandas.DataFrame.itertuples() core
        >>> # frame because your SQL table might add or drop columns, and shift 
        >>> # to the left or right -- causing their array slice to be incremented 
        >>> # or decremented. 
        >>> #
        >>> # Then, `itercolumns` will return an object that keeps track of the 
        >>> # column-named integer slices for you.
        >>> 
        >>> myDataframe
            a   b   c   d   e
        0   2   8   8   3   4
        1   4   2   9   0   9
        2   1   0   7   8   0
        3   5   1   7   1   3
        4   6   0   2   4   2
        >>> col = itercolumns(myDataframe)
        OrderedDict([('Index', 0), ('a', 1), ('b', 2), ('c', 3), ('d', 4), ('e', 5)])
        >>> col['b']
        2
        >>> for row in myDataframe.itertuples(name='SQLdata'):
        ...     if row[col['b']] == row[col['d']]:
        ...             print(row)
        ...
        SQLdata(Index=3, a=5, b=1, c=7, d=1, e=3)
        >>> _col = itercolumns(myDataframe, "e", "a")
        >>> _col
        OrderedDict([('a', 1), ('e', 5)])
        >>> _col['a']
        1
        >>> for row in myDataframe.itertuples():
        ...     if row[_col['a']] >= 5:
        ...         if row[_col['e']] == 0:
        ...             return eval('functionName')()
    """
    if len(colName) == 1:
        match = colName[0]
        for frame in dataframe.itertuples():
            columnsList = frame._asdict()
            columnsList = dict(columnsList)
            i = 0
            while i < len(columnsList):
                if list(columnsList)[i] == match:
                    return i
                i +=1
            break
        raise ValueError('DataFrame did not contain specified column header name')

    if all([_aslist == True]) :
        return list(dataframe)
    
    else:
        if all([_aslist == False, _asdict == True]) :
            for frame in dataframe.itertuples():
                columnsList = frame._asdict()
                columnsList = dict(columnsList)
                columnsDict = OrderedDict()
                i = 0
                for col in list(columnsList):
                    columnsDict[col] = i
                    i += 1
                if len(colName) == 0:
                    return columnsDict
                elif len(colName) >= 1:
                    for argGiven in colName:
                        if argGiven not in columnsList:
                            raise ValueError('Dataframe did not contain specified column header name')
                    return refineDict(columnsDict, *[x for x in colName])
