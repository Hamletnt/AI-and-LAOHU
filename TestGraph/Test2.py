import altair as alt
import pandas as pd

data = pd.DataFrame({
    'Category': ['วัตถุดิบ', 'ค่าเช่า', 'อุปกรณ์', 'ค่าไฟ'],
    'Value': [58.49, 3.14, 0.27, 5.19]
})

chart = alt.Chart(data).mark_arc().encode(
    theta=alt.Theta(field="Value", type="quantitative"),
    color=alt.Color(field="Category", type="nominal"),
    tooltip=['Category', 'Value']
)

chart.show()