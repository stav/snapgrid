from fasthtml.common import Button, Div, Form, H3, Input, P, Span, Titled
from fasthtml.svg import Circle, Svg


def index_route():
    return Titled(
        "SnapGrid",
        Div(
            Form(
                Input(
                    type="text",
                    name="url",
                    required=True,
                    placeholder="Enter URL",
                    style="padding: 8px",
                ),
                Button(
                    "Snap",
                    Span(
                        Svg(
                            Circle(
                                cx=25,
                                cy=25,
                                r="20",
                                cls="path",
                                fill="none",
                                stroke_width="5",
                            ),
                            cls="spinner-svg",
                            viewBox="0 0 50 50",
                        ),
                        id="spinner",
                        cls="spinner",
                    ),
                    type="submit",
                    style="position: relative; padding: 8px 16px;",
                ),
                hx_post="/snap",
                hx_swap="afterend",
                hx_target="#grid-head-node",
                hx_indicator="#spinner",
                hx_on__before_request="this.disabled = true",
                hx_on__after_request="this.disabled = false",
            ),
            Div(  # Grid for the blocks
                Div(id="grid-head-node", style="display: none"),
                cls="grid",
            ),
        ),
        Div(
            H3("Custom Modal"),
            P("Img: ${fancyboxDialog.querySelector('img').src}"),
            P("Markdown: ${fancyboxDialog.querySelector('.markdown-text')}", id="markdown-text"),
            Button("CloseME!", onclick="this.parentElement.style.display = 'none'"),
            id="markdown-dialog",
            style="display: none",
        ),
    )
