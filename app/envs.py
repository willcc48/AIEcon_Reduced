# Define the configuration of the environment that will be built

custom_config = {
    # ===== STANDARD ARGUMENTS ======
    'n_agents': 4,          # Number of non-planner agents
    'world_size': [30, 30], # [Height, Width] of the env world
    'episode_length': 1000, # Number of timesteps per episode
    
    # In multi-action-mode, the policy selects an action for each action subspace (defined in component code)
    # Otherwise, the policy selects only 1 action
    'multi_action_mode_agents': False,
    'multi_action_mode_planner': True,
    
    # When flattening observations, concatenate scalar & vector observations before output
    # Otherwise, return observations with minimal processing
    'flatten_observations': False,
    # When Flattening masks, concatenate each action subspace mask into a single array
    # Note: flatten_masks = True is recommended for masking action logits
    'flatten_masks': True,
    
    
    # ===== COMPONENTS =====
    # Which components to use (specified as list of {"component_name": {component_kwargs}} dictionaries)
    #   "component_name" refers to the component class's name in the Component Registry
    #   {component_kwargs} is a dictionary of kwargs passed to the component class
    # The order in which components reset, step, and generate obs follows their listed order below
    'components': [
        # (1) Building houses
        ('Build', dict(skill_dist="pareto", payment_max_skill_multiplier=3)),
        # (2) Trading collectible resources
        ('ContinuousDoubleAuction', dict(max_num_orders=5)),
        # (3) Movement and resource collection
        ('Gather', dict()),
        # (4) Income tax & lump-sum redistribution
        ('PeriodicBracketTax', dict(bracket_spacing="us-federal", period=100))
    ],
    

    # ===== SCENARIO =====
    # Which scenario class to use (specified by the class's name in the Scenario Registry)
    'scenario_name': 'uniform/simple_wood_and_stone'
}


opt_config = {
    # ===== SCENARIO CLASS =====
    # Which Scenario class to use: the class's name in the Scenario Registry (foundation.scenarios).
    # The environment object will be an instance of the Scenario class.
    'scenario_name': 'layout_from_file/simple_wood_and_stone',
    
    # ===== COMPONENTS =====
    # Which components to use (specified as list of ("component_name", {component_kwargs}) tuples).
    #     "component_name" refers to the Component class's name in the Component Registry (foundation.components)
    #     {component_kwargs} is a dictionary of kwargs passed to the Component class
    # The order in which components reset, step, and generate obs follows their listed order below.
    'components': [
        # (1) Building houses
        ('Build', dict(skill_dist="pareto", payment_max_skill_multiplier=3)),
        # (2) Trading collectible resources
        ('ContinuousDoubleAuction', dict(max_num_orders=5)),
        # (3) Movement and resource collection
        ('Gather', dict()),
        # (4) Income tax & lump-sum redistribution
        ('PeriodicBracketTax', dict(bracket_spacing="us-federal", period=100))
    ],
    
    # ===== SCENARIO CLASS ARGUMENTS =====
    # (optional) kwargs that are added by the Scenario class (i.e. not defined in BaseEnvironment)
    'env_layout_file': "quadrant_25x25_20each_30clump.txt",
    'fixed_four_skill_and_loc': True,
    
    # ===== STANDARD ARGUMENTS ======
    # kwargs that are used by every Scenario class (i.e. defined in BaseEnvironment)
    'n_agents': 4,          # Number of non-planner agents (must be >1)
    'world_size': [25, 25], # [Height, Width] of the env world
    'episode_length': 1000, # Number of timesteps per episode
    
    # In multi-action-mode, the policy selects an action for each action subspace (defined in component code).
    # Otherwise, the policy selects only 1 action.
    'multi_action_mode_agents': False,
    'multi_action_mode_planner': True,
    
    # When flattening observations, concatenate scalar & vector observations before output.
    # Otherwise, return observations with minimal processing.
    'flatten_observations': False,
    # When Flattening masks, concatenate each action subspace mask into a single array.
    # Note: flatten_masks = True is required for masking action logits in the code below.
    'flatten_masks': True,
}

covid_config = {
    # Scenario name - determines which scenario class to use
    "scenario_name": "CovidAndEconomySimulation",
    
    # The list of components in this simulation
    "components": [
        {"ControlUSStateOpenCloseStatus": {
            # action cooldown period in days.
            # Once a stringency level is set, the state(s) cannot switch to another level
            # for a certain number of days (referred to as the "action_cooldown_period")
            "action_cooldown_period": 28
        }},
        {"FederalGovernmentSubsidy": {
            # The number of subsidy levels.
            "num_subsidy_levels": 20,
            # The number of days over which the total subsidy amount is evenly rolled out.
            "subsidy_interval": 90,
            # The maximum annual subsidy that may be allocated per person.
            "max_annual_subsidy_per_person": 20000,
        }},
        {"VaccinationCampaign": {
            # The number of vaccines available per million people everyday.
            "daily_vaccines_per_million_people": 3000,
            # The number of days between vaccine deliveries.
            "delivery_interval": 1,
            # The date (YYYY-MM-DD) when vaccination begins
            "vaccine_delivery_start_date": "2021-01-12",
        }},
    ],

    # Date (YYYY-MM-DD) to start the simulation.
    "start_date": "2020-03-22",
    # How long to run the simulation for (in days)
    "episode_length": 405,
    
    # use_real_world_data (bool): Replay what happened in the real world.
    # Real-world data comprises SIR (susceptible/infected/recovered),
    # unemployment, government policy, and vaccination numbers.
    # This setting also sets use_real_world_policies=True.
    "use_real_world_data": False,
    # use_real_world_policies (bool): Run the environment with real-world policies
    # (stringency levels and subsidies). With this setting and
    # use_real_world_data=False, SIR and economy dynamics are still
    # driven by fitted models.
    "use_real_world_policies": False,
    
    # A factor indicating how much more the
    # states prioritize health (roughly speaking, loss of lives due to
    # opening up more) over the economy (roughly speaking, a loss in GDP
    # due to shutting down resulting in more unemployment) compared to the
    # real-world.
    # For example, a value of 1 corresponds to the health weight that 
    # maximizes social welfare under the real-world policy, while
    # a value of 2 means that states care twice as much about public health
    # (preventing deaths), while a value of 0.5 means that states care twice
    # as much about the economy (preventing GDP drops).
    "health_priority_scaling_agents": 1,
    # Same as above for the planner
    "health_priority_scaling_planner": 1,
    
    # Full path to the directory containing
    # the data, fitted parameters and model constants. This defaults to
    # "ai_economist/datasets/covid19_datasets/data_and_fitted_params".
    # For details on obtaining these parameters, please see the notebook
    # "ai-economist-foundation/ai_economist/datasets/covid19_datasets/
    # gather_real_world_data_and_fit_parameters.ipynb".
    "path_to_data_and_fitted_params": "",
    
    # Economy-related parameters
    # Fraction of people infected with COVID-19. Infected people don't work.
    "infection_too_sick_to_work_rate": 0.1,
    # Fraction of the population between ages 18-65.
    # This is the subset of the population whose employment/unemployment affects
    # economic productivity.
    "pop_between_age_18_65": 0.6,
    # Percentage of interest paid by the federal
    # government to borrow money from the federal reserve for COVID-19 relief
    # (direct payments). Higher interest rates mean that direct payments
    # have a larger cost on the federal government's economic index.
    "risk_free_interest_rate": 0.03,
    # CRRA eta parameter for modeling the economic reward non-linearity.
    "economic_reward_crra_eta": 2,
       
    # Number of agents in the simulation (50 US states + Washington DC)
    "n_agents": 51,    
    # World size: Not relevant to this simulation, but needs to be set for Foundation
    "world_size": [1, 1],
    # Flag to collate all the agents' observations, rewards and done flags into a single matrix
    "collate_agent_step_and_reset_data": True,
}