from .segs import NudenetDetector
from .segs import *

MAX_RESOLUTION = 8496
class NudeNetDetectorProvider:
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {}
        }

    RETURN_TYPES = ("BBOX_DETECTOR", )
    FUNCTION = "load_nudenet"

    CATEGORY = "ImpactPack"

    def load_nudenet(self):
        return (NudenetDetector, )

    
        
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "NudeNetDetectorProvider": NudeNetDetectorProvider
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "NudeNetDetectorProvider": "NudeNet _Detector_Provider"
}
