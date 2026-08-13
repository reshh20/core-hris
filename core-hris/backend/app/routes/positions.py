
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.position import Position
from app.models.employee import Employee
from app.schemas.position import PositionCreate, PositionUpdate, PositionResponse

router = APIRouter(prefix="/api/positions", tags=["Positions"])


@router.get(
    "",
    response_model=list[PositionResponse],
    summary="Get all positions",
    description="Retrieve all job positions in the organization.",
)
def get_positions(db: Session = Depends(get_db)):
    return db.query(Position).order_by(Position.title).all()


@router.post(
    "",
    response_model=PositionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new position",
)
def create_position(pos_data: PositionCreate, db: Session = Depends(get_db)):
    existing = db.query(Position).filter(Position.title == pos_data.title).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"success": False, "message": "Position title already exists", "field": "title"},
        )
    position = Position(title=pos_data.title, level=pos_data.level)
    db.add(position)
    db.commit()
    db.refresh(position)
    return position


@router.put(
    "/{position_id}",
    response_model=PositionResponse,
    summary="Update a position",
)
def update_position(
    position_id: int, pos_data: PositionUpdate, db: Session = Depends(get_db)
):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Position not found", "field": "id"},
        )

    update_dict = pos_data.model_dump(exclude_unset=True)

    if "title" in update_dict:
        existing = (
            db.query(Position)
            .filter(Position.title == update_dict["title"], Position.id != position_id)
            .first()
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={"success": False, "message": "Position title already exists", "field": "title"},
            )

    for key, value in update_dict.items():
        setattr(position, key, value)

    db.commit()
    db.refresh(position)
    return position


@router.delete(
    "/{position_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a position",
    description="Delete a position. Fails if employees hold this position.",
)
def delete_position(position_id: int, db: Session = Depends(get_db)):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"success": False, "message": "Position not found", "field": "id"},
        )

    employee_count = db.query(Employee).filter(Employee.position_id == position_id).count()
    if employee_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "message": f"Cannot delete position with {employee_count} employee(s). Reassign them first.",
                "field": "id",
            },
        )

    db.delete(position)
    db.commit()
