import osmapi
import requests

##### Fill configuration
NB_STAR = 3
OSM_USERNAME = ""
OSM_PASSWORD = ""

api = osmapi.OsmApi(OSM_USERNAME, OSM_PASSWORD)

f = open(f"restaurant_{NB_STAR}_etoiles.txt", "r")

lines = f.readlines()
for line in lines:
    # get data from qwant maps autocomplete api endpoint
    autocomplete_results = requests.get("https://www.qwant.com/maps/detail/v1/autocomplete?q={}".format(line))

    # for each result from autocomplete, select the first existing restaurant
    for suggest_result in autocomplete_results.json()['features']:
        if line.split(',')[0] in suggest_result["properties"]["geocoding"]["label"] and "poi_types" in \
                suggest_result["properties"]["geocoding"] and suggest_result["properties"]["geocoding"]["poi_types"][0][
            "id"] == "class_restaurant:subclass_restaurant":
            if suggest_result["properties"]["geocoding"]["id"].split(':')[1] == "node":
                node = api.NodeGet(suggest_result["properties"]["geocoding"]["id"].split(':')[2])
                # if the tag was not already set
                if "stars" not in node['tag']:
                    api.ChangesetCreate(
                        {u"comment": f"Add michelin star {NB_STAR} star restaurants", u"created_by": f"{OSM_USERNAME}"})
                    print(line.split(',')[0])
                    node['tag']['stars'] = f'{NB_STAR}'
                    api.NodeUpdate(node)
                    api.ChangesetClose()
                break
            if suggest_result["properties"]["geocoding"]["id"].split(':')[1] == "way":
                way = api.WayGet(suggest_result["properties"]["geocoding"]["id"].split(':')[2])
                if "stars" not in way['tag']:
                    api.ChangesetCreate(
                        {u"comment": f"Add michelin star {NB_STAR} star restaurants", u"created_by": f"{OSM_USERNAME}"})
                    print(line.split(',')[0])
                    way['tag']['stars'] = f'{NB_STAR}'
                    api.WayUpdate(way)
                    api.ChangesetClose()
                break
