'''
Call from command line as
python -m <project-name>
'''

from luigi import build
from .orchestration.orchestrate import VisualizeFeatureImportance, VisualizePreditions

if __name__ == '__main__':
    build([VisualizeFeatureImportance(), VisualizePreditions()], local_scheduler=True)
    # luigi.run() # Use this to get luigid graph at http://localhost:8082 

