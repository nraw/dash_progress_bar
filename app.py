import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from celery.result import AsyncResult
from dash.dash import no_update
from dash.dependencies import Input, Output

import celery_tasks.state_tasks as tasks

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(
    [
        html.Button(id="task_button", children="Click me nao!"),
        dcc.Interval(id="progress_bar_interval", interval=1000, disabled=True),
        dcc.Store(id="celery_id", data=None),
        html.Div(id="my-div"),
        html.Div(
            html.Div(
                [dbc.Progress(id="progress")],
                id="progress_container2",
                style={"display": "block"},
            ),
            id="progress_container1",
            style={"display": "none"},
        ),
    ]
)


@app.callback(
    [Output("progress_container1", "style"), Output("celery_id", "data")],
    [Input("task_button", "n_clicks")],
)
def start_task(n_clicks):
    if n_clicks:
        t = tasks.task.s().delay()
        celery_id = t.id
        visibility = {"display": "block"}
    else:
        visibility = {"display": "none"}
        celery_id = None
    return visibility, celery_id


@app.callback(
    [
        Output("progress", "value"),
        Output("progress_container2", "style"),
        Output("progress_bar_interval", "disabled"),
        Output("my-div", "children"),
    ],
    [Input("progress_bar_interval", "n_intervals"), Input("celery_id", "data")],
)
def update_progress_bar(progress_bar_interval, celery_id):
    print(celery_id)
    if celery_id is not None:
        t = AsyncResult(celery_id, app=tasks.app)
    if celery_id and not t.ready() and t.info is not None:
        print(f"State={t.state}, info={t.info}")
        progress = int(t.info["done"] / t.info["total"] * 100)
        visibility = {"display": "block"}
        stop_refresh = False
        result = no_update
    else:
        progress = 100
        visibility = {"display": "none"}
        stop_refresh = True
        if celery_id:
            result = t.get()
        else:
            result = no_update
    return progress, visibility, stop_refresh, result


if __name__ == "__main__":
    app.run_server(debug=True)
