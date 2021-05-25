# NBDash
NBDash (Namur Budget Dashboard) is an interactive dashboard which allows citizens to understand how the budget is dispatched per function
in the municipality of Namur. A demo of the dashboard is accessible at the following link: https://rb.gy/fsq8d3

## Data Used
NBDash used two main datasets available on the Namur open data portal:
[Namur-Ordinary Budget by function](https://rb.gy/61r8dk) and [Namur-Extraordinary Budget by function](https://rb.gy/dpayws)

## Objective
The dashboard was created to evaluate whether citizens are more receptive to well-designed dashboards than to visualizations offered on a traditional Open Government Data portal.  

## How to install
* Clone the repository
* Install dependencies (Pandas, Plotly, Dash):
  * pip install -r requirements.txt

## Interface
![HomePage](/assets/Homepage_NBDash.png)
HomePage Interface of NBDash.

![NBDash Interface for simple display](/assets/NBDash.png)
NBDash Interface for simple display. (1): Description of dashboard. (2): Information about the data used. (3): Possibility to give feedback and track status (4): Possibility to choose the display type (simple, less advanced and advanced). (3): Filters used to update the visualizations. (6): Display of the data overview. (6): Visualization used to present more details with descending sorting to help the user easily capture insights. (7): Automatic description and interpretation of the graph.   

![NBDash Interface for Less advanced and Advanced displays.](/assets/NBDash.png)
NBDash Interface for Less advanced and Advanced displays. For less advanced users, the button “Edit chart”(6-B) isn’t visible. Section 6-A is used to display the selected visualization followed by data displayed in table format (6-C). Section 7-A allows to choose the type of graph. Section 7-B allows to choose the data to be displayed on axis X. Section 7-C allows to choose the functions to be represented in the graph. Section 7-D allows to specify the sorting option.

## Contact Us
Abiola P. Chokki (abiola-paterne.chokki@unamur.be)
