# Theme Configuration for AWE Electronics
# Modify these values to customize the appearance of your application

class Theme:
    """
    Centralized theme configuration for AWE Electronics GUI
    """
    
    # Color Palette
    COLORS = {
        # Primary Colors
        'primary': '#007bff',           # Main blue for primary actions
        'primary_dark': '#0056b3',      # Darker blue for hover states
        'primary_light': '#6bb6ff',     # Lighter blue for accents
        
        # Secondary Colors
        'secondary': '#6c757d',         # Gray for secondary actions
        'secondary_dark': '#545b62',    # Darker gray for hover
        'secondary_light': '#adb5bd',   # Light gray for text
        
        # Status Colors
        'success': '#28a745',           # Green for success/positive actions
        'success_dark': '#218838',      # Darker green for hover
        'warning': '#ffc107',           # Yellow for warnings
        'warning_dark': '#e0a800',      # Darker yellow for hover
        'danger': '#dc3545',            # Red for danger/delete actions
        'danger_dark': '#c82333',       # Darker red for hover
        'info': '#17a2b8',              # Cyan for information
        'info_dark': '#138496',         # Darker cyan for hover
        
        # Background Colors
        'bg_primary': '#f8f9fa',        # Main background (light gray)
        'bg_secondary': '#e9ecef',      # Secondary background
        'bg_dark': '#343a40',           # Dark background for headers
        'bg_white': '#ffffff',          # Pure white for cards
        'bg_light': '#f8f9fa',          # Light background
        
        # Text Colors
        'text_primary': '#2c3e50',      # Main text color (dark blue-gray)
        'text_secondary': '#6c757d',    # Secondary text (gray)
        'text_muted': '#8d9db6',        # Muted text for less important info
        'text_white': '#ffffff',        # White text for dark backgrounds
        'text_success': '#28a745',      # Green text for success messages
        'text_danger': '#dc3545',       # Red text for errors
        
        # Border Colors
        'border_light': '#dee2e6',      # Light border for cards
        'border_dark': '#6c757d',       # Dark border for emphasis
    }
    
    # Typography
    FONTS = {
        'primary': ('Segoe UI', 'San Francisco', 'Ubuntu', 'sans-serif'),
        'monospace': ('Consolas', 'Monaco', 'Courier New', 'monospace'),
        
        # Font Sizes
        'size_small': 9,
        'size_normal': 11,
        'size_medium': 12,
        'size_large': 14,
        'size_xlarge': 16,
        'size_xxlarge': 20,
        'size_title': 28,
    }
    
    # Spacing
    SPACING = {
        'xs': 5,        # Extra small spacing
        'sm': 10,       # Small spacing
        'md': 15,       # Medium spacing
        'lg': 20,       # Large spacing
        'xl': 30,       # Extra large spacing
        'xxl': 40,      # Extra extra large spacing
    }
    
    # Component Styles
    COMPONENTS = {
        # Button padding (horizontal, vertical)
        'button_padding': (20, 12),
        'button_padding_small': (15, 8),
        'button_padding_large': (25, 15),
        
        # Border radius for rounded corners
        'border_radius': 4,
        'border_radius_large': 8,
        
        # Card shadows and elevation
        'card_relief': 'raised',
        'card_border_width': 1,
        
        # Input field styling
        'input_padding': 12,
        'input_border_width': 2,
    }
    
    # Window Configuration
    WINDOWS = {
        # Default window sizes
        'start_window': (500, 600),
        'login_window': (450, 550),
        'register_window': (500, 700),
        'customer_window': (1000, 700),
        'admin_window': (1200, 800),
        
        # Minimum window sizes
        'min_customer': (800, 600),
        'min_admin': (1000, 700),
    }
    
    # Custom Themes (Alternative color schemes)
    THEMES = {
        'default': {
            'name': 'AWE Default',
            'primary': '#007bff',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'bg_primary': '#f8f9fa',
        },
        
        'dark': {
            'name': 'Dark Mode',
            'primary': '#375a7f',
            'success': '#00bc8c',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'bg_primary': '#2c3e50',
        },
        
        'corporate': {
            'name': 'Corporate Blue',
            'primary': '#1e3d59',
            'success': '#2ecc40',
            'warning': '#ff851b',
            'danger': '#dc3545',
            'bg_primary': '#f4f4f4',
        },
        
        'modern': {
            'name': 'Modern Purple',
            'primary': '#6f42c1',
            'success': '#51cf66',
            'warning': '#ffd43b',
            'danger': '#ff6b6b',
            'bg_primary': '#f8f9fa',
        }
    }
    
    @classmethod
    def get_color(cls, color_name):
        """Get color value by name"""
        return cls.COLORS.get(color_name, '#000000')
    
    @classmethod
    def get_font(cls, font_type='primary', size='normal'):
        """Get font configuration"""
        font_family = cls.FONTS[font_type][0]  # Get first font in family
        font_size = cls.FONTS.get(f'size_{size}', cls.FONTS['size_normal'])
        return (font_family, font_size)
    
    @classmethod
    def get_font_bold(cls, font_type='primary', size='normal'):
        """Get bold font configuration"""
        font_family = cls.FONTS[font_type][0]
        font_size = cls.FONTS.get(f'size_{size}', cls.FONTS['size_normal'])
        return (font_family, font_size, 'bold')
    
    @classmethod
    def get_spacing(cls, size='md'):
        """Get spacing value"""
        return cls.SPACING.get(size, cls.SPACING['md'])
    
    @classmethod
    def apply_theme(cls, theme_name='default'):
        """Apply a different theme"""
        if theme_name in cls.THEMES:
            theme = cls.THEMES[theme_name]
            # Update colors with theme values
            for key, value in theme.items():
                if key != 'name' and key in cls.COLORS:
                    cls.COLORS[key] = value
    
    @classmethod
    def get_button_style_config(cls, button_type='primary'):
        """Get complete button style configuration"""
        color_map = {
            'primary': (cls.COLORS['primary'], cls.COLORS['primary_dark']),
            'secondary': (cls.COLORS['secondary'], cls.COLORS['secondary_dark']),
            'success': (cls.COLORS['success'], cls.COLORS['success_dark']),
            'warning': (cls.COLORS['warning'], cls.COLORS['warning_dark']),
            'danger': (cls.COLORS['danger'], cls.COLORS['danger_dark']),
            'info': (cls.COLORS['info'], cls.COLORS['info_dark']),
        }
        
        bg_color, hover_color = color_map.get(button_type, color_map['primary'])
        
        return {
            'background': bg_color,
            'activebackground': hover_color,
            'foreground': cls.COLORS['text_white'],
            'font': cls.get_font_bold(size='medium'),
            'borderwidth': 0,
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': cls.COMPONENTS['button_padding'][0],
            'pady': cls.COMPONENTS['button_padding'][1],
        }

# Convenience functions for easy access
def get_color(name):
    """Quick access to colors"""
    return Theme.get_color(name)

def get_font(size='normal', bold=False):
    """Quick access to fonts"""
    if bold:
        return Theme.get_font_bold(size=size)
    return Theme.get_font(size=size)

def get_spacing(size='md'):
    """Quick access to spacing"""
    return Theme.get_spacing(size)

# Example usage:
# from theme_config import get_color, get_font, get_spacing
# 
# # In your GUI code:
# my_button = tk.Button(parent, 
#                       text="Click Me", 
#                       bg=get_color('primary'),
#                       font=get_font('large', bold=True),
#                       padx=get_spacing('lg'))