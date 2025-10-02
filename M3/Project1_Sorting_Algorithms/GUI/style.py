"""
Catppuccin Mocha Theme Styling for Tkinter GUI
----------------------------------------------
Provides color and font constants and helper functions to style Tkinter widgets
according to the Catppuccin Mocha theme with a yellow accent.
"""

# Base colors
BG_COLOR = "#1e1e2e"           # Base background color
BUTTON_COLOR = "#f9e2af"       # Yellow (Catppuccin Mocha)
BUTTON_TEXT_COLOR = "#1e1e2e"  # Base (for contrast)
LABEL_COLOR = "#cdd6f4"        # Text color

# Fonts
TITLE_FONT = ("Helvetica", 20, "bold")
BUTTON_FONT = ("Helvetica", 14)
LABEL_FONT = ("Helvetica", 12)

# Accent color
ACCENT_COLOR = "#89b4fa"       # Blue for active/hover

# Window size
WINDOW_SIZE = "600x400"

def style_button(btn, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=BUTTON_FONT):
    """
    Apply Catppuccin style to a Tkinter Button widget.
    """
    btn.config(
        bg=bg,
        fg=fg,
        font=font,
        width=18,
        pady=5,
        activebackground=ACCENT_COLOR,   # Blue when pressed/hovered
        activeforeground=BG_COLOR        # Dark background for text when pressed
    )

def style_label(lbl, fg=LABEL_COLOR, bg=BG_COLOR, font=LABEL_FONT):
    """
    Apply Catppuccin style to a Tkinter Label widget.
    """
    lbl.config(fg=fg, bg=bg, font=font)