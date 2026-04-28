"""
OCR Settings Management

Type-safe configuration loading from config.yaml
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple
import yaml


@dataclass
class PathsConfig:
    """File system paths configuration"""

    pdf_input_root: Path
    csv_output_root: Path
    temp_images_dir: Path
    review_dir: Path
    logs_dir: Path
    checkpoints_dir: Path


@dataclass
class PreprocessingConfig:
    """Image preprocessing parameters"""

    target_dpi: int
    grayscale: bool
    adaptive_binarization: bool
    noise_removal_method: str
    median_kernel_size: int
    skew_correction: bool
    skew_angle_threshold: float
    contrast_enhancement: bool
    clahe_clip_limit: float
    clahe_tile_grid_size: Tuple[int, int]
    thinning: bool
    border_removal: bool
    border_size: int


@dataclass
class TesseractConfig:
    """Tesseract OCR settings"""

    language: str
    psm: int
    oem: int
    config_string: str


@dataclass
class TableExtractionConfig:
    """Table region extraction settings"""

    extract_upper_table_only: bool
    upper_table_region_ratio: Tuple[float, float]


@dataclass
class PDFStructureConfig:
    """PDF structure by year"""

    years_single_page: List[int]
    years_two_page: List[int]
    page_mapping: dict


@dataclass
class CSVOutputConfig:
    """CSV output formatting"""

    separator: str
    encoding: str
    na_rep: str


@dataclass
class ValidationConfig:
    """Output validation thresholds"""

    confidence_threshold: float
    expected_min_sectors: int
    expected_columns_table1_range: Tuple[int, int]
    expected_columns_table2_range: Tuple[int, int]


@dataclass
class LoggingConfig:
    """Logging configuration"""

    level: str
    format: str
    file: str


@dataclass
class ProgressConfig:
    """Progress tracking settings"""

    checkpoint_file: str
    save_intermediate_images: bool
    auto_cleanup_temp: bool


@dataclass
class OCRSettings:
    """Complete OCR pipeline settings"""

    paths: PathsConfig
    preprocessing: PreprocessingConfig
    tesseract: TesseractConfig
    table_extraction: TableExtractionConfig
    pdf_structure: PDFStructureConfig
    csv_output: CSVOutputConfig
    validation: ValidationConfig
    logging: LoggingConfig
    progress: ProgressConfig


def load_settings(config_path: str = "OCR/ocr_config/config.yaml") -> OCRSettings:
    """
    Load OCR settings from YAML configuration file.

    Args:
        config_path: Path to config.yaml file

    Returns:
        OCRSettings instance with all configuration loaded

    Raises:
        FileNotFoundError: If config file doesn't exist
        yaml.YAMLError: If config file is malformed
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, "r", encoding="utf-8") as f:
        config_dict = yaml.safe_load(f)

    # Parse paths
    paths = PathsConfig(
        pdf_input_root=Path(config_dict["paths"]["pdf_input_root"]),
        csv_output_root=Path(config_dict["paths"]["csv_output_root"]),
        temp_images_dir=Path(config_dict["paths"]["temp_images_dir"]),
        review_dir=Path(config_dict["paths"]["review_dir"]),
        logs_dir=Path(config_dict["paths"]["logs_dir"]),
        checkpoints_dir=Path(config_dict["paths"]["checkpoints_dir"]),
    )

    # Parse preprocessing
    prep = config_dict["preprocessing"]
    preprocessing = PreprocessingConfig(
        target_dpi=prep["target_dpi"],
        grayscale=prep["grayscale"],
        adaptive_binarization=prep["adaptive_binarization"],
        noise_removal_method=prep["noise_removal_method"],
        median_kernel_size=prep["median_kernel_size"],
        skew_correction=prep["skew_correction"],
        skew_angle_threshold=prep["skew_angle_threshold"],
        contrast_enhancement=prep["contrast_enhancement"],
        clahe_clip_limit=prep["clahe_clip_limit"],
        clahe_tile_grid_size=tuple(prep["clahe_tile_grid_size"]),
        thinning=prep["thinning"],
        border_removal=prep["border_removal"],
        border_size=prep["border_size"],
    )

    # Parse Tesseract
    tess = config_dict["tesseract"]
    tesseract = TesseractConfig(
        language=tess["language"],
        psm=tess["psm"],
        oem=tess["oem"],
        config_string=tess["config_string"],
    )

    # Parse table extraction
    table_ext = config_dict["table_extraction"]
    table_extraction = TableExtractionConfig(
        extract_upper_table_only=table_ext["extract_upper_table_only"],
        upper_table_region_ratio=tuple(table_ext["upper_table_region_ratio"]),
    )

    # Parse PDF structure
    pdf_struct = config_dict["pdf_structure"]
    pdf_structure = PDFStructureConfig(
        years_single_page=pdf_struct["years_single_page"],
        years_two_page=pdf_struct["years_two_page"],
        page_mapping=pdf_struct["page_mapping"],
    )

    # Parse CSV output
    csv_out = config_dict["csv_output"]
    csv_output = CSVOutputConfig(
        separator=csv_out["separator"], encoding=csv_out["encoding"], na_rep=csv_out["na_rep"]
    )

    # Parse validation
    val = config_dict["validation"]
    validation = ValidationConfig(
        confidence_threshold=val["confidence_threshold"],
        expected_min_sectors=val["expected_min_sectors"],
        expected_columns_table1_range=tuple(val["expected_columns_table1_range"]),
        expected_columns_table2_range=tuple(val["expected_columns_table2_range"]),
    )

    # Parse logging
    log = config_dict["logging"]
    logging_config = LoggingConfig(level=log["level"], format=log["format"], file=log["file"])

    # Parse progress
    prog = config_dict["progress"]
    progress = ProgressConfig(
        checkpoint_file=prog["checkpoint_file"],
        save_intermediate_images=prog["save_intermediate_images"],
        auto_cleanup_temp=prog["auto_cleanup_temp"],
    )

    # Assemble complete settings
    settings = OCRSettings(
        paths=paths,
        preprocessing=preprocessing,
        tesseract=tesseract,
        table_extraction=table_extraction,
        pdf_structure=pdf_structure,
        csv_output=csv_output,
        validation=validation,
        logging=logging_config,
        progress=progress,
    )

    return settings


if __name__ == "__main__":
    # Test configuration loading
    try:
        settings = load_settings()
        print("✓ Configuration loaded successfully")
        print(f"  PDF input: {settings.paths.pdf_input_root}")
        print(f"  CSV output: {settings.paths.csv_output_root}")
        print(f"  Tesseract language: {settings.tesseract.language}")
        print(f"  Confidence threshold: {settings.validation.confidence_threshold}")
    except Exception as e:
        print(f"✗ Configuration loading failed: {e}")
