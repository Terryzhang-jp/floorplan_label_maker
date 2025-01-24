# Floor Plan Label Maker

A tool that uses Google's Gemini API to analyze floor plans and extract distinctive features.

## Features

- Analyzes floor plan images using AI
- Identifies unique interior and exterior features
- Ranks features by uniqueness
- Outputs results in structured JSON format
- Includes comprehensive test suite

## Requirements

- Python 3.8 or higher
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Terryzhang-jp/floorplan_label_maker.git
cd floorplan_label_maker
```

2. Install dependencies:
```bash
pip install -e .
```

3. Set up environment:
   - Create a `.env` file in the project root
   - Add your Gemini API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

1. Place your floor plan images in the `data` directory

2. Run the analyzer:
```bash
python example_run.py
```

The tool will analyze the floor plan and output:
- Interior design features (ranked by uniqueness)
- Exterior design features (if present)

## Testing

Run the test suite:
```bash
python -m unittest tests/test_analyzer.py -v
```

## Project Structure

```
floorplan_analyzer/
├── src/
│   └── floorplan_analyzer/
│       ├── __init__.py
│       ├── analyzer.py    # Main analysis logic
│       └── config.py      # Configuration handling
├── tests/
│   └── test_analyzer.py   # Test suite
├── data/                  # Floor plan images
└── example_run.py         # Example usage
```

## License

MIT License

## Author

Terry Zhang