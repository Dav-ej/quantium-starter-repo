import dash
from dash import Dash, dcc, html
import pandas as pd
import plotly.express as px

app = Dash()

DATA_FILE = "task2-3output.csv"
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")


def load_sales_data(file_path: str) -> pd.DataFrame:
	df = pd.read_csv(file_path)
	df["sales"] = df["sales"].astype(float)
	df["date"] = pd.to_datetime(df["date"])

	# Sum sales per day across all regions, then sort for a proper time-series line chart.
	sales_by_date = df.groupby("date", as_index=False)["sales"].sum()
	sales_by_date = sales_by_date.sort_values("date")
	return sales_by_date


def build_figure(sales_by_date: pd.DataFrame):
	fig = px.line(
		sales_by_date,
		x="date",
		y="sales",
		title="Pink Morsel Sales Over Time",
		labels={"date": "Date", "sales": "Sales (USD)"},
	)

	fig.add_shape(
		type="line",
		x0=PRICE_INCREASE_DATE,
		x1=PRICE_INCREASE_DATE,
		y0=0,
		y1=1,
		xref="x",
		yref="paper",
		line=dict(color="red", dash="dash"),
	)
	fig.add_annotation(
		x=PRICE_INCREASE_DATE,
		y=1,
		xref="x",
		yref="paper",
		text="Price increase (15 Jan 2021)",
		showarrow=False,
		yshift=-10,
		xshift=8,
	)
	return fig


sales_data = load_sales_data(DATA_FILE)
line_figure = build_figure(sales_data)

app = dash.Dash(__name__)

app.layout = html.Div(
	children=[
		html.H1("Soul Foods Pink Morsel Sales Visualiser"),
		dcc.Graph(id="sales-line-chart", figure=line_figure),
	]
)


if __name__ == "__main__":
	app.run(debug=True)
