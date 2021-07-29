import logging
import os
log = "isochrone.log"
if os.path.isfile(log): os.remove(log)
logger = logging.basicConfig(filename=log,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

from cartoframes.data.services import Isolines
from cartoframes.auth import set_default_credentials
set_default_credentials('creds.json')

import numpy as np
import geopandas as gpd
from tqdm import tqdm


print('Program start.')

la_homes = gpd.read_file('data/vector/la_homes_clean.geojson')
chuncks = np.array_split(la_homes, 380)

print('Chucnks prepared, starting to calculate isochrones.')
for i in tqdm(range(len(chuncks)), position=0, leave=True):
    chunck = chuncks[i]
    try:
        isochrones_15, _ = Isolines().isochrones(chunck, [15*60], mode='walk', quality=3)
        isochrones_15.to_file(f'data/vector/isochrones/{i}.geojson', driver='GeoJSON')
        logging.info(f'chucnk {i} guardado.')
    except Exception as e:
        logging.info(f'Error en chunck {i}:\n  class:{e.__class__}\n  expetion:{e}')

