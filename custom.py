import streamlit as st
import matplotlib.pyplot as plt
import IPython.display as display

import numpy as np
import plotting
from ai_economist import foundation

def sample_random_action(agent, mask):
    if agent.multi_action_mode:
        split_masks = np.split(mask, agent.action_spaces.cumsum()[:-1])
        return [np.random.choice(np.arange(len(m_)), p=m_/m_.sum()) for m_ in split_masks]

    else:
        return np.random.choice(np.arange(agent.action_spaces), p=mask/mask.sum())

def sample_random_actions(env, obs):        
    actions = {
        a_idx: sample_random_action(env.get_agent(a_idx), a_obs['action_mask'])
        for a_idx, a_obs in obs.items()
    }

    return actions

def do_plot(env, ax):
    plotting.plot_env_state(env, ax)
    ax.set_aspect('equal')

def fig2nparr(fig):
    fig.canvas.draw()
 
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
 
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

def init(iters, num_agents):
    import envs
    cfg = envs.opt_config
    cfg['episode_length'] = iters
    cfg['n_agents'] = num_agents
    envs = foundation.make_env_instance(**cfg)
    obs = envs.reset()
    return envs, obs

def breakdown(env):
    dense_log = env.previous_episode_dense_log
    (fig0, fig1, fig2), _, _, _, _ = plotting.breakdown(dense_log)
    return fig0, fig1, fig2

def play_random_episode(env, obs, placeholder, animate, plot_every, save):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    obs = env.reset(force_dense_logging=True)

    if save: frames = []
    for t in range(env.episode_length):
        actions = sample_random_actions(env, obs)
        obs, rew, done, info = env.step(actions)
        
        if animate:
            display.clear_output(wait=True)
            if ((t+1) % plot_every) == 0:
                do_plot(env, ax)
                np_img = fig2nparr(fig)
                placeholder.image(fig2nparr(fig))
                if save: frames.append(np_img)
    if animate:
        display.clear_output(wait=True)
        if ((t+1) % plot_every) != 0:
            do_plot(env, ax)
            np_img = fig2nparr(fig)
            placeholder.image(fig2nparr(fig))
            if save: frames.append(np_img)    
        
        if save:
            save_file = './gifs/opt.gif'
            fps = 5

            from moviepy.editor import ImageSequenceClip
            gif = ImageSequenceClip(list(frames), fps=fps)
            gif.write_gif(save_file, fps=fps)
        
            st.write(f"gif saved to: {save_file}")

def sim_page(iterations, animate, plt_every, num_agents, save):
    st.title('Custom Simulation')
    st.text("")

    if st.button("Run Simulation"):
        st.markdown("***")
        st.write("Running...")

        env, obs = init(iterations, num_agents)
        placeholder = st.empty()

        play_random_episode(env, obs, placeholder, animate, plt_every, save)
        st.write("Done!")

        fig0, fig1, fig2 = breakdown(env)

        st.subheader("Analytics")
        st.pyplot(fig0)
        st.pyplot(fig1)
        st.pyplot(fig2)