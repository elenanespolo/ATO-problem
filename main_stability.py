import gurobipy as gp # type: ignore
import pandas as pd # type: ignore
from gurobipy import GRB # type: ignore
import numpy as np # type: ignore
from model import gurobi_model # type: ignore
from scipy.stats import norm # type: ignore
import matplotlib.pyplot as plt # type: ignore

def compute_in_sample_stability(starting_n_scenario:int = 2, max_iterations:int=50, step_iteration:int = 1, alpha:float = 0.008, df1:pd.DataFrame = None, products_price:dict = None, machine_daily_time:dict = None):
    #
    # This function computes the in-sample stability analysis for the ATO problem with stochastic demand
    #
    # ATTENTION: the function stops as soon as a model is not feasible
    #
    # INPUTS:
    # starting_n_scenario: initial number of scenarios
    # max_iterations: maximum number of iterations
    # step_iteration: increment in the number of scenarios
    # df1: dataframe with n_components rows and (n_machines + n_products +1) columns.
    #   The first n_machines columns are the time in minutes that each component takes in each machine.
    #   The next n_products columns are the gozinto factors for each component.
    #   The last column is the fixed cost of each component.
    # products_price: dictionary with the price of each product
    # machine_daily_time: dictionary with the daily time in minutes available for each machine
    #
    # OUTPUT:
    # n_scenario: when the CLT conditions are satisfied number of scenarios 
    #   otherwise 'No scenario satisfies the CLT conditions' or
    #   'Model not feasible' if the model is not feasible
    # stability_diff_dict: dictionary with the stability difference for each number of scenarios
    #  


    if products_price == None:
        num_items = 2
    else:
        num_items = len(products_price)
    n_scenario = starting_n_scenario
    final_scenario = 'No scenario satisfies the CLT conditions'

    stability_diff_dict = {}
    for iteration in range(max_iterations):
        # Generate two independent sets of scenarios S1 and S2 with cardinality n_scenario
        np.random.seed(42*iteration)
        demand_S1 =  np.random.normal(loc=100, scale=40, size=(n_scenario, num_items)).astype(int)
        demand_S1 = np.clip(demand_S1, 0, None) # Check no values are negative

        np.random.seed(84*iteration+1)
        demand_S2 = np.random.normal(loc=100, scale=40, size=(n_scenario, num_items)).astype(int)
        demand_S2 = np.clip(demand_S2, 0, None)

        # Solve the stochastic models for S1 and S2
        modelS1 = gurobi_model(df1=df1, products_price=products_price, machine_daily_time=machine_daily_time, demand=demand_S1)
        modelS2 = gurobi_model(df1=df1, products_price=products_price, machine_daily_time=machine_daily_time, demand=demand_S2)
        
        if modelS1 is None or modelS2 is None:
            return ('Model not feasible', stability_diff_dict)
        # Compute the stability difference
        stability_diff = abs(modelS1.objVal - modelS2.objVal)
        stability_diff_dict[n_scenario] = stability_diff
        
        # print(f'Mean = {mu}, Standard Deviation = {sigma}, z_alpha = {z_alpha}')
        if iteration == 0:
            n_scenario += step_iteration
        elif final_scenario == 'No scenario satisfies the CLT conditions':
            mu = np.mean(list(stability_diff_dict.values()))
            sigma = np.std(list(stability_diff_dict.values()))
            z_alpha = norm.ppf(1 - alpha / 2)
            # print(mu + z_alpha*sigma/np.sqrt(max_iterations), mu - z_alpha*sigma/np.sqrt(max_iterations))
            
            # Check if the CLT conditions are satisfied
            if mu + z_alpha*sigma/np.sqrt(iteration+1) > 0 and mu - z_alpha*sigma/np.sqrt(iteration+1) < 0:
                final_scenario = n_scenario
            else:
                n_scenario += step_iteration
        else:
            n_scenario += step_iteration
    

    return (final_scenario, stability_diff_dict)

def compute_out_sample_stability(starting_n_scenario:int = 2, big_n_scenario:int = 55, max_iterations:int=50, step_iteration:int = 1, alpha:float = 0.025, df1:pd.DataFrame = None, products_price:dict = None, machine_daily_time:dict = None) -> int:
    #
    # This function computes the out-of-sample stability analysis for the ATO problem with stochastic demand
    #
    # ATTENTION: the function stops as soon as a model is not feasible
    #
    # INPUTS:
    # starting_n_scenario: initial number of scenarios
    # max_iterations: maximum number of iterations
    # step_iteration: increment in the number of scenarios
    # df1: dataframe with n_components rows and (n_machines + n_products +1) columns.
    #   The first n_machines columns are the time in minutes that each component takes in each machine.
    #   The next n_products columns are the gozinto factors for each component.
    #   The last column is the fixed cost of each component.
    # products_price: dictionary with the price of each product
    # machine_daily_time: dictionary with the daily time in minutes available for each machine
    #
    # OUTPUT:
    # n_scenario: when the CLT conditions are satisfied number of scenarios 
    #   otherwise 'No scenario satisfies the CLT conditions' or
    #   'Model not feasible' if the model is not feasible
    # stability_diff_dict: dictionary with the stability difference for each number of scenarios
    #  
    
    if products_price == None:
        num_items = 2
    else:
        num_items = len(products_price)
    n_scenario = starting_n_scenario
    final_scenario = 'No scenario satisfies the CLT conditions'

    stability_diff_dict = {}
    np.random.seed(1)
    demand_bigN = np.random.normal(loc=100, scale=40, size=(big_n_scenario, num_items)).astype(int)
    demand_bigN = np.clip(demand_bigN, 0, None)
    model_bigN = gurobi_model(df1=df1, products_price=products_price, machine_daily_time=machine_daily_time, demand=demand_bigN)
    objVal_bigN = model_bigN.objVal
    for iteration in range(max_iterations):
        # Generate scenario S1 with cardinality n_scenario
        np.random.seed(42*iteration)
        demand_S1 = np.random.normal(loc=100, scale=40, size=(n_scenario, num_items)).astype(int)
        demand_S1 = np.clip(demand_S1, 0, None)

        # Solve the stochastic model for S1
        modelS1 = gurobi_model(df1=df1, products_price=products_price, machine_daily_time=machine_daily_time, demand=demand_S1)
        
        if modelS1 is None:
            return ('Model not feasible', stability_diff_dict)
        # Compute the stability difference
        stability_diff = abs(modelS1.objVal - objVal_bigN)
        stability_diff_dict[n_scenario] = stability_diff
        
        # Check if the stability difference is within the tolerance
        if iteration == 0:
            n_scenario += step_iteration
        elif final_scenario == 'No scenario satisfies the CLT conditions':
            mu = np.mean(list(stability_diff_dict.values()))
            sigma = np.std(list(stability_diff_dict.values()))
            z_alpha = norm.ppf(1 - alpha / 2)
            # print(mu + z_alpha*sigma/np.sqrt(max_iterations), mu - z_alpha*sigma/np.sqrt(max_iterations))
            
            # Check if the CLT conditions are satisfied
            if mu + z_alpha*sigma/np.sqrt(iteration+1) > 0 and mu - z_alpha*sigma/np.sqrt(iteration+1) < 0:
                final_scenario = n_scenario
            else:
                n_scenario += step_iteration
        else:
            n_scenario += step_iteration

    return (final_scenario, stability_diff_dict)

# Perform In-Sample Stability Analysis
n_scenario_in_sample, stability_dict_in_sample = compute_in_sample_stability()

# Perform Out-of-Sample Stability Analysis
bigN = 55
n_scenario_out_sample, stability_dict_out_sample = compute_out_sample_stability(big_n_scenario=bigN)

print(' ')
print('In-Sample Stability Analysis')
if n_scenario_in_sample == 'Model not feasible':
    print(f'Model not feasible')
elif n_scenario_in_sample == 'No scenario satisfies the CLT conditions':
    print(f'No scenario satisfies the CLT conditions')
else:
    print(f'In-Sample Stability achieved with {n_scenario_in_sample} scenarios and stability difference = {stability_dict_in_sample[n_scenario_in_sample]}')

data = []
for i,el in enumerate(stability_dict_in_sample.values()):
    if i == 0:
        data.append(el)
        continue
    elif i == 1:
        el1 = data.pop()
        data.append([el1, el])
    else:
        el1 = data[i-2].copy()
        el1.append(el)
        data.append(el1)
plt.figure(figsize=(15, 10))
plt.boxplot(data)
plt.xticks(ticks=range(len(data)+1), labels=range(2, len(data)+3), rotation=45)
plt.hlines(0, 0, len(data)+1, colors='r', linestyles='dashed')
plt.xlabel('Number of scenarios')
plt.ylabel('Stability difference')
plt.title('In-Sample Stability Analysis')
plt.savefig('in_sample_stability.pdf')


# stability_dict_in_sample = dict(sorted(stability_dict_in_sample.items(), key=lambda x: x[1], reverse=False))
# print('The differences in the objective function value for different scenarios are:')
# for key, value in stability_dict_in_sample.items():
#     print(f'n_scenario = {key}, stability difference = {value}')
print(' ')

print('Out-of-Sample Stability Analysis')
print(f'performed with respect to the {bigN} scenarios')

if n_scenario_out_sample == 'Model not feasible':
    print(f'Model not feasible')
elif n_scenario_out_sample == 'No scenario satisfies the CLT conditions':
    print(f'No scenario satisfies the CLT conditions')
else:
    print(f'Out-of-Sample Stability achieved with {n_scenario_out_sample} scenarios and stability difference = {stability_dict_out_sample[n_scenario_out_sample]}')

data = []
for i,el in enumerate(stability_dict_out_sample.values()):
    if i == 0:
        data.append(el)
        continue
    elif i == 1:
        el1 = data.pop()
        data.append([el1, el])
    else:
        el1 = data[i-2].copy()
        el1.append(el)
        data.append(el1)
plt.figure(figsize=(15, 10))
plt.boxplot(data)
plt.xticks(ticks=range(len(data)+1), labels=range(2, len(data)+3), rotation=45)
plt.hlines(0, 0, len(data)+1, colors='r', linestyles='dashed')
plt.xlabel('Number of scenarios')
plt.ylabel('Stability difference')
plt.title('In-Sample Stability Analysis')
plt.savefig('out_sample_stability.pdf')


# stability_dict_out_sample = dict(sorted(stability_dict_out_sample.items(), key=lambda x: x[1], reverse=False))
# print('The differences in the objective function value for different scenarios are:')
# for key, value in stability_dict_out_sample.items():
#     print(f'n_scenario = {key}, stability difference = {value}')