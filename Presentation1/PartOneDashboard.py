
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import json
from itertools import count


#snapshot html
snapShotHtml = "2021-02-05_SnapShotPrediction.html"

#Bootstrap themes
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
#         html.H2('Dashboard', className="display-4"),
        html.Hr(),
        html.P(
            "Part One Dashboard", className = "lead"
              ),
        dbc.Nav(
            [
                dbc.NavLink("Business Problem", href="/page-1", id = "page-1-link"),
                dbc.NavLink("Information/Questions", href="/page-2", id = "page-2-link"),
                dbc.NavLink("Assumptions", href="/page-3", id = "page-3-link"),
                dbc.NavLink("Proposed solution", href="/page-4", id = "page-4-link"),
            ],
            vertical = True,
            pills = True,
        ),
    ],
    style = SIDEBAR_STYLE,
)

#business problem
BpPage = html.P("Currently only 4% of prospective students communicated with at the Enquiry Stage mature \
                through the pipeline to enrol.\
                Business leaders would like to have higher conversion rate which is at least 5%.\
                Is there any solution that can also answer the following questions:\
                (a) Which prospective students to target? (b) Which actions or activity would be the most effective for the conversion?")

#information/questions
InfoQuestionPage = [
        html.Div(children = [
        dbc.Row(dbc.Col(html.Div("To define a solution"))),        
        dcc.Dropdown(
            id = 'informationRound',
            options = [{'label': i, 'value': i} for i in ['Information', 'Questions']],
            value = 'Information'
                    ),
        html.Div(id = "informationContent")
                            ])
            ]
#Information
section1 = "For past 3 years(an arbitrary choice)"
S1point1 = "Demographic factors of prospective students (age, gender, nationality, country of residence and education background)"
S1point2 = "Course/Programme students enquired"
S1point3 = "Date and time of enquiry, "
S1point4 = "Number of prospective students enquiring through channels (live chat, phone, email and webform)\
             and enrolling after enquiry through those channels"
S1point5 = "Communication history (if there exists for live chat, phone and email)"
InformationPage = [
                    html.Div([
                    html.H6("%s"%section1),
                    html.Br([]),
                    html.Li("%s"%S1point1),
                    html.Li("%s"%S1point2),
                    html.Li("%s"%S1point3),
                    html.Li("%s"%S1point4),
                    html.Li("%s"%S1point5),
                            ])
                    ]
#Questions
section1 = "Business Questions - determine direction/roadmap of solution"
S1point1 = "Due date of proposed solution"
S1point2 = "Business expectation of proposed solution - data product/analytical findings?"
S1point3 = "Can we use next 1-year data or latest 1-year data to evaluate our solution - take 12 months to mature on average"
section2 = "Research Questions - determine methodology"
S2point1 = "Are there any differentiating factors (demographic or other) in prospective students who enrol after inquiry \
            compared to students who do not enrol?"
S2point2 = "Is there a channel significantly better than other channels in conversion? (statistical way or exploratory)"
S2point3 = "Is there a course/programme that has significantly better conversion rate than others? In particular channel? \
            In particular institution? (statistical way or exploratory)"
S2point4 = "Is there any difference in communication between students' direct interaction with institution and via our channels?"
S2point5 = "What is prescriptive analysis that we can do given our planned research works?"
section3 = "Data Questions - determine data quality/scope"
S3point1 = "How far can we back track our data?"
S3point2 = "Do we have a list of enrolled students who communicate with institution directly?"
S3point3 = "Do we have complete communication history whether students communicate with institution directly or via our channels?"

QuestionPage = [
                    html.Div([
                    #Business Questions
                    html.H6("%s"%section1),
                    html.Br([]),
                    html.Li("%s"%S1point1),
                    html.Li("%s"%S1point2),
                    html.Li("%s"%S1point3), 
                    html.Br([]),
                    #Research Questions
                    html.H6("%s"%section2),
                    html.Br([]),
                    html.Li("%s"%S2point1),
                    html.Li("%s"%S2point2),
                    html.Li("%s"%S2point3), 
                    html.Li("%s"%S2point4),   
                    html.Br([]),
                    #Data Questions
                    html.H6("%s"%section3),
                    html.Br([]),
                    html.Li("%s"%S3point1),
                    html.Li("%s"%S3point2),
                    html.Li("%s"%S3point3),
                            ]),
                ]

#assumption
section1 = "Assumptions which affect information/questions to get/ask"
S1point1 = "1 batch: take 1 year to mature from enquiry to enrolment"
S1point2 = "Next 1-year data to re-evaluate proposed solution (first evaluation using latest 1-year data)"
S1point3 = "Pattern is consistent over batches (if one or few batches is/are used in once)"
S1point4 = "Stakeholders prefer a balance between results' interpretability and results"
AssumptionPage = html.Div(
                            [
                                html.H6("%s"%section1),
                                html.Div(
                                        [
                                html.Li("%s"%S1point1),
                                html.Li("%s"%S1point2),
                                html.Li("%s"%S1point3),
                                html.Li("%s"%S1point4),
                                        ]
                                        )
                            ]
                        )

#solution
solution = "solutionPart1.png"
SolutionPage = [html.Img(
                        src = app.get_asset_url(solution),
                        style={'height':'50%', 'width':'70%'}
                )]

content = html.Div(id="page-content", style = CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id = "url"), sidebar, content])
                    
#callback on link
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
            )
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]
                
#callback on page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return BpPage
    elif pathname == "/page-2":
        return InfoQuestionPage
    elif pathname == "/page-3":
        return AssumptionPage
    elif pathname == "/page-4":
        return SolutionPage
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
                        )

#callback on details
@app.callback([Output('informationContent', 'children')],
              [Input('informationRound', 'value')])
def churnOutDetails(value):
    if value == "Information":
        return InformationPage
    elif value == "Questions":
        return QuestionPage
           
if __name__ == '__main__':
    app.run_server(debug=True)
