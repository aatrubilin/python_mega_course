import folium
import pandas as pd


nsk_sport_places = pd.read_csv("nsk_sports.csv")
# 'Type', 'District', 'Street', 'House', 'SportType', 'Phone', 'Latitude', 'Longitude'


map_ = folium.Map(
    location=[54.986994, 82.905433],
    tiles="OpenStreetMap",
    zoom_start=12,
)

# Add Sport places layers

sg = folium.FeatureGroup(name="Sports grounds")
hb = folium.FeatureGroup(name="Hockey Boxes")
oth = folium.FeatureGroup(name="Others")

__colors = {
    "Спортивная площадка": (sg, "green"),
    "Хоккейная коробка": (hb, "blue"),
}


def type_producer(place_type):
    # 'red', 'blue', 'green', 'purple', 'orange', 'darkred',
    # 'lightred', 'beige', 'darkblue', 'darkgreen',
    # 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue',
    # 'lightgreen', 'gray', 'black', 'lightgray'

    return __colors.get(place_type, (oth, "red"))


for index, row in nsk_sport_places.iterrows():
    fg, color = type_producer(row["Type"])
    fg.add_child(
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            name=row["Type"],
            popup=f"<b>{row['SportType']}</b><br><i>{row['Street']}, {row['House']}</i><br>{row['Phone']}",
            icon=folium.Icon(color=color),
        )
    )

map_.add_child(sg)
map_.add_child(hb)
map_.add_child(oth)


# Add population layer
pop = folium.FeatureGroup(name="Population", show=False)


def population_color(r):
    pop2005 = r["properties"]["POP2005"]
    if pop2005 < 10_000_000:
        color_ = "green"
    elif pop2005 < 20_000_000:
        color_ = "orange"
    else:
        color_ = "red"
    return {"fillColor": color_}


pop.add_child(
    folium.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(),
        style_function=population_color
    )
)

map_.add_child(pop)

map_.add_child(folium.LayerControl())

map_.save("map.html")
