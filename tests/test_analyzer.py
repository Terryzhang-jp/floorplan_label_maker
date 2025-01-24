import unittest
from pathlib import Path
import json
import sys
import os
from unittest import skip, skipIf

# Set environment variable to suppress gRPC warning
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '0'

# Add project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.floorplan_analyzer import FloorplanAnalyzer, Config

def requires_api(func):
    """Decorator: Mark tests that require API access"""
    return func

class TestFloorplanAnalyzer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Class level setup, runs once"""
        cls.data_dir = Path(__file__).parent.parent / "data"
        cls.env_path = Path(__file__).parent.parent / ".env"
        
        if not cls.data_dir.exists() or not any(cls.data_dir.glob("*.png")):
            raise unittest.SkipTest("Test data directory does not exist or no test images found")
    
    def setUp(self):
        """Setup before each test method"""
        self.image_files = list(self.data_dir.glob("*.jpg")) + list(self.data_dir.glob("*.png"))
        self.analyzer = FloorplanAnalyzer(Config(env_path=str(self.env_path)))
        self.test_image = self.image_files[0]
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        self.assertIsNotNone(self.analyzer)
        self.assertIsInstance(self.analyzer.config, Config)
    
    def test_result_is_json(self):
        """Test if return result is valid JSON format"""
        result = self.analyzer.analyze(self.test_image)
        self.assertIsNotNone(result, "Analysis result should not be None")
        
        # Verify result can be serialized to JSON
        try:
            json.dumps(result)
        except Exception as e:
            self.fail(f"Result cannot be serialized to JSON: {str(e)}")
    
    def test_result_structure(self):
        """Test if JSON result structure meets expectations"""
        result = self.analyzer.analyze(self.test_image)
        self.assertIsNotNone(result, "Analysis result should not be None")
        
        # Check if contains interior_design_features
        self.assertIn("interior_design_features", result, 
                     "Result must contain 'interior_design_features' field")
        
        # Check if interior_design_features is a list
        self.assertIsInstance(result["interior_design_features"], list,
                            "'interior_design_features' must be a list")
        
        # Check if has minimum required features
        self.assertGreaterEqual(
            len(result["interior_design_features"]),
            self.analyzer.config.min_features,
            f"Interior features should have at least {self.analyzer.config.min_features} items"
        )
        
        # If has exterior_design_features, check its format
        if "exterior_design_features" in result:
            self.assertIsInstance(result["exterior_design_features"], list,
                                "'exterior_design_features' must be a list")
    
    def test_feature_format(self):
        """Test if feature descriptions meet requirements"""
        result = self.analyzer.analyze(self.test_image)
        self.assertIsNotNone(result, "Analysis result should not be None")
        
        for feature in result["interior_design_features"]:
            # Check if is string
            self.assertIsInstance(feature, str, "Feature description must be string")
            
            # Check if word count is within config range
            words = feature.split()
            self.assertGreaterEqual(
                len(words),
                self.analyzer.config.min_words_per_feature,
                f"Feature description '{feature}' has fewer than {self.analyzer.config.min_words_per_feature} words"
            )
            self.assertLessEqual(
                len(words),
                self.analyzer.config.max_words_per_feature,
                f"Feature description '{feature}' has more than {self.analyzer.config.max_words_per_feature} words"
            )
    
    def test_feature_uniqueness(self):
        """Test if features are unique"""
        result = self.analyzer.analyze(self.test_image)
        self.assertIsNotNone(result, "Analysis result should not be None")
        
        # Check if interior features have duplicates
        interior_features = result["interior_design_features"]
        self.assertEqual(
            len(interior_features),
            len(set(interior_features)),
            "Interior features contain duplicates"
        )
        
        # If has exterior features, check for duplicates
        if "exterior_design_features" in result:
            exterior_features = result["exterior_design_features"]
            self.assertEqual(
                len(exterior_features),
                len(set(exterior_features)),
                "Exterior features contain duplicates"
            )

if __name__ == '__main__':
    unittest.main(verbosity=2) 