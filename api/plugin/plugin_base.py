# plugin_base.py

class PluginBase:
    def __init__(self, data):
        self.data = data

    def apply(self):
        """
        This method will be implemented by each plugin
        to apply its custom functionality to the data.
        """
        raise NotImplementedError("Plugins must implement the `apply` method.")
