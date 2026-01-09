<<<<<<< HEAD
# Fingerprint_3

A comprehensive fingerprint image processing pipeline that enhances and processes fingerprint images through multiple stages of image analysis and improvement.

## 📋 Project Overview

Fingerprint_3 is a Python-based image processing system designed to process fingerprint images through a sophisticated pipeline. It takes raw fingerprint images as input and produces enhanced, processed fingerprint images suitable for further analysis or biometric applications.

## 🏗️ Project Structure

```
Fingerprint_3/
├── .git/                            # Git version control
├── .gitignore                       # Git ignore rules
├── main.py                          # Main entry point for the application
├── requirements.txt                 # Python package dependencies
├── README.md                        # Project documentation
├── venv/                            # Virtual environment (not tracked)
│
├── input/                           # Input folder for raw fingerprint images
│   ├── finger1.jpg                 # Sample fingerprint image 1
│   ├── finger2.jpg                 # Sample fingerprint image 2
│   ├── Fingers_test/               # Test dataset folder
│   └── Samarth/                    # Sample dataset folder
│
├── output/                          # Output folder for processed images
│   ├── 01_roi.png                  # ROI extraction output
│   ├── 02_gray.png                 # Grayscale conversion output
│   ├── 03_normalized.png           # Normalized image output
│   ├── 04_gabor_energy.png         # Gabor filter output
│   ├── 06_binary.png               # Thresholding output
│   ├── final_fingerprint.png       # Final processed fingerprint
│   ├── finger1.jpg                 # Processed sample 1
│   ├── finger2.jpg                 # Processed sample 2
│   ├── Fingers_test/               # Processed test dataset
│   └── Samarth/                    # Processed sample dataset
│
├── pipeline/                        # Core image processing modules
│   ├── __init__.py                 # Package initializer
│   ├── acquisition.py              # Image loading functionality
│   ├── roi_extraction.py           # Region of Interest (ROI) extraction
│   ├── preprocessing.py            # Image preprocessing and normalization
│   ├── gabor_enhancement.py        # Gabor filter ridge enhancement
│   ├── thresholding.py             # Adaptive thresholding
│   ├── ridge_postprocess.py        # Post-processing for ridge enhancement
│   └── __pycache__/                # Python cache (not tracked)
│
└── utils/                           # Utility modules
    ├── __init__.py                 # Package initializer
    ├── io_utils.py                 # Input/Output utilities
    └── __pycache__/                # Python cache (not tracked)
```

## 🔄 Processing Pipeline

The application processes fingerprint images through the following stages:

1. **Acquisition** (`acquisition.py`)
   - Loads fingerprint images from disk using OpenCV
   - Supports multiple image formats (JPG, JPEG, PNG, BMP)

2. **ROI Extraction** (`roi_extraction.py`)
   - Extracts the Region of Interest from the fingerprint image
   - Focuses processing on relevant areas

3. **Preprocessing** (`preprocessing.py`)
   - Normalizes image data
   - Prepares image for enhancement filters

4. **Gabor Enhancement** (`gabor_enhancement.py`)
   - Applies Gabor filter for ridge enhancement
   - Improves fingerprint ridge clarity and visibility

5. **Adaptive Thresholding** (`thresholding.py`)
   - Converts grayscale image to binary
   - Uses adaptive thresholding for better ridge definition

6. **Ridge Postprocessing** (`ridge_postprocess.py`)
   - Further enhances ridge patterns
   - Final image refinement and cleanup

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Clone or navigate to the project directory:
   ```bash
   cd Fingerprint_3
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📦 Dependencies

- **opencv-python** - Image processing and computer vision
- **numpy** - Numerical computing and array operations
- **scipy** - Scientific computing and signal processing
- **scikit-image** - Image processing algorithms

## 💻 Usage

### Process a Single Image
```bash
python main.py input/path/to/image.jpg
```

### Process All Images in a Folder
```bash
python main.py input/folder_name
```

### Examples
```bash
# Process a single fingerprint image
python main.py input/Samarth/finger.jpg

# Process all images in the Fingers_test folder
python main.py input/Fingers_test

# Process all images in the Samarth folder
python main.py input/Samarth
```

### Supported Image Formats
- `.jpg` / `.jpeg`
- `.png`
- `.bmp`

### Output
- Processed images are saved to the `output/` directory
- Folder structure is automatically created to mirror the input structure
- Output files retain the same filename as input files

## 📝 File Descriptions

### Configuration Files
| File | Purpose |
|------|---------|
| `.gitignore` | Specifies files and directories to ignore in version control |
| `requirements.txt` | Lists all Python package dependencies |

### Main Application
| File | Purpose |
|------|---------|
| `main.py` | Application entry point; handles CLI arguments and orchestrates the processing pipeline |

### Pipeline Modules (`pipeline/`)
| File | Purpose |
|------|---------|
| `acquisition.py` | Loads fingerprint images from file paths using OpenCV |
| `roi_extraction.py` | Extracts the Region of Interest (ROI) from fingerprint image |
| `preprocessing.py` | Normalizes and prepares images for enhancement filters |
| `gabor_enhancement.py` | Applies Gabor filters for ridge-oriented enhancement |
| `thresholding.py` | Converts enhanced grayscale images to binary format using adaptive thresholding |
| `ridge_postprocess.py` | Final ridge enhancement, cleanup, and postprocessing |
| `__init__.py` | Makes the pipeline folder a Python package |

### Utility Modules (`utils/`)
| File | Purpose |
|------|---------|
| `io_utils.py` | Image input/output utility functions (save, load, etc.) |
| `__init__.py` | Makes the utils folder a Python package |

## 🎯 Features

✅ Single image processing  
✅ Batch processing of image folders  
✅ Automatic output directory creation  
✅ Error handling for invalid images  
✅ Support for multiple image formats  
✅ Advanced fingerprint enhancement pipeline  
✅ Ridge pattern enhancement and clarity  

## 🐛 Error Handling

The application includes error handling for:
- Invalid or missing file paths
- Unsupported image formats
- Corrupted image files
- Directory creation issues

## 📂 Input/Output Structure

### Input Directory
```
input/
├── finger1.jpg                (sample fingerprint image)
├── finger2.jpg                (sample fingerprint image)
├── Fingers_test/              (test dataset)
│   └── [test fingerprint images]
└── Samarth/                   (sample dataset)
    └── [sample fingerprint images]
```

### Output Directory
```
output/
├── 01_roi.png                 (ROI extraction result)
├── 02_gray.png                (grayscale conversion result)
├── 03_normalized.png          (normalized image result)
├── 04_gabor_energy.png        (Gabor enhancement result)
├── 06_binary.png              (thresholding result)
├── final_fingerprint.png      (final processed fingerprint)
├── finger1.jpg                (processed sample 1)
├── finger2.jpg                (processed sample 2)
├── Fingers_test/              (processed test dataset)
│   └── [processed test images]
└── Samarth/                   (processed sample dataset)
    └── [processed sample images]
```

## 🔬 Technical Details

- **Image Format**: Processed images are saved in the same format as input
- **Color Space**: Works with color images and converts as needed
- **Filtering**: Uses Gabor filters for ridge-oriented enhancement
- **Thresholding**: Adaptive thresholding for robust binarization

## 📝 License

[Add license information if applicable]

## 👤 Author

[Add author information if applicable]

## 📞 Support

For issues or questions, please refer to the project documentation or contact the development team.

---

**Last Updated**: January 2026
=======
# Fingerprint-Scanner
New Repo
>>>>>>> 7704ace831c9fa2ada515299ad18b24fb6cdab21
