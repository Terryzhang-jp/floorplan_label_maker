import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import google.generativeai as genai
from PIL import Image

from .config import Config

class FloorplanAnalyzer:
    """Floor Plan Analysis Class"""
    
    def __init__(self, config: Config = None):
        """
        Initialize analyzer
        
        Args:
            config: Configuration object (optional)
        """
        self.config = config or Config()
        self._setup_model()
    
    def _setup_model(self):
        """Setup Gemini model"""
        genai.configure(api_key=self.config.api_key)
        self.model = genai.GenerativeModel(self.config.model_name)
    
    def _create_prompt(self) -> str:
        """Create analysis prompt"""
        return """As an experienced real estate agent, analyze this floorplan to identify distinctive features that are clearly visible and confirmed from the floorplan only.

What counts as a "distinctive feature":

Unique Design Elements:
-Special layout arrangements (e.g., "dual-level studio design")
-Uncommon room combinations or connections
-Premium design choices (e.g., "butler's pantry setup")
-Luxury space planning (e.g., "ensuite master arrangement")

Premium Facilities:
-Luxury amenities (e.g., "heated indoor pool")
-High-end additions (e.g., "wine cellar storage")
-Entertainment spaces (e.g., "home theater setup")
-Wellness facilities (e.g., "dedicated gym space")

Practical Valuable Features:
-Multiple car accommodation (e.g., "triple car garage")
-Storage solutions (e.g., "walk-in pantry system")
-Utility setups (e.g., "separate laundry room")
-Service areas (e.g., "mud room entrance")

Outdoor Features and Amenities:
-Pool and spa facilities
-Outdoor living spaces (e.g., "covered deck area")
-Garden features (e.g., "landscaped courtyard")
-Outdoor entertainment

Features that consumers value:
-Garage and its size (e.g., "4 car garage space")
-Swimming pool (e.g., "pool design")
-Outdoor entertainment areas (e.g., "multiple deck zones")

Examples of Good Feature Descriptions:

Interior:
✓ "Dual-level workspace design"
✓ "Butler's pantry integration"
✓ "Triple bathroom configuration"
✓ "Walk-in robe system"
✓ "Open-plan living arrangement"

Exterior:
✓ "Double car garage setup"
✓ "Multi-level deck system"
✓ "Pool entertainment zone"
✓ "Covered entry design"

Examples of Poor Descriptions:
× "Kitchen"
× "Large bedroom"
× "Nice view"

Strict Analysis Rules:
Each feature must describe a unique aspect
Features must highlight distinctive elements
Include both design and facility features
Quantify where relevant (e.g., "double", "triple")
Use 2-4 words for each description
No duplicate features
List minimum 5 features per category
Must be clearly marked in plan

Present in this JSON format:
{
    "interior_design_features": [
        "feature 1",
        "feature 2"
    ],
    "exterior_design_features": [
        "feature 1",
        "feature 2"
    ]
}

please rank the features according to its uniqueness.If floorplan contains no exterior feature, then output nothing."""
    
    def analyze(self, image_path: Union[str, Path]) -> Optional[Dict[str, List[str]]]:
        """
        Analyze floor plan
        
        Args:
            image_path: Path to floor plan image
            
        Returns:
            Dictionary containing interior and exterior features
        """
        try:
            # Use with statement to ensure file is properly closed
            with Image.open(image_path) as image:
                # Create prompt
                prompt = self._create_prompt()
                
                # Generate analysis result
                response = self.model.generate_content([prompt, image])
                
                # Extract JSON part
                try:
                    # Try to parse response text directly as JSON
                    result = json.loads(response.text)
                except json.JSONDecodeError:
                    # If direct parsing fails, try to extract JSON part from text
                    text = response.text
                    start_idx = text.find('{')
                    end_idx = text.rfind('}') + 1
                    if start_idx != -1 and end_idx != -1:
                        json_str = text[start_idx:end_idx]
                        result = json.loads(json_str)
                    else:
                        raise ValueError("Could not extract JSON from response")
                
                # Validate result format
                if not isinstance(result, dict):
                    raise ValueError("Invalid result format")
                
                if "interior_design_features" not in result:
                    raise ValueError("Missing required 'interior_design_features' field")
                
                return result
                
        except Exception as e:
            print(f"Error analyzing floor plan: {str(e)}")
            return None
    
    def validate_features(self, features: List[str]) -> bool:
        """
        Validate feature descriptions
        
        Args:
            features: List of feature descriptions
            
        Returns:
            Whether descriptions meet requirements
        """
        for feature in features:
            words = feature.split()
            if not (self.config.min_words_per_feature <= len(words) <= self.config.max_words_per_feature):
                return False
        return True 