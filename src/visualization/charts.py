import plotly.express as px
import plotly.graph_objects as go

def create_salary_trend_chart(df, metric_type='mean'):
    
    #Tworzy wykres trendu wynagrodzeń w czasie.
    if metric_type in ['mean', 'median']:
        if metric_type == 'mean':
            data = df.groupby('work_year')['salary_in_usd'].mean().reset_index()
            title = "Średnie wynagrodzenie w czasie"
            y_label = "Średnie wynagrodzenie (USD)"
        else:
            data = df.groupby('work_year')['salary_in_usd'].median().reset_index()
            title = "Mediana wynagrodzenia w czasie"
            y_label = "Mediana wynagrodzenia (USD)"
        
        fig = px.bar(
            data,
            x='work_year',
            y='salary_in_usd',
            title=title,
            labels={'work_year': 'Rok', 'salary_in_usd': y_label},
            color_discrete_sequence=["#DF3F3F"]
        )
        fig.update_xaxes(dtick=1)
        fig.update_traces(marker_line_width=1.2, marker_line_color="white")
        
    else:  # count
        data = df.groupby('work_year').size().reset_index(name='count')
        fig = px.line(
            data,
            x='work_year',
            y='count',
            title="Liczba ofert pracy w czasie",
            labels={'work_year': 'Rok', 'count': 'Liczba ofert'},
            color_discrete_sequence=["#e23333"]
        )
        fig.update_xaxes(dtick=1)
    
    return fig

def create_top_jobs_chart(top10_df):
    
    #Tworzy wykres słupkowy top 10 stanowisk.
    fig = px.bar(
        top10_df,
        x='mean_salary',
        y='job_title',
        orientation='h',
        title="Średnie wynagrodzenia — Top 10 stanowisk",
        labels={"mean_salary": "Średnie wynagrodzenie (USD)", "job_title": "Stanowisko"},
        color_discrete_sequence=["#1DB954"]
    )
    fig.update_layout(yaxis_categoryorder='total ascending')
    fig.update_traces(marker_line_width=1.2, marker_line_color="white")
    return fig

def create_salary_distribution_chart(df_plot):
    
    #Tworzy histogram rozkładu wynagrodzeń.
    fig = px.histogram(
        df_plot,
        x='salary_in_usd',
        nbins=60,
        title="Rozkład wynagrodzeń (USD)",
        labels={'salary_in_usd': "Wynagrodzenie (USD)"},
        color_discrete_sequence=["#1DB954"]
    )
    fig.update_traces(marker_line_width=1.2, marker_line_color="white")
    fig.update_yaxes(title_text="Liczba pracowników")
    return fig

def create_country_comparison_chart(df, selected_countries):
    
    #Tworzy wykres porównujący kraje.
    subset = df[df["company_location"].isin(selected_countries)]
    compare_stats = subset.groupby("company_location")["salary_in_usd"].mean().reset_index()
    
    fig = px.bar(
        compare_stats,
        x="company_location",
        y="salary_in_usd",
        title="Średnie wynagrodzenia — wybrane kraje",
        labels={"company_location": "Kraj", "salary_in_usd": "Średnia (USD)"},
        color_discrete_sequence=["#067EB5"]
    )
    fig.update_traces(marker_line_width=1.7, marker_line_color="white")
    return fig

def create_job_trend_chart(job_df, selected_job):
    
    #Tworzy wykres trendu wynagrodzeń dla konkretnego stanowiska.
    trend_data = job_df.groupby('work_year')['salary_in_usd'].mean().reset_index()
    
    fig = px.line(
        trend_data,
        x='work_year',
        y='salary_in_usd',
        title=f"Trend wynagrodzeń — {selected_job}",
        labels={"work_year": "Rok", "salary_in_usd": "Średnia (USD)"},
        markers=True,
        color_discrete_sequence=["#1DB954"]
    )
    fig.update_xaxes(dtick=1)
    return fig