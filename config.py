"""
Configuration for microscopy FAQ scraper
"""

# Microscopy categories and their search keywords
MICROSCOPY_CATEGORIES = {
    "inverted_microscopes": {
        "name": "Inverted Microscopes",
        "keywords": [
            "inverted microscope",
            "inverted microscopy",
            "tissue culture microscope",
            "cell culture microscope",
            "inverted scope"
        ]
    },
    "confocal_microscopes": {
        "name": "Confocal Microscopes",
        "keywords": [
            "confocal microscope",
            "confocal microscopy",
            "confocal imaging",
            "laser scanning microscope",
            "LSCM",
            "confocal scope"
        ]
    },
    "digital_microscopes": {
        "name": "Digital Microscopes",
        "keywords": [
            "digital microscope",
            "digital microscopy",
            "USB microscope",
            "computer microscope",
            "LCD microscope"
        ]
    },
    "upright_microscopes": {
        "name": "Upright Microscopes",
        "keywords": [
            "upright microscope",
            "upright microscopy",
            "compound microscope",
            "standard microscope",
            "benchtop microscope"
        ]
    },
    "stereo_microscopes": {
        "name": "Stereo Microscopes",
        "keywords": [
            "stereo microscope",
            "stereomicroscope",
            "dissecting microscope",
            "dissection microscope",
            "stereo zoom microscope"
        ]
    },
    "digital_pathology": {
        "name": "Digital Pathology Systems",
        "keywords": [
            "digital pathology",
            "whole slide imaging",
            "WSI",
            "slide scanner",
            "virtual microscopy",
            "pathology scanner"
        ]
    },
    "microscope_cameras": {
        "name": "Microscope Cameras",
        "keywords": [
            "microscope camera",
            "microscopy camera",
            "digital camera microscope",
            "CCD camera microscope",
            "CMOS camera microscope",
            "imaging camera microscope"
        ]
    }
}

# Subreddits to search (ordered by relevance)
# Focused on academia and research professionals
SUBREDDITS = [
    "microscopy",
    "labrats",
    "biology",
    "cellbiology",
    "microbiology",
    "neuroscience",
    "biochemistry",
    "molecularbiology",
    "pathology",
    "bioinformatics",
    "biotech",
    "bioengineering",
    "labporn",  # For microscopy images/equipment
    "science",
    "askscience",
    "chemistry",
    "gradschool",  # Graduate students and researchers
    "academia",    # Academic researchers
    "scientificresearch"
]

# Question indicators in titles/text
QUESTION_KEYWORDS = [
    "?",
    "how",
    "what",
    "why",
    "when",
    "where",
    "which",
    "recommend",
    "suggestion",
    "advice",
    "help",
    "question",
    "wondering",
    "confused",
    "difference between",
    "vs",
    "versus",
    "compare",
    "comparison",
    "should i",
    "can i",
    "anyone know",
    "does anyone"
]

# Search parameters
SEARCH_CONFIG = {
    "time_filter": "all",  # all, year, month, week, day
    "sort": "relevance",   # relevance, hot, top, new, comments
    "limit": 100,          # Maximum results per search
    "min_score": 1,        # Minimum upvotes to include
    "max_results_per_category": 50  # Maximum results to keep per category
}

# Output configuration
OUTPUT_CONFIG = {
    "directory": "output",
    "csv_filename": "microscopy_faqs.csv",
    "json_filename": "microscopy_faqs.json",
    "json_by_category_filename": "microscopy_faqs_by_category.json"
}
