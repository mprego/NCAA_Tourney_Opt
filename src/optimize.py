from ortools.linear_solver import pywraplp

def optimize_tourney(df, opt_var):
    '''
    Given a dataframe predictions of match ups, returns dataframe of optimal predictions
    '''



def _optimize_tourney_helper(df, opt_var, constraint_min, constraint_max):
    # creates solver instance and creates decision variable
    solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x_list = {}
    for i in range(len(df)):
        x_list[i] = solver.IntVar(0.0, 1.0, 'x'+str(i))

    # adds constraints
    for col in ['x']:


    # sets objective
    obj = solver.Objective()
    for i in range(len(df)):
        obj.SetCoefficient(x_list[i], int(df.loc[i, opt_vars]))
    obj.SetMaximization()


def create_nba_fd_lineup(opt_input, drop_lowest, budget=60000, max_p=9):
    '''
    Solves NBA FD Lineup
    '''

    # creates solver instance and creates decision variable
    solver = pywraplp.Solver('SolveIntegerProblem', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x_list = {}
    for i in range(len(opt_input)):
        x_list[i] = solver.IntVar(0.0, 1.0, 'x'+str(i))

    # adds drop lowest constraint
    if drop_lowest:
        constraint_min_salary = solver.Constraint(1, max_p)
        for i in range(len(opt_input)):
            constraint_min_salary.SetCoefficient(x_list[i], int(opt_input.loc[i, 'min_salary']))

    # Adds constraints for number of position players
    constraint_c = solver.Constraint(1,1)
    for i in range(len(opt_input)):
        constraint_c.SetCoefficient(x_list[i], int(opt_input.loc[i, 'Position_C']))

    constraint_pg = solver.Constraint(2,2)
    for i in range(len(opt_input)):
        constraint_pg.SetCoefficient(x_list[i], int(opt_input.loc[i, 'Position_PG']))

    constraint_sg = solver.Constraint(2,2)
    for i in range(len(opt_input)):
        constraint_sg.SetCoefficient(x_list[i], int(opt_input.loc[i, 'Position_SG']))

    constraint_sf = solver.Constraint(2,2)
    for i in range(len(opt_input)):
        constraint_sf.SetCoefficient(x_list[i], int(opt_input.loc[i, 'Position_SF']))

    constraint_pf = solver.Constraint(2,2)
    for i in range(len(opt_input)):
        constraint_pf.SetCoefficient(x_list[i], int(opt_input.loc[i, 'Position_PF']))

    # adds constraint for salary
    constraint_sal = solver.Constraint(0, budget)
    for i in range(len(opt_input)):
        constraint_sal.SetCoefficient(x_list[i], int(opt_input.loc[i, 'Salary']))

    # sets objective
    obj = solver.Objective()
    for i in range(len(opt_input)):
        obj.SetCoefficient(x_list[i], int(opt_input.loc[i, 'p_FD']))
    obj.SetMaximization()

    # Solves optimization
    result_status = solver.Solve()
    opt_results = opt_input.copy()

    for i in range(len(opt_input)):
        opt_results.set_value(i, 'Play', x_list[i].solution_value())

    lineup = opt_results.loc[opt_results['Play']==1][['Player', 'Team', 'Date', 'p_FD']]

    return lineup
