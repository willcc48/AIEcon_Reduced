# AI Economist Policy
Web dashboard and extension of Salesforce's AI Economist multi-agent reinforcement learning tax policy environment. Streamlit is being used as a Python web framework. Conda environment used with Python 3.7. ai_economist directory holds base code and agent models, etc.

Setup conda environment and clone project:

      conda create -n "env_name" python=3.7
      conda activate env_name
      git clone https://github.com/willcc48/AIEcon_Reduced.git

*******No need to install ai-economist

*******If training, edit config.yaml in phase1/2 directory...

*******Look for CPU, GPU, workers, episode length, etc

Install Streamlit for web:

      pip install streamlit

Typical packages are needed like matplotlib, numpy (use conda environment). In app folder:

      streamlit run app.py

To push changes to main branch:

      git add .
      git commit -m "commit message"
      git push -u origin main
