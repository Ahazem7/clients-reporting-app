import re
import pandas as pd
import logging
import json
from typing import List, Dict, Any, Optional, Set, Union

logger = logging.getLogger(__name__)

def deduplicate_fields(fields_str: Optional[str]) -> str:
    """Deduplicate fields from a comma-separated string
    
    Args:
        fields_str: Comma-separated string of fields
        
    Returns:
        str: Deduplicated and sorted fields string
    """
    if not fields_str:
        return ""
        
    # Split by comma and strip whitespace
    fields_list = [field.strip() for field in fields_str.split(',')]
    
    # Remove empty strings and duplicates, maintain order
    unique_fields = []
    seen = set()
    for field in fields_list:
        if field and field not in seen:
            unique_fields.append(field)
            seen.add(field)
            
    # Join back with commas
    return ', '.join(unique_fields)

def normalize_name(name: str) -> str:
    """Normalize a name by removing special characters and converting to lowercase
    
    Args:
        name: Name to normalize
        
    Returns:
        str: Normalized name
    """
    if not name:
        return ""
        
    # Convert to lowercase and replace special chars with spaces
    normalized = re.sub(r'[^a-zA-Z0-9]', ' ', name.lower())
    
    # Replace multiple spaces with a single space
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    
    return normalized

def parse_json_fields(json_str: Optional[str]) -> Dict[str, Any]:
    """Parse a JSON string into a dictionary
    
    Args:
        json_str: JSON string
        
    Returns:
        Dict[str, Any]: Parsed dictionary or empty dict if invalid
    """
    if not json_str:
        return {}
        
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        # Try to handle common formatting issues
        try:
            # Replace single quotes with double quotes
            fixed_json = json_str.replace("'", '"')
            return json.loads(fixed_json)
        except (json.JSONDecodeError, TypeError):
            return {}
            
def format_number(number: Union[int, float, None], default: str = "N/A") -> str:
    """Format a number with thousands separator
    
    Args:
        number: Number to format
        default: Default value if number is None
        
    Returns:
        str: Formatted number
    """
    if number is None:
        return default
        
    try:
        return f"{int(number):,}"
    except (ValueError, TypeError):
        try:
            return f"{float(number):,.2f}"
        except (ValueError, TypeError):
            return default
            
def get_unique_values(data_list: List[Dict[str, Any]], field_name: str) -> List[str]:
    """Get unique values for a field from a list of dictionaries
    
    Args:
        data_list: List of dictionaries
        field_name: Field name to extract unique values from
        
    Returns:
        List[str]: List of unique values
    """
    unique_values = set()
    
    for item in data_list:
        value = item.get(field_name)
        if value:
            if isinstance(value, str) and ',' in value:
                # Handle comma-separated values
                for val in value.split(','):
                    val = val.strip()
                    if val:
                        unique_values.add(val)
            else:
                unique_values.add(str(value))
                
    return sorted(list(unique_values))

def extract_fields(df: pd.DataFrame, column_name: str) -> List[str]:
    """Extract unique field values from a comma-separated column
    
    Args:
        df: DataFrame containing the data
        column_name: Name of the column containing comma-separated values
        
    Returns:
        List[str]: List of unique field values
    """
    if df.empty or column_name not in df.columns:
        return []
        
    # Combine all values, split by comma, and extract unique values
    combined = ", ".join(df[column_name].dropna().astype(str))
    field_parts = re.split(r'[,\s]+', combined)
    
    # Normalize and deduplicate
    unique_fields = set()
    for part in field_parts:
        clean_part = part.strip()
        if clean_part:
            unique_fields.add(clean_part)
            
    return sorted(list(unique_fields))
    
def clean_numeric_value(value: Any) -> int:
    """Clean and convert a value to integer
    
    Args:
        value: Value to convert
        
    Returns:
        int: Converted value
    """
    if pd.isna(value):
        return 0
        
    try:
        # Convert to string, remove non-numeric chars, and convert to int
        return int(re.sub(r'[^\d]', '', str(value)) or 0)
    except (ValueError, TypeError):
        return 0
        
def safe_get(dictionary: Dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get a value from a dictionary
    
    Args:
        dictionary: Dictionary to get value from
        key: Key to look up
        default: Default value if key doesn't exist
        
    Returns:
        Any: Value from dictionary or default
    """
    return dictionary.get(key, default)
    
def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names in a DataFrame
    
    Args:
        df: DataFrame to normalize
        
    Returns:
        pd.DataFrame: DataFrame with normalized column names
    """
    rename_map = {}
    for col in df.columns:
        # Convert to lowercase, replace spaces with underscores
        new_col = col.lower().replace(' ', '_')
        rename_map[col] = new_col
        
    return df.rename(columns=rename_map)
    
def ensure_required_columns(df: pd.DataFrame, required_columns: List[str]) -> bool:
    """Check if DataFrame has all required columns
    
    Args:
        df: DataFrame to check
        required_columns: List of required column names
        
    Returns:
        bool: True if all required columns are present
    """
    missing_columns = [col for col in required_columns if col not in df.columns]
    return len(missing_columns) == 0
    
def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> Dict[str, Any]:
    """Validate a DataFrame against required columns and return validation results
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        
    Returns:
        Dict[str, Any]: Validation results
    """
    results = {
        'is_valid': True,
        'errors': [],
        'warnings': []
    }
    
    # Check for empty DataFrame
    if df.empty:
        results['is_valid'] = False
        results['errors'].append("DataFrame is empty")
        return results
        
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        results['is_valid'] = False
        results['errors'].append(f"Missing required columns: {', '.join(missing_columns)}")
        
    # Check for missing values in required columns
    for col in [c for c in required_columns if c in df.columns]:
        null_count = df[col].isna().sum()
        if null_count > 0:
            results['warnings'].append(f"Column '{col}' has {null_count} missing values")
            
    return results 