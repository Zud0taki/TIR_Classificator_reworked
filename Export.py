# import functions from ShapeWriter
import fiona


def get_temp(threshold):
    temp = (threshold - 30000) / 100  # 30000dn == 0°C every 100dn == 1°C
    return temp


# define ShapeWrite
# used to export the shapefile
def ShapeWrite(acml_list, threshold, outputpath):  # temperature
    # get the temp from threshold
    temperature = get_temp(threshold)
    # set the file name
    polygon_name = r"" + outputpath + "/" + str(int(threshold)) + "dn_around_" + str(temperature) + "°C" + ".shp"  # str(temperature) + "dn - " + "above" + "°C"
    # initialize xy_list
    xy_list = []
    # give the Shapefile a schema
    schema = {
        'geometry': 'Polygon',
        'properties': [('Name', 'str')]
    }
    # create the Polygon Shape with name, mode, coordinate system and driver
    polyShp = fiona.open(polygon_name, mode='w', driver='ESRI Shapefile',
                         schema=schema, crs="WGS84")
    label_counter = 1
    # iterate through the acml_list
    for x in range(len(acml_list)):
        # if seprator is not found - append xy_list
        if acml_list[x][1][0] != 0:
            xy_list.append((acml_list[x][1][1], acml_list[x][1][0]))
        # if seperator is found - count up - set counter as polygon id and save to the polyShp-Object
        else:
            label_counter += 1
            polygon_id = str(label_counter)
            # save record and close shapefile
            rowDict = {
                'geometry': {'type': 'Polygon',
                             'coordinates': [xy_list]},  # Here the xyList is in brackets
                'properties': {'Name': polygon_id},
            }
            polyShp.write(rowDict)
            # clear the list
            xy_list.clear()
    # close the polyShp-Object
    polyShp.close()


# define export function using accumulated list, threshold value, temperature value and the outputpath
# write Shapefile.txt with the items from the accumulated list
def export(acml_list, threshold, outputpath):  # temperature
    with open('Shapefile.txt', 'w') as f:
        for item in acml_list:
            f.write("%s\n" % item)
    ShapeWrite(acml_list, threshold, outputpath)  # temperature
