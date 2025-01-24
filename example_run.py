from pathlib import Path
from floorplan_analyzer import FloorplanAnalyzer

def main():
    # Initialize analyzer
    analyzer = FloorplanAnalyzer()
    
    # Get the test image path
    data_dir = Path(__file__).parent / "data"
    test_images = list(data_dir.glob("*.jpg")) + list(data_dir.glob("*.png"))
    
    if not test_images:
        print("Error: No test images found in data directory")
        return
    
    # Use the first image
    test_image = test_images[0]
    print(f"\nAnalyzing floor plan: {test_image.name}")
    print("-" * 50)
    
    # Analyze the floor plan
    result = analyzer.analyze(test_image)
    
    if result:
        print("\nAnalysis Results:")
        print("-" * 50)
        
        # Print interior features
        if "interior_design_features" in result:
            print("\nInterior Features (ranked by uniqueness):")
            for i, feature in enumerate(result["interior_design_features"], 1):
                print(f"{i}. {feature}")
        
        # Print exterior features if any
        if "exterior_design_features" in result:
            print("\nExterior Features (ranked by uniqueness):")
            for i, feature in enumerate(result["exterior_design_features"], 1):
                print(f"{i}. {feature}")
    else:
        print("Analysis failed. Please check the error message above.")

if __name__ == "__main__":
    main() 