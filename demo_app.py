"""Demo application for cjm-fasthtml-app-core library.

This demo showcases all the core utilities:
- AppHtmlIds for centralized ID management
- HTMX request handling utilities
- Page layout wrapper
- Responsive navbar component
- Confirm modal (V12 destructive-confirm composition)
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
from cjm_fasthtml_app_core.components.confirm_modal import render_confirm_modal
from cjm_fasthtml_app_core.core.htmx import handle_htmx_request, is_htmx_request
from cjm_fasthtml_app_core.core.layout import wrap_with_layout
from cjm_fasthtml_app_core.components.navbar import create_navbar

# Import utilities for styling
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import flex_display, items, gap
from cjm_fasthtml_tailwind.core.base import combine_classes
from cjm_fasthtml_daisyui.components.actions.button import btn, btn_colors, btn_sizes
from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
from cjm_fasthtml_daisyui.components.feedback.alert import alert, alert_colors

# Design system: V1 button roles, V11 icon-size roles
from cjm_fasthtml_design_system.buttons import buttons
from cjm_fasthtml_design_system.icons import icons
from cjm_fasthtml_lucide_icons.factory import lucide_icon

print("✓ All library components imported successfully")

# Create the FastHTML app at module level
APP_ID = "appcore"

app, rt = fast_app(
    pico=False,
    hdrs=[
        *get_daisyui_headers(),
        create_theme_persistence_script(),
    ],
    title="FastHTML App Core Demo",
    htmlkw={'data-theme': 'light'},
    session_cookie=f'session_{APP_ID}_',
    secret_key=f'{APP_ID}-demo-secret',
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
                    cls=combine_classes(m.b(3))
                ),
                Div(
                    Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                    Span("Generic destructive-confirm modal (V12)"),
                    cls=combine_classes(m.b(8))
                ),
                cls=combine_classes(text_align.left, m.b(8))
            ),

            # Navigation
            Div(
                A(
                    "View Confirm Modal Demo",
                    href=confirms.to(),
                    hx_get=confirms.to(),
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
def confirms(request):
    """Page demonstrating the V12 destructive-confirm modal recipe."""

    def confirms_content():
        # Trigger button — V1 destructive_cancellable (outline error).
        # Opens the confirm modal via onclick.
        delete_trigger = Button(
            lucide_icon("trash-2", size=icons.text_button),
            "Delete Item",
            cls=combine_classes(
                buttons.destructive_cancellable,
                flex_display, items.center, gap(1),
            ),
            onclick=(
                "document.getElementById('demo-delete-body').innerHTML = "
                "'<p>Permanently delete <strong>Sample Item #42</strong>?</p>'"
                "+ '<p class=\"text-sm text-base-content/60 mt-2\">"
                "This action cannot be undone (demo only — nothing is actually deleted).</p>';"
                "document.getElementById('demo-delete-modal').showModal()"
            ),
        )

        # No-icon variant trigger
        discard_trigger = Button(
            "Discard Draft",
            cls=combine_classes(buttons.destructive_cancellable),
            onclick=(
                "document.getElementById('demo-discard-body').innerHTML = "
                "'<p>Discard your unsaved draft?</p>';"
                "document.getElementById('demo-discard-modal').showModal()"
            ),
        )

        # The two confirm modals
        delete_modal = render_confirm_modal(
            modal_id="demo-delete-modal",
            body_id="demo-delete-body",
            title="Delete Item?",
            confirm_label="Delete",
            confirm_icon="trash-2",
            confirm_attrs={
                "hx_post": confirms_action.to(),
                "hx_target": f"#confirm-status",
                "hx_swap": "outerHTML",
                "hx_vals": '{"action": "delete"}',
            },
        )

        discard_modal = render_confirm_modal(
            modal_id="demo-discard-modal",
            body_id="demo-discard-body",
            title="Discard Changes?",
            confirm_label="Discard",
            cancel_label="Keep Editing",
            confirm_attrs={
                "hx_post": confirms_action.to(),
                "hx_target": f"#confirm-status",
                "hx_swap": "outerHTML",
                "hx_vals": '{"action": "discard"}',
            },
        )

        return Div(
            H1(
                "Confirm Modal (V12)",
                cls=combine_classes(font_size._3xl, font_weight.bold, m.b(2)),
            ),
            P(
                "Destructive-confirm modal recipe — Cancel-on-LEFT, Confirm-on-RIGHT, "
                "backdrop click-to-dismiss, defensive type=\"button\", body via HTMX swap.",
                cls=combine_classes(font_size.lg, m.b(6)),
            ),

            # Trigger row
            H2(
                "Triggers (V1 destructive_cancellable)",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            P(
                "Each trigger button is a V1 destructive_cancellable role that opens its "
                "associated V12 confirm modal. Clicking Confirm fires an HTMX request to a "
                "demo endpoint; clicking Cancel or the backdrop dismisses natively via the "
                "HTML5 dialog element.",
                cls=combine_classes(m.b(4)),
            ),
            Div(
                delete_trigger,
                discard_trigger,
                cls=combine_classes(flex_display, gap(3), m.b(8)),
            ),

            # Confirm-action result lands here
            H2(
                "Result",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            Div(
                P(
                    "After clicking Confirm in either modal, the server response will "
                    "appear here.",
                    cls=combine_classes(font_size.sm, text_align.center),
                ),
                id="confirm-status",
                cls=combine_classes(p(4), m.b(6)),
            ),

            # Modals (rendered at end of page so the dialog elements are in DOM
            # but invisible until showModal() is called)
            delete_modal,
            discard_modal,

            cls=combine_classes(container, max_w._4xl, m.x.auto, p(8)),
        )

    return handle_htmx_request(
        request,
        confirms_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar),
    )


@rt
def confirms_action(request):
    """Demo handler for the confirm modal's HTMX action.

    Returns a small daisyui alert and a Script that closes whichever dialog was open.
    Real consumers would do real destructive work here.
    """
    return Div(
        Div(
            Span("Confirmed (demo) — modal flow worked end-to-end."),
            role="alert",
            cls=combine_classes(alert, alert_colors.success),
        ),
        # Closing a non-open dialog is a no-op, so calling close() on both is safe.
        Script(
            "document.getElementById('demo-delete-modal').close();"
            "document.getElementById('demo-discard-modal').close();"
        ),
        id="confirm-status",
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
                    Li(Code("as_selector()"), " helper for CSS selectors"),
                    cls=combine_classes(m.l(6), m.b(6))
                ),
            ),

            # Confirm Modal (V12)
            Div(
                H2("Confirm Modal (V12)", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Generic destructive-confirm modal — Cancel-on-LEFT, Confirm-on-RIGHT, "
                  "backdrop click-to-dismiss, defensive type=button. "
                  "Codifies V12 (Destructive-confirm composition).",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(Code("render_confirm_modal()"), " - Generic Cancel/Confirm dialog"),
                    Li("Body via HTMX swap into ", Code("body_id"), " — caller injects message text"),
                    Li("Optional Lucide icon prefix on the confirm button"),
                    Li("Composes V1 ", Code("buttons.destructive_confirm"), " + ",
                       Code("buttons.soft_dismissal")),
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
        ("Confirms", confirms),
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
print("  • Confirm modal (V12) - Generic destructive-confirm dialog")
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
    print(f"  http://{display_host}:{port}/confirms  - Confirm modal (V12) demo")
    print(f"  http://{display_host}:{port}/features  - Feature list")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
