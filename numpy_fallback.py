# NumPy Fallback for Smart Music Generator AI
"""
This module provides basic numpy-like functionality when numpy is not available.
"""

class NumpyFallback:
    """Fallback implementation for basic numpy operations"""
    
    @staticmethod
    def array(values):
        """Create array-like list"""
        return list(values)
    
    @staticmethod
    def mean(values):
        """Calculate mean of values"""
        return sum(values) / len(values) if values else 0
    
    @staticmethod
    def clip(value, min_val, max_val):
        """Clip value between min and max"""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def random():
        """Access to random module"""
        import random
        return random
    
    def __version__(self):
        return "fallback-1.0"

# Create numpy-like interface
numpy_fallback = NumpyFallback()
