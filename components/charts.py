import plotly.express as px
import streamlit as st


def _theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(8,22,36,.45)",
        font=dict(family="DM Sans", color="#d9eff8"),
        margin=dict(l=20, r=20, t=55, b=20),
        title_font=dict(family="Space Grotesk", size=18),
        hoverlabel=dict(bgcolor="#10283b"),
    )
    return fig


def show_convergence_chart(history):
    values = [x for x in history if x is not None]
    if not values:
        return
    fig = px.line(
        x=list(range(1, len(values) + 1)),
        y=values,
        labels={"x": "Iteration", "y": "Best Route Cost"},
        title="Optimization Convergence",
        markers=True,
    )
    st.plotly_chart(_theme(fig), use_container_width=True)


def show_bar_chart(dataframe, x, y, title):
    if dataframe.empty:
        return
    fig = px.bar(dataframe, x=x, y=y, title=title)
    st.plotly_chart(_theme(fig), use_container_width=True)
