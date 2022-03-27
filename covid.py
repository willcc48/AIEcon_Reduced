import streamlit as st
from ai_economist import foundation
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

# Helper function: useful for generating arbitrary actions
def generate_actions(env, type="random", episode_length=None, seed=None):
    if episode_length is None:
        episode_length = env.episode_length
    if seed is not None:
        np.random.rand(seed)

    action_seq = [None for _ in range(episode_length)]
    num_agents = env.n_agents
    agent_action_spaces = env.all_agents[0].action_spaces
    planner_action_spaces = env.all_agents[-1].action_spaces

    for timestep in range(episode_length):

        actions = {}
        if type == "real_world":
            # For these cases, we do not need to explicitly provide external actions.
            pass
        
        elif type == "random":
            actions = {str(agent_id): np.random.randint(agent_action_spaces) 
                       for agent_id in range(num_agents)}
            actions['p'] = np.random.randint(planner_action_spaces)
            
        elif type == "states_open_no_subsidies":
            actions = {str(agent_id): np.array([1]) for agent_id in range(num_agents)}
            actions['p'] = np.zeros_like(planner_action_spaces)
            
        elif type == "states_closed_full_subsidies":
            actions = {str(agent_id): np.array([agent_action_spaces - 1]) 
                             for agent_id in range(num_agents)}
            actions['p'] = np.array(planner_action_spaces) - 1
            
        elif type == "states_closed_6_months_no_subsidies":
            if timestep < 6 * 30:
                actions = {str(agent_id): np.array([agent_action_spaces - 1]) 
                                 for agent_id in range(num_agents)}
            else:
                actions = {str(agent_id): np.array([1]) for agent_id in range(num_agents)}
            actions['p'] = np.zeros_like(planner_action_spaces)

        else:
            raise NotImplementedError

        action_seq[timestep] = actions

    return action_seq

# Helper function to fetch environment dense logs

def fetch_env_dense_log(
    env_config,
    action_type="real_world"
):
    env = foundation.make_env_instance(**env_config)
    env.reset(force_dense_logging=True)
    
    action_seq = generate_actions(env, action_type)

    for t in range(env.episode_length):
        env.step(action_seq[t]);
    return env._dense_log

def init(iters, num_agents):
    import envs
    cfg = envs.opt_config
    cfg['episode_length'] = iters
    cfg['n_agents'] = num_agents
    envs = foundation.make_env_instance(**cfg)
    obs = envs.reset()
    return envs, obs

def sim_page(iterations, plt_every, num_agents, save):
    st.title('COVID-19 Policy')
    st.text("")

    # Set font size for the matplotlib figures
    plt.rcParams.update({'font.size': 26})

    if st.button("Run Simulation"):
        st.markdown("***")
        st.write("Running...")

        real_world_env_config = env_config.copy()
        real_world_env_config.update(
            {
                "use_real_world_data": True,
                "use_real_world_policies": True   
            }
        )
        dense_logs["real_world"] = fetch_env_dense_log(
            real_world_env_config,
            action_type="real_world"
        )

        env, obs = init(iterations, num_agents)
        placeholder = st.empty()
m
        play_random_episode(env, obs, placeholder, plot_every=plt_every, save=save)

        fig0, fig1, fig2 = breakdown(env)

        st.subheader("Analytics")
        st.pyplot(fig0)
        st.pyplot(fig1)
        st.pyplot(fig2)