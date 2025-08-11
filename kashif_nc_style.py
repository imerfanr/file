import sys
import os
import time
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, VSplit, Window
from prompt_toolkit.widgets import Frame, TextArea
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit import print_formatted_text as printft

# Norton Commander Colors
NC_STYLE = Style.from_dict({
    "frame.label": "bold white on #005fff",
    "frame.border": "ansiblue",
    "window.border": "ansiyellow",
    "menu": "bold black on #ffff55",
    "menu-bar": "bold white on #005fff",
    "footer": "black on #ffff55",
    "body": "white on #0000aa",
    "text": "white on #0000aa",
    "status": "bold black on #ffff55",
    "selected": "bold white on #ff9933",
})

# The classic NC header and footer
HEADER = [
    ("class:menu-bar", "  F1 Help   F2 Menu   F3 View   F4 Edit   F5 Copy   F6 RenMov   F7 Mkdir   F8 Delete   F9 PullDn   F10 Quit")
]
FOOTER = [
    ("class:footer", " Left: [User Files]    Right: [Scan Results]    |    Ctrl-Tab: Switch | Tab: Next | q: Quit ")
]

def nc_menu():
    # Simulate a Norton Commander menu bar as a single line.
    return Window(
        content=FormattedTextControl(HEADER),
        height=1,
        style="class:menu-bar"
    )

def nc_footer():
    return Window(
        content=FormattedTextControl(FOOTER),
        height=1,
        style="class:footer"
    )

def nc_panel(title, content, selected=False):
    # content: str for display (simulate file list or results)
    style = "class:frame.label" if selected else "class:body"
    return Frame(
        TextArea(
            text=content,
            style="class:text",
            read_only=True,
            width=38,
            height=18,
            scrollbar=True,
        ),
        title=title,
        style=style,
        width=40,
        height=20,
    )

def main():
    # Simulate file list and scan results
    file_panel = nc_panel("User Files", "iran_states_cities.json\nfind-miner-ip_advanced.py\nminer_hunter.py\n...", selected=True)
    results_panel = nc_panel("Scan Results", "No scan yet.\nPress F5 to start scan.", selected=False)

    # Main layout
    body = VSplit(
        [
            file_panel,
            Window(width=2, char=" ", style="bg:#0000aa"),
            results_panel,
        ],
        style="class:body"
    )

    # Key bindings
    kb = KeyBindings()
    focused = {"panel": 0}  # 0: left, 1: right

    @kb.add("tab")
    def _(event):
        focused["panel"] = 1 - focused["panel"]
        # Visually mark selection
        if focused["panel"] == 0:
            file_panel.style = "class:frame.label"
            results_panel.style = "class:body"
        else:
            file_panel.style = "class:body"
            results_panel.style = "class:frame.label"
        event.app.layout.focus(file_panel if focused["panel"] == 0 else results_panel)

    @kb.add("c-q")
    @kb.add("q")
    @kb.add("f10")
    def _(event):
        event.app.exit()

    @kb.add("f5")
    def _(event):
        # Simulate scan (replace with your real scan function)
        results_panel.body.text = "Scan started...\nScanning IPs...\nDone!\n\nResult:\nNo miners found."
        event.app.layout.focus(results_panel)

    # Build layout
    root_container = HSplit([
        nc_menu(),
        body,
        nc_footer(),
    ])

    layout = Layout(root_container, focused_element=file_panel)

    app = Application(
        layout=layout,
        key_bindings=kb,
        style=NC_STYLE,
        full_screen=True,
        mouse_support=True,
    )

    app.run()

if __name__ == "__main__":
    main()