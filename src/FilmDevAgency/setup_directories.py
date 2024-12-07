import os

def setup_agent_directories():
    # List of agents
    agents = [
        'CreativeDirector',
        'Researcher',
        'BrainstormingAgent',
        'IdeationAgent',
        'Scriptwriter1',
        'Scriptwriter2'
    ]
    
    # Required subdirectories for each agent
    subdirs = ['files', 'schemas', 'tools']
    
    # Get the base directory (where this script is located)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create directories for each agent
    for agent in agents:
        agent_dir = os.path.join(base_dir, agent)
        os.makedirs(agent_dir, exist_ok=True)
        
        # Create subdirectories for each agent
        for subdir in subdirs:
            subdir_path = os.path.join(agent_dir, subdir)
            os.makedirs(subdir_path, exist_ok=True)
            
            # Create an empty .gitkeep file to ensure the directory is tracked by git
            gitkeep_path = os.path.join(subdir_path, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    pass

if __name__ == '__main__':
    setup_agent_directories() 