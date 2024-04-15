#Add functions to import
import seaborn as sns
import plotly.express as px
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly

#Import the dataset
import palmerpenguins 

#Load the dataframe for Palmer Penguins
df = palmerpenguins.load_penguins()

#Set up the Page Title
ui.page_opts(title="Palmer Penguins Data Statistics", fillable=True)

#Add a sidebar, Use a subheading for additional details
with ui.sidebar(title="Filter controls", style="background-color: #F0FFFF; font-family: 'Comic Sans MS';"):
    ui.h2("Select the mass or species", class_="text-center")
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    #Use ui.hr() to add a horizontal line on the display
    ui.hr()

    #Add links with Source weblink, App weblink, Issues weblink, and more    
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/sapapesh/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="sapapesh.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/sapapesh/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

#Add value box with number of penguins with filtered data
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), style="background-color: #F0FFFF;"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    #Add value box with bill length with filtered data
    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="background-color: #F0FFFF;"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    #Add value box with bill depth with filtered data
    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="background-color: #F0FFFF;"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

#Add Scatterplot with the bill length and depth
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram - Bill length and depth", style="background-color: #F0FFFF;")

        @render_plotly
        def plot():
            return px.histogram(
                data_frame=filtered_df(),
                x="bill_length_mm", 
                y="bill_depth_mm",
                color="species",
            )

    #Add data frame with the Penguin data broken out in columns
    with ui.card(full_screen=True):
        ui.card_header("Penguin data", style="background-color: #F0FFFF;")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=False)


#ui.include_css(app_dir / "styles.css")

#Add reactive calculator with input of species selected and filtered by body mass.
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
