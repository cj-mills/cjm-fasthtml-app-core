"""Demo application for cjm-fasthtml-app-core library.

This demo showcases all the core utilities:
- AppHtmlIds for centralized ID management
- Alert components (success, error, warning, info)
- HTMX request handling utilities
- Page layout wrapper
- Responsive navbar component
"""

from pathlib import Path
from fasthtml.common import *
from cjm_fasthtml_daisyui.core.resources import get_daisyui_headers
from cjm_fasthtml_daisyui.core.testing import create_theme_persistence_script

print("\n" + "="*70)
print("Initializing cjm-fasthtml-app-core Demo")
print("="*70)

# Import all the library components
from cjm_fasthtml_app_core.core.html_ids import AppHtmlIds
from cjm_fasthtml_app_core.components.alerts import (
    create_success_alert,
    create_error_alert,
    create_warning_alert,
    create_info_alert
)
from cjm_fasthtml_app_core.core.htmx import handle_htmx_request, is_htmx_request
from cjm_fasthtml_app_core.core.layout import wrap_with_layout
from cjm_fasthtml_app_core.components.navbar import create_navbar, create_nav_link

# Import utilities for styling
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
from cjm_fasthtml_tailwind.core.base import combine_classes
from cjm_fasthtml_daisyui.components.actions.button import btn, btn_colors, btn_sizes
from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors

print("✓ All library components imported successfully")

# Create the FastHTML app at module level
app, rt = fast_app(
    pico=False,
    hdrs=[
        *get_daisyui_headers(),
        create_theme_persistence_script(),
    ],
    title="FastHTML App Core Demo",
    htmlkw={'data-theme': 'light'}
)

# Define routes at module level
@rt
def index(request):
    """Homepage with feature showcase."""

    def home_content():
        return Div(
            H1("cjm-fasthtml-app-core Demo",
               cls=combine_classes(font_size._4xl, font_weight.bold, m.b(4))),

            P("A library of reusable FastHTML application utilities:",
              cls=combine_classes(font_size.lg, m.b(6))),

            # Feature list
            Div(
                Div(
                    Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                    Span("Centralized HTML ID management with IDE autocomplete"),
                    cls=combine_classes(m.b(3))
                ),
                Div(
                    Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                    Span("DaisyUI alert components (success, error, warning, info)"),
                    cls=combine_classes(m.b(3))
                ),
                Div(
                    Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                    Span("HTMX request handling utilities"),
                    cls=combine_classes(m.b(3))
                ),
                Div(
                    Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                    Span("Flexible page layout wrapper"),
                    cls=combine_classes(m.b(3))
                ),
                Div(
                    Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                    Span("Responsive navbar with mobile support"),
                    cls=combine_classes(m.b(8))
                ),
                cls=combine_classes(text_align.left, m.b(8))
            ),

            # Navigation
            Div(
                A(
                    "View Alerts Demo",
                    href=alerts.to(),
                    hx_get=alerts.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.primary, btn_sizes.lg, m.r(2))
                ),
                A(
                    "View Features",
                    href=features.to(),
                    hx_get=features.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(btn, btn_colors.secondary, btn_sizes.lg)
                ),
            ),

            cls=combine_classes(
                container,
                max_w._4xl,
                m.x.auto,
                p(8),
                text_align.center
            )
        )

    # Use handle_htmx_request to return appropriate response
    return handle_htmx_request(
        request,
        home_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

@rt
def alerts(request):
    """Page demonstrating all alert types."""

    def alerts_content():
        return Div(
            H1("Alert Components",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(6))),

            P("Examples of all available alert types:",
              cls=combine_classes(font_size.lg, m.b(8))),

            # Success alert
            H2("Success Alert", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
            create_success_alert("Operation completed successfully!"),

            # Error alert
            H2("Error Alert", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3), m.t(6))),
            create_error_alert("An error occurred", "Please check your input and try again"),

            # Warning alert
            H2("Warning Alert", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3), m.t(6))),
            create_warning_alert("Proceeding may cause issues", "Consider reviewing your changes"),

            # Info alert
            H2("Info Alert", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3), m.t(6))),
            create_info_alert("New features available", "Check out the updated documentation"),

            cls=combine_classes(
                container,
                max_w._4xl,
                m.x.auto,
                p(8)
            )
        )

    return handle_htmx_request(
        request,
        alerts_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

@rt
def features(request):
    """Page listing all library features."""

    def features_content():
        return Div(
            H1("Library Features",
               cls=combine_classes(font_size._3xl, font_weight.bold, m.b(6))),

            # HTML IDs
            Div(
                H2("AppHtmlIds", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Centralized HTML ID management with type safety:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(f"MAIN_CONTENT = '{AppHtmlIds.MAIN_CONTENT}'"),
                    Li(f"ALERT_CONTAINER = '{AppHtmlIds.ALERT_CONTAINER}'"),
                    Li(Code("as_selector()"), " helper for CSS selectors"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # Alert Components
            Div(
                H2("Alert Components", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Four alert types with auto-dismiss and optional details:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(Code("create_success_alert()"), " - Success messages"),
                    Li(Code("create_error_alert()"), " - Error messages with details"),
                    Li(Code("create_warning_alert()"), " - Warning messages"),
                    Li(Code("create_info_alert()"), " - Informational messages"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # HTMX Utilities
            Div(
                H2("HTMX Utilities", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Helpers for HTMX-powered SPAs:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(Code("is_htmx_request()"), " - Detect HTMX requests"),
                    Li(Code("handle_htmx_request()"), " - Route handler pattern"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # Layout
            Div(
                H2("Layout Wrapper", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Consistent page structure:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(Code("wrap_with_layout()"), " - Wrap content with navbar/footer"),
                    Li("Configurable container ID and tag"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # Navbar
            Div(
                H2("Navbar Component", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Responsive navigation bar:",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(Code("create_navbar()"), " - Full navbar with mobile support"),
                    Li(Code("create_nav_link()"), " - HTMX navigation links"),
                    Li("Optional theme selector integration"),
                    Li("Mobile dropdown menu"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            cls=combine_classes(
                container,
                max_w._4xl,
                m.x.auto,
                p(8)
            )
        )

    return handle_htmx_request(
        request,
        features_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar)
    )

# Create navbar at module level (after route definitions so it can reference them)
navbar = create_navbar(
    title="App Core Demo",
    nav_items=[
        ("Home", index),
        ("Alerts", alerts),
        ("Features", features)
    ],
    home_route=index,
    theme_selector=True
)

print("\n" + "="*70)
print("Demo App Ready!")
print("="*70)
print("\n📦 Library Components:")
print("  • AppHtmlIds - Centralized ID management")
print("  • Alert components - Success, error, warning, info")
print("  • HTMX utilities - Request handling helpers")
print("  • Layout wrapper - Consistent page structure")
print("  • Navbar component - Responsive navigation")
print("="*70 + "\n")


if __name__ == "__main__":
    import uvicorn
    import webbrowser
    import threading

    def open_browser(url):
        print(f"🌐 Opening browser at {url}")
        webbrowser.open(url)

    port = 5020
    host = "0.0.0.0"
    display_host = 'localhost' if host in ['0.0.0.0', '127.0.0.1'] else host

    print(f"🚀 Server: http://{display_host}:{port}")
    print("\n📍 Available routes:")
    print(f"  http://{display_host}:{port}/          - Homepage")
    print(f"  http://{display_host}:{port}/alerts    - Alert demos")
    print(f"  http://{display_host}:{port}/features  - Feature list")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
