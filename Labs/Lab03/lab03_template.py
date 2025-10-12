pip install geopandas
import os
import geopandas as gpd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

class CensusTract:
    def __init__(self, geoid, population, geometry):
        self.geoid = geoid
        self.population = population
        self.geometry = geometry
    
    def calculate_population_density(self):
        
        area_sq_meters = self.geometry.area
        area_sq_kilometers = area_sq_meters / 1000000

        if area_sq_kilometers == 0:
            population_density = 0.0
        else:
            population_density = self.population / area_sq_kilometers
        # calculate the population density based on geometry
        ### >>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<< ###
        
        return population_density
        ### <<<<<<<<<<< END OF YOUR CODE <<<<<<<<<<< ###
_+


if __name__ == "__main__":
    # read data
    file_path = os.path.join(DATA_DIR, 'data.geojson')
    # load data into GeoDataFrame
    gdf = gpd.read_file(file_path)
    # preview data
    print(gdf.head())
    print(gdf.columns)
    print(gdf.shape)
    print(gdf.dtypes)

    # calculate the Population Density based on geometry
    ### >>>>>>>>>>>> YOUR CODE HERE <<<<<<<<<<< ###
    # instantiate the CensusTract class

    # calculate the population density for each census tract

    new_densities = gdf.apply(
        lambda row: CensusTract(
            geoid=row['GeoId'], 
            population=row['Pop'], 
            geometry=row['geometry']
        ).calculate_population_density(), 
        axis=1
    )

    # create a new column for the population density and name it as 'Pop_Den_new'
gdf['Pop_Den_new'] = new_densities
    ### <<<<<<<<<<< END OF YOUR CODE <<<<<<<<<<< ###

    # preview the data again
    print(gdf.head())
    
