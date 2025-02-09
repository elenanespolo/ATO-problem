import gurobipy as gp # type: ignore
from gurobipy import GRB # type: ignore
import pandas as pd # type: ignore
import numpy as np # type: ignore
import csv

def gurobi_model_variables(df1:pd.DataFrame = None, products_price:dict = None, machine_daily_time:dict = None, demand:list = None, prob:list = None, path:str = None):
    #
    # This function creates a gurobi model to solve the ATO problem with stochastic demand
    #
    # INPUTS:
    # df1: dataframe with n_components rows and (n_machines + n_products +1) columns. 
    #   The first n_machines columns are the time in minutes that each component takes in each machine.
    #   The next n_products columns are the gozinto factors for each component.
    #   The last column is the fixed cost of each component.
    # products_price: dictionary with the price of each product
    # machine_daily_time: dictionary with the daily time in minutes available for each machine 
    # demand: list with the demand of each product in each scenario
    # prob: list with the probability of each scenario
    # path: path to the data files if the function is called from a different directory
    # 
    # OUTPUT:
    # model_stochastic: optimized model 
    # ATTENTION: when it is not possible to find an optimal solution, the function returns None
    
    # if the input is not provided, use the default values

    if df1 is None:
        df1, products_price, machine_daily_time, products, num_components, num_items, num_machines = get_data(path = path)

    if demand is None:
        np.random.seed(42)
        demand = np.random.normal(loc=100, scale=40, size=num_items).astype(int)
        demand = np.clip(demand, 0, None)
        demand = [demand]
        prob = [1]
    else:
        if prob is None:
            prob = [1/len(demand)]*len(demand)
    num_scenarios = len(demand)

    # Create a new model
    model_stochastic = gp.Model("ato")
    model_stochastic.setParam('OutputFlag', 0)

    # Decision variables
    # y[j] is the amount of product j produced
    y = model_stochastic.addVars(num_items, num_scenarios, vtype=GRB.INTEGER, name="y")

    # x[i] is the number of i components 
    x = model_stochastic.addVars(num_components, vtype=GRB.INTEGER, name="x")

    # Objective function: minimize fixed costs + transportation costs
    model_stochastic.setObjective(
        - gp.quicksum(df1.iloc[i,-1] * x[i] for i in range(num_components) ) +
        gp.quicksum(prob[s] * gp.quicksum(products_price[products[j]] * y[j, s] for j in range(num_items)) for s in range(num_scenarios)),
        GRB.MAXIMIZE
    )

    # Constraint 1: the amount of hours of work for every piece must be inferior to the threshold for the machine
    model_stochastic.addConstrs(
        (gp.quicksum(df1.iloc[i,j] * x[i] for i in range(num_components)) <= machine_daily_time[list(machine_daily_time.keys())[j]]*7 for j in range(num_machines) ),
        name="working_hours"
    )

    # Constraint 2: the number of products of every type must be geq the demand
    model_stochastic.addConstrs(
        (y[j, s] <= demand[s][j] for j in range(num_items) for s in range(num_scenarios)),
        name = "qty_products"
    )

    # Constraint 3: gozinto factor
    model_stochastic.addConstrs(
        (gp.quicksum(df1.iloc[i,j+num_machines] * y[j, s] for j in range(num_items)) <= x[i] for i in range(num_components) for s in range(num_scenarios)),
        name="gozinto"
    )

    ## Optimize the model
    model_stochastic.optimize()

    ## Output solution details
    if model_stochastic.status == GRB.OPTIMAL:
        return (model_stochastic, y, x)
    else:
        print("No optimal solution found.")
        return (None, None, None)

def gurobi_model(df1:pd.DataFrame = None, products_price:dict = None, machine_daily_time:dict = None, demand:list = None, prob:list = None, path:str = None):
    (model_stochastic, y, x) = gurobi_model_variables(df1 = df1, products_price = products_price, machine_daily_time = machine_daily_time, demand = demand, prob = prob, path = path)
    return model_stochastic
    
def get_data(path:str = None):
    # This function reads the data from the csv files
    if path is None:
        file_path = 'data/'
    else:
        file_path = f'{path}data/'
    df1 = pd.read_csv(f'{file_path}components_data.csv', index_col=0)
    with open(f'{file_path}products_machines.csv', 'r') as f:
        reader = csv.reader(f)
        num_items, num_machines = next(reader)
        num_items = int(num_items)
        num_machines = int(num_machines)
        products_price = {}
        for i in range(num_items):
            p, s = next(reader)
            products_price[p] = int(s)
        machine_daily_time = {}
        for i in range(num_machines):
            m, t = next(reader)
            machine_daily_time[m] = int(t)
    num_components = len(df1)
    products = list(products_price.keys())
    return df1, products_price, machine_daily_time, products, num_components, num_items, num_machines
