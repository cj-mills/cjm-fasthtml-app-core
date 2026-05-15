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
from cjm_fasthtml_app_core.components.empty_state import render_empty_state
from cjm_fasthtml_app_core.core.htmx import handle_htmx_request, is_htmx_request
from cjm_fasthtml_app_core.core.layout import wrap_with_layout
from cjm_fasthtml_app_core.components.navbar import create_navbar

# Import utilities for styling
from cjm_fasthtml_tailwind.utilities.spacing import p, m
from cjm_fasthtml_tailwind.utilities.sizing import container, max_w, h
from cjm_fasthtml_tailwind.utilities.typography import font_size, font_weight, text_align
from cjm_fasthtml_tailwind.utilities.flexbox_and_grid import flex_display, flex_direction, items, gap
from cjm_fasthtml_tailwind.core.base import combine_classes
from cjm_fasthtml_daisyui.components.actions.button import btn, btn_colors, btn_sizes
from cjm_fasthtml_daisyui.components.data_display.badge import badge, badge_colors
from cjm_fasthtml_daisyui.components.feedback.alert import alert, alert_colors

# Design system: V1 button roles, V11 icon-size roles, V10 panel roles
from cjm_fasthtml_design_system.buttons import buttons
from cjm_fasthtml_design_system.icons import icons
from cjm_fasthtml_design_system.panels import panels
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
                    cls=combine_classes(m.b(3))
                ),
                Div(
                    Span("✓", cls=combine_classes(font_size._2xl, m.r(3))),
                    Span("Empty-state component (V8)"),
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
                    cls=combine_classes(buttons.page_primary, m.r(2))
                ),
                A(
                    "View Empty State Demo",
                    href=empty_states.to(),
                    hx_get=empty_states.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=combine_classes(buttons.page_primary, m.r(2))
                ),
                A(
                    "View Features",
                    href=features.to(),
                    hx_get=features.to(),
                    hx_target=f"#{AppHtmlIds.MAIN_CONTENT}",
                    hx_push_url="true",
                    cls=buttons.page_primary
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
def empty_states(request):
    """Page demonstrating render_empty_state (V8 anatomy composition helper).

    Renders the canonical empty-state variants (full, minimal, title+detail no icon,
    title+CTA no icon) plus in-context demos against both V10 panel backgrounds
    (base_200 minimal_container, base_100 content_card inside a base_200 viewport)
    so cross-theme tours can verify legibility on both surfaces.
    """

    def empty_states_content():
        # Bound the wrapper's grow() with a flex-column parent at a fixed height so
        # the wrapper's vertical-fill behavior is visually demonstrable. The flex
        # parent context is necessary because empty_states.wrapper composes grow(),
        # which requires a flex container with bounded cross-axis to fill.
        bounded_parent_cls = combine_classes(
            h(96), panels.minimal_container,
            flex_display, flex_direction.col,
        )
        compact_bounded_parent_cls = combine_classes(
            h(48), panels.minimal_container,
            flex_display, flex_direction.col,
        )
        med_bounded_parent_cls = combine_classes(
            h(64), panels.minimal_container,
            flex_display, flex_direction.col,
        )

        return Div(
            H1(
                "Empty State (V8)",
                cls=combine_classes(font_size._3xl, font_weight.bold, m.b(2)),
            ),
            P(
                "render_empty_state composes V8 anatomy slots (wrapper / icon / "
                "title / detail) into a Div with canonical child ordering (icon → "
                "title → detail → CTA). All slots are optional except message. "
                "Codifies V8 (Empty-state anatomy) per the V12 convention/implementation "
                "split — anatomy in design-system, rendering helper here.",
                cls=combine_classes(font_size.lg, m.b(6)),
            ),

            # Canonical full composition ───────────────────────────────────
            H2(
                "Canonical full composition (icon + title + detail + CTA)",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            P(
                "All four V8 slots plus an optional V1 CTA. The wrapper's grow() "
                "fills the bounded flex parent; the parent's height determines the "
                "fill region.",
                cls=combine_classes(m.b(4)),
            ),
            Div(
                render_empty_state(
                    message="No transcription sources selected",
                    detail="Add a source from the browser to begin.",
                    icon_name="inbox",
                    cta=Button("Add a source", cls=buttons.primary_action),
                ),
                cls=combine_classes(bounded_parent_cls, m.b(8)),
            ),

            # Minimal — title only ─────────────────────────────────────────
            H2(
                "Minimal — title only",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            P(
                "The simplest empty state: just the title slot inside the wrapper. "
                "Used when context is self-evident or vertical space is constrained.",
                cls=combine_classes(m.b(4)),
            ),
            Div(
                render_empty_state(message="No items available"),
                cls=combine_classes(compact_bounded_parent_cls, m.b(8)),
            ),

            # Title + detail (no icon) ─────────────────────────────────────
            H2(
                "Title + detail (no icon)",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            P(
                "Drops the icon slot when iconography would add visual weight "
                "without informational gain. Common shape for management-page "
                "empty lists where the surrounding chrome already conveys context.",
                cls=combine_classes(m.b(4)),
            ),
            Div(
                render_empty_state(
                    message="No graphs committed yet",
                    detail="Complete a workflow to commit a graph.",
                ),
                cls=combine_classes(med_bounded_parent_cls, m.b(8)),
            ),

            # With CTA only (no detail, no icon) ───────────────────────────
            H2(
                "Title + CTA only (no detail, no icon)",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            P(
                "Drops detail when the title carries enough context and the CTA "
                "verb is self-explanatory. Tight three-line shape (title + spacing "
                "+ CTA).",
                cls=combine_classes(m.b(4)),
            ),
            Div(
                render_empty_state(
                    message="No documents yet",
                    cta=Button("Start a workflow", cls=buttons.primary_action),
                ),
                cls=combine_classes(med_bounded_parent_cls, m.b(8)),
            ),

            # In-context: base_200 background ──────────────────────────────
            H2(
                "In-context: base_200 (panels.minimal_container)",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            P(
                "Canonical empty state rendered directly inside a base_200 panel. "
                "Tour across silk / cyberpunk / abyss / retro to verify icon and "
                "text legibility against each theme's base_200 fill.",
                cls=combine_classes(m.b(4)),
            ),
            Div(
                render_empty_state(
                    message="No transcription sources selected",
                    detail="Add a source from the browser to begin.",
                    icon_name="inbox",
                ),
                cls=combine_classes(
                    h(80), p(4), panels.minimal_container,
                    flex_display, flex_direction.col, m.b(8),
                ),
            ),

            # In-context: base_100 inside base_200 ─────────────────────────
            H2(
                "In-context: base_100 (panels.content_card inside base_200)",
                cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3)),
            ),
            P(
                "Canonical empty state rendered inside a base_100 content_card, "
                "which is itself rendered inside a base_200 viewport. This mirrors "
                "the canonical card-stack focus-slot empty-state composition.",
                cls=combine_classes(m.b(4)),
            ),
            Div(
                Div(
                    render_empty_state(
                        message="No transcription sources selected",
                        detail="Add a source from the browser to begin.",
                        icon_name="inbox",
                    ),
                    cls=combine_classes(
                        h(80), p(4), panels.content_card,
                        flex_display, flex_direction.col,
                    ),
                ),
                cls=combine_classes(p(3), panels.minimal_container, m.b(6)),
            ),

            cls=combine_classes(container, max_w._4xl, m.x.auto, p(8)),
        )

    return handle_htmx_request(
        request,
        empty_states_content,
        wrap_fn=lambda content: wrap_with_layout(content, navbar=navbar),
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

            # Empty State (V8)
            Div(
                H2("Empty State (V8)", cls=combine_classes(font_size._2xl, font_weight.bold, m.b(3))),
                P("Generic empty-state component — centered icon-above-title-above-detail "
                  "composition with optional CTA. Codifies V8 (Empty-state anatomy) per the "
                  "V12 convention/implementation split (anatomy in design-system, rendering "
                  "helper here).",
                  cls=combine_classes(m.b(2))),
                Ul(
                    Li(Code("render_empty_state()"), " - Icon + title + detail + CTA composition"),
                    Li("All slots optional except ", Code("message"), " (title text)"),
                    Li("Canonical child ordering: icon → title → detail → CTA"),
                    Li("Composes V8 ", Code("empty_states"), " anatomy slots + V11 ",
                       Code("icons.empty_state"), " size + V13 text tiers"),
                    Li(Code("cta"), " accepts any FT (Button, A, Div), not just Button"),
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
        ("Empty States", empty_states),
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
print("  • Empty state (V8) - Generic empty-state composition helper")
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
    print(f"  http://{display_host}:{port}/               - Homepage")
    print(f"  http://{display_host}:{port}/confirms       - Confirm modal (V12) demo")
    print(f"  http://{display_host}:{port}/empty_states   - Empty state (V8) demo")
    print(f"  http://{display_host}:{port}/features       - Feature list")
    print("\n" + "="*70 + "\n")

    # Open browser after a short delay
    timer = threading.Timer(1.5, lambda: open_browser(f"http://localhost:{port}"))
    timer.daemon = True
    timer.start()

    # Start server
    uvicorn.run(app, host=host, port=port)
