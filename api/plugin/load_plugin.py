import importlib
import os

def load_plugin(plugin_id):
    try:
        # Define the path to the plugins directory
        plugins_directory = os.path.join(os.path.dirname(__file__), 'plugins')
        
        # Import the plugin module dynamically
        plugin_module = importlib.import_module(f'plugins.{plugin_id}')
        
        # Assuming each plugin has a 'run' method
        if not hasattr(plugin_module, 'run'):
            raise ValueError(f"Plugin '{plugin_id}' does not have a 'run' method.")
        
        return plugin_module
        
    except ModuleNotFoundError:
        raise ValueError(f"Plugin '{plugin_id}' not found.")
    except ImportError:
        raise ValueError(f"Error importing plugin '{plugin_id}'.")
