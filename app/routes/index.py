from fasthtml.common import Button, Div, Form, Input, Span, Style, Titled
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
                    hx_post="/fetch",
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
            Style(
                """
                .grid {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                }

                .brick {
                    width: 300px;
                }

                .spinner {
                    visibility: hidden;
                    display: inline-block;
                    position: absolute;
                    top: 20%;
                    right: 30%;
                }

                .spinner.htmx-request  {
                    visibility: visible;
                }

                .spinner-svg {
                    animation: rotate 2s linear infinite;
                    width: 20px;
                    height: 20px;
                }

                .path {
                    stroke: white;
                    stroke-linecap: round;
                    animation: dash 1.5s ease-in-out infinite;
                }

                @keyframes rotate {
                    100% { transform: rotate(360deg); }
                }

                @keyframes dash {
                    0% { stroke-dasharray: 1, 150; stroke-dashoffset: 0; }
                    50% { stroke-dasharray: 90, 150; stroke-dashoffset: -35; }
                    100% { stroke-dasharray: 90, 150; stroke-dashoffset: -124; }
                }
                """
            ),
        ),
    )
