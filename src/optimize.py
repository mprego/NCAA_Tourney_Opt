import pandas as pd
import numpy as np
from ortools.linear_solver import pywraplp

def optimize_tourney(df, opt_var, max_or_min):
    '''
    Given a dataframe predictions of match ups, returns dataframe of optimal predictions
    '''
    solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x_list = {}
    for i in range(len(df)):
        x_list[i] = solver.IntVar(0.0, 1.0, 'x'+str(i))   

    # add game constraints
    for rg in set(df['Slot']):
        constraint = solver.Constraint(1, 1)
        for i in range(len(df)):
            constraint.SetCoefficient(x_list[i], int(df.loc[i, 'Round_Game_'+rg]))

    # adds constraint for each team/round
    teams = set(list(df['TeamID_Strong']) + list(df['TeamID_Weak']))
    for r in set(df['Round']):
        for t in teams:
            col = str(t)+'_'+str(r)
            constraint = solver.Constraint(-50, 1)
            for i in range(len(df)):
               constraint.SetCoefficient(x_list[i], int(df.loc[i, col]))
            
     # sets objective
    opt_vars = opt_var 

    obj = solver.Objective()
    for i in range(len(df)):
        obj.SetCoefficient(x_list[i], int(df.loc[i, opt_vars]))
    
    if max_or_min=='max':
        obj.SetMaximization()
    elif max_or_min=='min':
        obj.SetMinimization()
        
    result_status = solver.Solve()
    assert result_status==0, 'Error in optimization'

    # outputs results
    opt_results = df.copy()

    for i in range(len(df)):
        opt_results.loc[i, 'Chosen'] = x_list[i].solution_value()

    opt_results = opt_results.loc[opt_results['Chosen']==1]
    
    return opt_results


    