import streamlit as st
import custom
import optimal
#import covid

if __name__ == '__main__':

    st.set_page_config(
        page_title='MARL Market Policy',
        page_icon='🧊',
        initial_sidebar_state='expanded'
    )

    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    PAGES = {
        'Custom AI Economist': custom,
        'COVID-19': None,
        'Climate Policy': None,
        'Learn More...': None,
    }

    DYNAMIC_STATIC = {
        'uniform/simple_wood_and_stone': 'uniform/simple_wood_and_stone'
        """
        'layout_from_file/simple_wood_and_stone': 'layout_from_file/simple_wood_and_stone',
        """
    }

    MAPS = {
        'quadrant_25x25_20each_30clump.txt': 'quadrant_25x25_20each_30clump.txt'
        """
        'open_35x35_gold.txt': 'open_35x35_gold.txt',
        'closed_quadrant_25x25_20each_30clump.txt': 'closed_quadrant_25x25_20each_30clump.txt',
        'env-pure_and_mixed-15x15.txt': 'env-pure_and_mixed-15x15.txt',
        'env-pure_and_mixed-25x25.txt': 'env-pure_and_mixed-25x25.txt',
        'env-pure_and_mixed-40x40.txt': 'env-pure_and_mixed-40x40.txt',
        'quadrant_8x8_4each_8clump.txt': 'quadrant_8x8_4each_8clump.txt',
        'quadrant_25x25_20each_30clump_no_water.txt': 'quadrant_25x25_20each_30clump_no_water.txt',
        'quadrant_25x25_20each_30clump.txt': 'quadrant_25x25_20each_30clump.txt',
        'quadrant_40x40_50each_no_water.txt': 'quadrant_40x40_50each_no_water.txt',
        'quadrant_40x40_50each.txt': 'quadrant_40x40_50each.txt',
        'top_wood_bottom_stone_14x14.txt': 'top_wood_bottom_stone_14x14.txt',
        'uniform_25x25_25each_65clump.txt': 'uniform_25x25_25each_65clump.txt',
        """
    }

    model_select = st.sidebar.radio('Select Page', list(PAGES.keys()))

    st.sidebar.markdown('***')
    st.sidebar.title('Customization')
    st.sidebar.markdown(' ')
    st.sidebar.markdown(' ')

    num_agents = st.sidebar.number_input('Number of Agents', value=4, min_value=2)
    world_size = st.sidebar.number_input('World Size', value=25, min_value=num_agents)
    scenario_name = st.sidebar.selectbox('Choose Dynamic or Static Resources', DYNAMIC_STATIC.keys())
    env_layout_file = st.sidebar.selectbox('Choose a Map', MAPS.keys(), )

    st.sidebar.markdown('***')
    animate = st.sidebar.checkbox('Animate?', value=True)
    save = st.sidebar.checkbox('Save to gif?', value=False, disabled=(not animate))
    iterations = st.sidebar.number_input('Steps', value=1000, min_value=1, disabled=(not animate))
    plt_every = st.sidebar.number_input('Step size', value=100, min_value=1, disabled=(not animate))

    page = PAGES[model_select]
    page.sim_page(iterations, animate, plt_every, num_agents, save, world_size, DYNAMIC_STATIC[scenario_name])
    