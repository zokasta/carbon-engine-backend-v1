import importlib
from .Email import EmailValidator
def load_plugin(plugin_id):
    if plugin_id.endswith('.py'):
        plugin_id = plugin_id[:-3]
    
    try:
        # plugin_module = importlib.import_module(f'plugin.{plugin_id}')
        
        # if hasattr(plugin_module, 'get_plugin'):
        #     plugin_instance = plugin_module.get_plugin()
        # else:
        #     plugin_instance = plugin_module
        
        # if not hasattr(plugin_instance, 'run'):
        #     raise ValueError(f"Plugin '{plugin_id}' does not have a 'run' method.")
        
        return EmailValidator()

    except ModuleNotFoundError:
        raise ValueError(f"Plugin '{plugin_id}' not found.")
    except ImportError:
        raise ValueError(f"Error importing plugin '{plugin_id}'.")
