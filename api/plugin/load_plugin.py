import importlib
import os

def load_plugin(plugin_id):
    try:
        plugins_directory = os.path.join(os.path.dirname(__file__), 'plugin')
        
        plugin_module = importlib.import_module(f'plugin.Email.py')
        if not hasattr(plugin_module, 'run'):
            raise ValueError(f"Plugin '{plugin_id}' does not have a 'run' method.")
        
        return plugin_module
        
    except ModuleNotFoundError:
        raise ValueError(f"Plugin '{plugin_id}' not found.")
    except ImportError:
        raise ValueError(f"Error importing plugin '{plugin_id}'.")
