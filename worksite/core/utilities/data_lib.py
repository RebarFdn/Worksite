# data_lib.py
# Provide static data and utility functions for the sitelite application.

from functools import lru_cache
from typing import List, Dict

# Occupation  categories.
@lru_cache
def get_job_categories() -> List[str]:
    """Return a list of predefined job categories."""
    return [
        "all",
        "architect",
        "electrician",
        "carpenter",
        "driver",
        "joiner",
        "plumber",
        "mason",
        "painter",
        "welder",
        "roofer",
        "labourer",
        "leader",
        "foreman",
        "engineer",
        "safety officer",
        "scaffolder",        
        "steelman",
        "surveyor",
        "supervisor",
        "tiler",
        "technician",
        "landscaper",
        "inspector",
        "project manager",        
        "equipment operator",        
        "watchman",
        "welder",
        
    ]



# Rate categories.
@lru_cache
def rate_categories():
    return {
            "all": "All",
            "excavation": "Excavation",
            "steelwork": "Steelwork",
            "masonry": "Masonry",
            "carpentry": "Carpentry",
            "joinery": "Joinery",
            "painting": "Painting",
            "plumbing": "Plumbing",
            "scaffolding": "Scaffolding",
            "tiling": "Tiling",
            "welding": "Welding",
            "electrical": "Electrical",
            "housekeeping": "Housekeeping",
            "landscaping": "Landscaping",
            "roofing": "Roofing",
            "concrete": "Concrete",
            "drywall": "Drywall",
            "flooring": "Flooring",
            "demolition": "Demolition",
            "finishing": "Finishing",
            "general": "General",
    }


# Project phases.
@lru_cache
def project_phases()->dict:
    """Construction development phases

    Returns:
        dict: key value of project phases
    """        
    return {     
                
            'preliminary':'Preliminary',
            'substructure': 'Substructrue',
            'superstructure': 'Superstructure',
            'floors': 'Floors',
            'roofing': 'Roofing',
            'installations': 'Installations',
            'electrical': 'Electrical',
            'plumbung': 'Plumbing',
            'finishes': 'Finishes',
            'landscaping': 'Landscaping', 
                 
            
    }
   