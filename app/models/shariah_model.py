from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional
import json

@dataclass
class ShariahData:
    """Data class for Shariah DataFeed records"""
    client: str
    current_source: Optional[str] = None
    after_migration: Optional[str] = None
    delivery_name: Optional[str] = None
    fields: Optional[str] = None
    universe: Optional[str] = None
    universe_count: Optional[int] = None
    frequency: Optional[str] = None
    migration_plan: Optional[str] = None
    sedol_count: Optional[int] = None
    isin_count: Optional[int] = None
    cusip_count: Optional[int] = None
    id: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        # Use dataclasses.asdict and filter out None values
        data_dict = {k: v for k, v in asdict(self).items() if v is not None}
        return data_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ShariahData':
        """Create ShariahData instance from dictionary"""
        # Handle potential type conversions
        for field_name in ['universe_count', 'sedol_count', 'isin_count', 'cusip_count', 'id']:
            if field_name in data and data[field_name] is not None:
                try:
                    data[field_name] = int(data[field_name])
                except (ValueError, TypeError):
                    data[field_name] = None
                    
        # Initialize with known fields
        return cls(
            id=data.get('id'),
            client=data.get('client', ''),
            current_source=data.get('current_source'),
            after_migration=data.get('after_migration'),
            delivery_name=data.get('delivery_name'),
            fields=data.get('fields'),
            universe=data.get('universe'),
            universe_count=data.get('universe_count'),
            frequency=data.get('frequency'),
            migration_plan=data.get('migration_plan'),
            sedol_count=data.get('sedol_count'),
            isin_count=data.get('isin_count'),
            cusip_count=data.get('cusip_count'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    def is_valid(self) -> bool:
        """Check if the Shariah data has required fields"""
        # Basic validation for required fields (only client is mandatory)
        return bool(self.client)
    
    def __str__(self) -> str:
        """String representation"""
        return f"ShariahData(id={self.id}, client='{self.client}', universe='{self.universe or ''}')"

@dataclass
class ShariahAggregatedData:
    """Data class for aggregated Shariah data"""
    client: str
    sources: str = ''
    fields: str = ''
    universe: str = ''
    total_universe_count: int = 0
    total_sedol_count: int = 0
    total_isin_count: int = 0
    total_cusip_count: int = 0
    frequencies: str = ''
    record_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ShariahAggregatedData':
        """Create ShariahAggregatedData instance from dictionary"""
        # Handle potential type conversions
        for field_name in ['total_universe_count', 'total_sedol_count', 'total_isin_count', 'total_cusip_count', 'record_count']:
            if field_name in data and data[field_name] is not None:
                try:
                    data[field_name] = int(data[field_name])
                except (ValueError, TypeError):
                    data[field_name] = 0
                    
        return cls(
            client=data.get('client', ''),
            sources=data.get('sources', ''),
            fields=data.get('fields', ''),
            universe=data.get('universe', ''),
            total_universe_count=data.get('total_universe_count', 0),
            total_sedol_count=data.get('total_sedol_count', 0),
            total_isin_count=data.get('total_isin_count', 0),
            total_cusip_count=data.get('total_cusip_count', 0),
            frequencies=data.get('frequencies', ''),
            record_count=data.get('record_count', 0)
        ) 