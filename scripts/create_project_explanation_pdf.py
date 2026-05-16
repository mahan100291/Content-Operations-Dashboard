from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs"
PDF_PATH = OUT_DIR / "content-operations-dashboard-explanation.pdf"


class RouteFlow(Flowable):
    def __init__(self) -> None:
        super().__init__()
        self.width = 6.4 * inch
        self.height = 1.45 * inch

    def draw(self) -> None:
        canvas = self.canv
        box_w = 1.72 * inch
        box_h = 0.56 * inch
        y = 0.55 * inch
        xs = [0.0, 2.33 * inch, 4.66 * inch]
        labels = [
            "/go/team-growth",
            "middleware.ts",
            "/?workspace=team-growth",
        ]
        fills = [colors.HexColor("#F7F4ED"), colors.HexColor("#E8EEF5"), colors.HexColor("#FFF7E6")]

        canvas.setStrokeColor(colors.HexColor("#2C5C63"))
        canvas.setLineWidth(1.2)

        for x, label, fill in zip(xs, labels, fills):
            canvas.setFillColor(fill)
            canvas.roundRect(x, y, box_w, box_h, 6, stroke=1, fill=1)
            canvas.setFillColor(colors.HexColor("#1E2A2F"))
            canvas.setFont("Helvetica-Bold", 8.6)
            canvas.drawCentredString(x + box_w / 2, y + 0.32 * inch, label)

        canvas.setStrokeColor(colors.HexColor("#D8664A"))
        canvas.setLineWidth(1.5)
        for start_x in [xs[0] + box_w, xs[1] + box_w]:
            end_x = start_x + 0.55 * inch
            canvas.line(start_x + 0.1 * inch, y + box_h / 2, end_x, y + box_h / 2)
            canvas.line(end_x, y + box_h / 2, end_x - 0.08 * inch, y + box_h / 2 + 0.06 * inch)
            canvas.line(end_x, y + box_h / 2, end_x - 0.08 * inch, y + box_h / 2 - 0.06 * inch)

        canvas.setFillColor(colors.HexColor("#607078"))
        canvas.setFont("Helvetica", 8)
        canvas.drawString(0, 0.2 * inch, "The browser URL stays friendly while Next middleware maps it to the dashboard route.")


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#1E2A2F"),
            spaceAfter=8,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=15,
            textColor=colors.HexColor("#607078"),
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=colors.HexColor("#2C5C63"),
            spaceBefore=12,
            spaceAfter=7,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#1F4D78"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.7,
            leading=14,
            textColor=colors.HexColor("#1E2A2F"),
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=12,
            textColor=colors.HexColor("#607078"),
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["BodyText"],
            fontName="Courier",
            fontSize=8.5,
            leading=11.5,
            backColor=colors.HexColor("#F2F4F7"),
            borderColor=colors.HexColor("#DADCE0"),
            borderWidth=0.5,
            borderPadding=6,
            spaceBefore=3,
            spaceAfter=8,
        ),
        "center": ParagraphStyle(
            "Center",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#607078"),
        ),
        "table": ParagraphStyle(
            "TableText",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=11.2,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1E2A2F"),
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10.5,
            textColor=colors.HexColor("#1E2A2F"),
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def bullets(items: list[str], style: ParagraphStyle) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, style), leftIndent=14) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=6,
    )


def table(rows: list[list[str]], widths: list[float], styles: dict[str, ParagraphStyle]) -> Table:
    wrapped = []
    for row_index, row in enumerate(rows):
        row_style = styles["table_header"] if row_index == 0 else styles["table"]
        wrapped.append([p(cell, row_style) for cell in row])

    t = Table(wrapped, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1E2A2F")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#DADCE0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def footer(canvas, doc) -> None:  # type: ignore[no-untyped-def]
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#607078"))
    canvas.drawString(doc.leftMargin, 0.45 * inch, "Content Operations Dashboard Explanation")
    canvas.drawRightString(LETTER[0] - doc.rightMargin, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    styles = build_styles()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=LETTER,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.72 * inch,
        bottomMargin=0.72 * inch,
        title="Content Operations Dashboard Explanation",
        author="Codex",
    )

    story = [
        p("Content Operations Dashboard Explanation", styles["title"]),
        p(
            "A detailed guide to the local Next.js mini project in "
            "<font name='Courier'>C:\\Users\\Mahan Chaturvedi\\OneDrive\\Documents\\react-project</font>.",
            styles["subtitle"],
        ),
        p("1. Project Purpose", styles["h1"]),
        p(
            "This mini project is a compact content management and social publishing dashboard. "
            "It demonstrates a practical Pages Router application while showing the migration target for routing "
            "logic: native Next.js middleware instead of a custom Express server.",
            styles["body"],
        ),
        bullets(
            [
                "Use Next.js 15+, React, and TypeScript as the application foundation.",
                "Keep routing in the Pages Router to match the current architecture.",
                "Move route middleware concerns into <font name='Courier'>middleware.ts</font>.",
                "Use CSS Modules for scoped styling.",
                "Use Motion for polished interface animation.",
                "Use Radix UI and Base UI for accessible headless components.",
                "Use Recharts to visualize publishing metrics.",
            ],
            styles["body"],
        ),
        p("2. Technology Stack", styles["h1"]),
        table(
            [
                ["Area", "Library / Tool", "How it is used"],
                ["Framework", "Next.js 15+", "Runs the React app, Pages Router routes, API route, and middleware."],
                ["Language", "TypeScript", "Adds type safety for components, data models, config, and API handlers."],
                ["UI primitives", "Radix UI Tabs", "Provides accessible tab behavior for dashboard sections."],
                ["Headless components", "Base UI Popover", "Provides accessible popover behavior without prescribing styles."],
                ["Animation", "Motion", "Animates the hero and workflow cards."],
                ["Charts", "Recharts", "Renders the scheduled-vs-published bar chart."],
                ["Styling", "CSS Modules", "Scopes page styles to avoid global class-name collisions."],
            ],
            [1.25 * inch, 1.45 * inch, 3.8 * inch],
            styles,
        ),
        p("3. File Map", styles["h1"]),
        table(
            [
                ["File / Folder", "Purpose"],
                ["package.json", "Defines scripts and dependencies for Next.js, React, UI libraries, charts, linting, and TypeScript."],
                ["pages/index.tsx", "Main dashboard page. It renders the hero, metrics, tabs, chart, workflow cards, and routing popover."],
                ["pages/_app.tsx", "Imports global CSS and renders every Pages Router page."],
                ["pages/api/metrics.ts", "API route that returns the sample channel and workflow metrics as JSON."],
                ["middleware.ts", "Native Next.js middleware that handles /go/:workspace and workspace headers."],
                ["data/contentMetrics.ts", "Shared sample data and TypeScript types for channel metrics and workflow stages."],
                ["styles/globals.css", "Global reset, color tokens, font stack, and Base UI portal stacking setup."],
                ["styles/Home.module.css", "Scoped dashboard layout and responsive visual styling."],
                ["next.config.ts", "Small Next.js configuration with React strict mode enabled."],
                ["tsconfig.json", "TypeScript compiler options and @/* import alias setup."],
                ["eslint.config.mjs", "ESLint flat config for Next.js Core Web Vitals and TypeScript rules."],
            ],
            [1.75 * inch, 4.75 * inch],
            styles,
        ),
        PageBreak(),
        p("4. Routing Architecture", styles["h1"]),
        p(
            "The application currently uses the Pages Router. The route structure is simple: "
            "<font name='Courier'>pages/index.tsx</font> maps to the homepage, and "
            "<font name='Courier'>pages/api/metrics.ts</font> maps to an API endpoint.",
            styles["body"],
        ),
        p("Pages Router routes", styles["h2"]),
        p(
            "/                       -> pages/index.tsx<br/>"
            "/api/metrics             -> pages/api/metrics.ts<br/>"
            "/go/team-growth          -> handled by middleware.ts, then rewritten to /?workspace=team-growth",
            styles["code"],
        ),
        p("Middleware flow", styles["h2"]),
        RouteFlow(),
        p(
            "The old Express idea was a custom server route like "
            "<font name='Courier'>/go/:workspace</font>. That has now been replaced with native Next.js middleware. "
            "When someone visits <font name='Courier'>/go/team-growth</font>, middleware extracts "
            "<font name='Courier'>team-growth</font>, rewrites the request to the dashboard route, and adds "
            "the workspace value as a query parameter.",
            styles["body"],
        ),
        p("Core middleware behavior", styles["h2"]),
        p(
            "1. Match paths for <font name='Courier'>/</font> and "
            "<font name='Courier'>/go/:workspace</font>.<br/>"
            "2. If the URL is <font name='Courier'>/go/:workspace</font>, clone the request URL.<br/>"
            "3. Change the pathname to <font name='Courier'>/</font>.<br/>"
            "4. Set <font name='Courier'>workspace</font> in the query string.<br/>"
            "5. Rewrite the request with <font name='Courier'>NextResponse.rewrite</font>.<br/>"
            "6. Add an <font name='Courier'>x-content-workspace</font> response header.",
            styles["body"],
        ),
        p("5. Main Dashboard Page", styles["h1"]),
        p(
            "The dashboard in <font name='Courier'>pages/index.tsx</font> is intentionally small but complete. "
            "It demonstrates how real product surfaces are assembled from data, UI primitives, animation, and charts.",
            styles["body"],
        ),
        table(
            [
                ["Section", "What it demonstrates"],
                ["Hero", "Product-style page heading, short explanation, and Motion entrance animation."],
                ["Summary metrics", "Derived values calculated from shared data in contentMetrics.ts."],
                ["Overview tab", "Recharts bar chart comparing scheduled and published content."],
                ["Workflow tab", "Motion-animated cards showing review, scheduling, and approval counts."],
                ["Routing tab", "Base UI Popover explaining how the middleware route behaves."],
            ],
            [1.55 * inch, 4.95 * inch],
            styles,
        ),
        p("6. Data Model", styles["h1"]),
        p(
            "The sample data lives in <font name='Courier'>data/contentMetrics.ts</font>. "
            "The <font name='Courier'>ChannelMetric</font> type describes each social channel, and the exported arrays "
            "are reused by both the page and API route.",
            styles["body"],
        ),
        p(
            "type ChannelMetric = {<br/>"
            "&nbsp;&nbsp;channel: string;<br/>"
            "&nbsp;&nbsp;scheduled: number;<br/>"
            "&nbsp;&nbsp;published: number;<br/>"
            "&nbsp;&nbsp;engagement: number;<br/>"
            "};",
            styles["code"],
        ),
        p(
            "This keeps the mini project easy to understand: there is one source of truth for the dashboard data, "
            "and the API route simply exposes that same data as JSON.",
            styles["body"],
        ),
        p("7. Styling and Design", styles["h1"]),
        bullets(
            [
                "<font name='Courier'>globals.css</font> defines global design tokens like background, ink, muted text, teal, gold, and coral.",
                "<font name='Courier'>Home.module.css</font> owns the dashboard layout, card styling, tabs, chart frame, popover, and mobile breakpoints.",
                "CSS Modules keep styles local to the page component, which is useful in a growing Pages Router codebase.",
                "Base UI portal guidance is represented by isolating the Next root, so popovers layer predictably above page content.",
            ],
            styles["body"],
        ),
        PageBreak(),
        p("8. Accessibility Notes", styles["h1"]),
        p(
            "Radix UI and Base UI are used because they provide accessible behavior while letting the project keep its own visual design. "
            "The dashboard uses semantic headings, button-based tab triggers, an aria-label for the tab list, and headless popover behavior.",
            styles["body"],
        ),
        table(
            [
                ["Component", "Accessibility benefit"],
                ["Radix Tabs", "Keyboard-friendly tab navigation and proper tab state management."],
                ["Base UI Popover", "Accessible trigger and popup behavior without custom focus logic."],
                ["Semantic HTML", "Sections, headings, articles, and main landmarks improve screen-reader structure."],
                ["Responsive CSS", "Tabs and layout collapse cleanly on narrower screens."],
            ],
            [1.55 * inch, 4.95 * inch],
            styles,
        ),
        p("9. How to Run the Project", styles["h1"]),
        p(
            "Open a terminal at the project folder:",
            styles["body"],
        ),
        p("C:\\Users\\Mahan Chaturvedi\\OneDrive\\Documents\\react-project", styles["code"]),
        p("Install dependencies and start the dev server:", styles["body"]),
        p("npm install<br/>npm run dev", styles["code"]),
        p(
            "Then open <font name='Courier'>http://localhost:3000</font>. "
            "To test the middleware route, open <font name='Courier'>http://localhost:3000/go/team-growth</font>.",
            styles["body"],
        ),
        p("10. What to Explain in an Interview or Review", styles["h1"]),
        bullets(
            [
                "The project mirrors a realistic migration path: keep Pages Router pages while moving route middleware out of Express.",
                "The middleware rewrite preserves a friendly URL pattern while rendering the existing dashboard page.",
                "Data is centralized in a typed module and reused by both the UI and API route.",
                "UI behavior comes from accessible primitives instead of hand-rolled tab or popover logic.",
                "Charts are dynamically imported because browser-oriented chart libraries are safer when rendered client-side.",
                "CSS Modules keep the styling approach close to the existing stack and avoid global leakage.",
            ],
            styles["body"],
        ),
        p("11. Suggested Next Improvements", styles["h1"]),
        table(
            [
                ["Improvement", "Why it matters"],
                ["Read workspace query in UI", "Display the active workspace name when visiting /go/:workspace."],
                ["Add tests", "Use unit tests for middleware matching and component tests for tabs/popover behavior."],
                ["Fetch API metrics", "Move the dashboard from imported data to client/server fetching through /api/metrics."],
                ["Add App Router route", "Create an app/ version of the page as a migration exercise."],
                ["Persist data", "Replace sample data with a small database or JSON-backed service."],
            ],
            [1.9 * inch, 4.6 * inch],
            styles,
        ),
        Spacer(1, 0.12 * inch),
        KeepTogether(
            [
                p("Summary", styles["h1"]),
                p(
                    "This project is small on purpose, but it touches the important parts of the requested stack: "
                    "Next.js Pages Router, native middleware, TypeScript data modeling, accessible component primitives, "
                    "CSS Modules, Motion animations, and Recharts visualization.",
                    styles["body"],
                ),
            ]
        ),
    ]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build_pdf()
    print(PDF_PATH)
