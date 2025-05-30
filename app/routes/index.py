from fasthtml.common import Button, Div, Form, Input, Span, Titled
from fasthtml.svg import Circle, Svg

from app.utils import lay_brick, get_index_data


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
                # Grid head node
                Div(id="grid-head-node", style="display: none"),
                # Grid body nodes loaded from index.json
                *[lay_brick(data["url"], data["filename"]) for data in get_index_data()],
                cls="grid",
            ),
        ),
    )
