from dash import Dash, Input, Output, dcc, html
import pandas as pd
import plotly.express as px


DATA_FILE = "task2-3output.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")
REGION_OPTIONS = ["all", "north", "east", "south", "west"]


def load_sales_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["region"] = df["region"].astype(str).str.strip().str.lower()
    df = df.dropna(subset=["sales", "date", "region"])
    return df


def filter_and_aggregate(df: pd.DataFrame, selected_region: str) -> pd.DataFrame:
    if selected_region != "all":
        df = df[df["region"] == selected_region]

    sales_by_date = df.groupby("date", as_index=False)["sales"].sum()
    sales_by_date = sales_by_date.sort_values("date")
    return sales_by_date


def build_figure(sales_by_date: pd.DataFrame, selected_region: str):
    region_title = "All Regions" if selected_region == "all" else selected_region.title()

    fig = px.line(
        sales_by_date,
        x="date",
        y="sales",
        markers=True,
        title=f"Pink Morsel Sales Over Time - {region_title}",
        labels={"date": "Date", "sales": "Sales"},
    )

    fig.update_traces(line=dict(color="#0b6e4f", width=4), marker=dict(size=7))
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="#fcfaf3",
        title_font=dict(size=22, family="Space Grotesk"),
        font=dict(family="Space Grotesk", size=14, color="#1d2d2a"),
        margin=dict(l=30, r=30, t=80, b=30),
        xaxis=dict(showgrid=True, gridcolor="#e8e2d5"),
        yaxis=dict(showgrid=True, gridcolor="#e8e2d5"),
    )

    fig.add_shape(
        type="line",
        x0=PRICE_INCREASE_DATE,
        x1=PRICE_INCREASE_DATE,
        y0=0,
        y1=1,
        xref="x",
        yref="paper",
        line=dict(color="#b22222", dash="dash", width=2),
    )
    fig.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        xref="x",
        yref="paper",
        text="Price increase: 15 Jan 2021",
        showarrow=False,
        bgcolor="#fff4e6",
        bordercolor="#b22222",
        borderwidth=1,
        yshift=-12,
        xshift=8,
    )

    return fig


app = Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap"
    ],
)

raw_sales_data = load_sales_data(DATA_FILE)
initial_chart_data = filter_and_aggregate(raw_sales_data, "all")

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "padding": "32px 20px",
        "background": "linear-gradient(140deg, #f6efe0 0%, #f3f7e9 45%, #d9efe5 100%)",
        "fontFamily": "Space Grotesk, sans-serif",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1050px",
                "margin": "0 auto",
                "background": "rgba(255, 255, 255, 0.88)",
                "backdropFilter": "blur(3px)",
                "padding": "28px",
                "borderRadius": "18px",
                "boxShadow": "0 14px 45px rgba(11, 110, 79, 0.16)",
                "border": "1px solid #d9e6dc",
            },
            children=[
                html.H1(
                    "Soul Foods Pink Morsel Sales Explorer",
                    style={
                        "margin": "0 0 10px",
                        "fontSize": "2.1rem",
                        "color": "#153d35",
                        "letterSpacing": "0.3px",
                    },
                ),
                html.P(
                    "Compare sales before and after the 15 Jan 2021 price increase by region.",
                    style={"margin": "0 0 22px", "fontSize": "1rem", "color": "#31554d"},
                ),
                html.Div(
                    style={
                        "padding": "14px 16px",
                        "borderRadius": "12px",
                        "background": "#f7f4ec",
                        "border": "1px solid #e8ddc8",
                        "marginBottom": "18px",
                    },
                    children=[
                        html.Label(
                            "Filter By Region",
                            style={
                                "display": "block",
                                "fontWeight": "700",
                                "marginBottom": "10px",
                                "color": "#20453d",
                            },
                        ),
                        dcc.RadioItems(
                            id="region-filter",
                            options=[
                                {"label": region.title(), "value": region}
                                for region in REGION_OPTIONS
                            ],
                            value="all",
                            inline=True,
                            labelStyle={
                                "marginRight": "16px",
                                "padding": "6px 10px",
                                "borderRadius": "999px",
                                "backgroundColor": "#ffffff",
                                "border": "1px solid #c8d9d0",
                                "cursor": "pointer",
                            },
                            inputStyle={"marginRight": "6px"},
                        ),
                    ],
                ),
                dcc.Graph(
                    id="sales-line-chart",
                    figure=build_figure(initial_chart_data, "all"),
                    style={"height": "70vh", "minHeight": "420px"},
                ),
            ],
        )
    ],
)


@app.callback(Output("sales-line-chart", "figure"), Input("region-filter", "value"))
def update_sales_chart(selected_region: str):
    chart_data = filter_and_aggregate(raw_sales_data, selected_region)
    return build_figure(chart_data, selected_region)


if __name__ == "__main__":
    app.run(debug=True)
