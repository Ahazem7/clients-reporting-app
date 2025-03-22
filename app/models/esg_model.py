from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional
import json


@dataclass
class ESGData:
    """Data class for ESG records"""
    client: str
    fields: str
    data_type: Optional[str] = None
    data_source: Optional[str] = None
    sedol_count: Optional[int] = None
    isin_count: Optional[int] = None
    cusip_count: Optional[int] = None
    compliance: Optional[str] = None
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        # Use dataclasses.asdict and filter out None values
        data_dict = {k: v for k, v in asdict(self).items() if v is not None}
        return data_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ESGData':
        """Create ESGData instance from dictionary"""
        # Handle potential type conversions
        for field_name in ['sedol_count', 'isin_count', 'cusip_count', 'id']:
            if field_name in data and data[field_name] is not None:
                try:
                    data[field_name] = int(data[field_name])
                except (ValueError, TypeError):
                    data[field_name] = None
                    
        # Initialize with known fields
        return cls(
            id=data.get('id'),
            client=data.get('client', ''),
            fields=data.get('fields', ''),
            data_type=data.get('data_type'),
            data_source=data.get('data_source'),
            sedol_count=data.get('sedol_count'),
            isin_count=data.get('isin_count'),
            cusip_count=data.get('cusip_count'),
            compliance=data.get('compliance'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def is_valid(self) -> bool:
        """Check if the ESG data has required fields"""
        # Basic validation for required fields
        return bool(self.client and self.fields)
    
    def __str__(self) -> str:
        """String representation"""
        return f"ESGData(id={self.id}, client='{self.client}', fields='{self.fields}')"


@dataclass
class ESGAggregatedData:
    """Data class for aggregated ESG data"""
    client: str
    fields: str
    data_types: str
    data_sources: str
    total_sedol_count: int = 0
    total_isin_count: int = 0 
    total_cusip_count: int = 0
    compliance_status: str = ''
    record_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ESGAggregatedData':
        """Create ESGAggregatedData instance from dictionary"""
        # Handle potential type conversions
        for field_name in ['total_sedol_count', 'total_isin_count', 'total_cusip_count', 'record_count']:
            if field_name in data and data[field_name] is not None:
                try:
                    data[field_name] = int(data[field_name])
                except (ValueError, TypeError):
                    data[field_name] = 0
                    
        return cls(
            client=data.get('client', ''),
            fields=data.get('fields', ''),
            data_types=data.get('data_types', ''),
            data_sources=data.get('data_sources', ''),
            total_sedol_count=data.get('total_sedol_count', 0),
            total_isin_count=data.get('total_isin_count', 0),
            total_cusip_count=data.get('total_cusip_count', 0),
            compliance_status=data.get('compliance_status', ''),
            record_count=data.get('record_count', 0)
        ) 