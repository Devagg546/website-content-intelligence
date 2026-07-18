"""
Inventory routes — Content inventory dashboard data.
"""

from fastapi import APIRouter, Depends

from app.models.inventory import InventoryResponse
from app.api.dependencies import get_db
from app.services.inventory_service import InventoryService

router = APIRouter()


@router.get("", response_model=InventoryResponse)
async def get_inventory(db=Depends(get_db)):
    """
    Generate content inventory report with statistics.
    """
    service = InventoryService()
    return service.generate_report(db)