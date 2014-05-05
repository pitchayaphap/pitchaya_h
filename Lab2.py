#Pitchaya Phapanon
#Lab 2 Assignment
#Geoprocessing 
#May 4th 2014

#I worked with Jorge and Prescott for writing my script
#We worked together by searching through Esri Help center and ArcMap Help.


#getting Canopy/Ipython to be able to import each others's packages
import sys
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\bin')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\arcpy')
sys.path.append('C:\\Program Files (x86)\\ArcGIS\\Desktop10.2\\ArcToolbox\\Scripts')
import arcpy

input_fc = arcpy.GetParameterAsText(0) #input feature class
output_fc = arcpy.GetParameterAsText(1) #output feature class
input_table = arcpy.GetParameterAsText(2) #input reclass table
input_field = arcpy.GetParameterAsText(3) #name field reclassified
output_field = arcpy.GetParameterAsText(4) #name output field
NotFoundValue = arcpy.GetParameterAsText(5) #value used in output field for NULL values

fieldname = arcpy.ValidateFieldName(output_field) #Validate new field name
arcpy.CopyFeatures_management(input_fc, output_fc)  #create new feature class
arcpy.AddField_management(output_fc, fieldname, "DOUBLE") #add the validate field to the output feature class

#search through input feature class
cursor_fc = arcpy.da.UpdateCursor(output_fc, [input_field, fieldname])
for row_fc in cursor_fc: #search in reclass table
    cursor_table = arcpy.da.SearchCursor(input_table, ["lowerbound", "upperbound", "value"])
    row_fc[1] = NotFoundValue #initialize value in output field with NotFoundValue
    cursor_fc.updateRow(row_fc)
    for row_table in cursor_table: #if reclass value exists over write existing value with value from row in table
        if row_fc[0] >= row_table[0] and row_fc[0] <= row_table[1]:
            row_fc[1] = row_table[2]
            cursor_fc.updateRow(row_fc)
        else:
            pass
    del row_table
    del cursor_table
del row_fc
del cursor_fc