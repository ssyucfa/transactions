from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core import tasks
from app.models.user import User
from app.schemas.transaction import Transaction, TransactionType

router = APIRouter()


@router.post("/", status_code=201)
def create_transaction(
    transaction: Transaction,
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user),
):
    if transaction.type == TransactionType.WITHDRAW and transaction.amount > user.balance:
        raise HTTPException(
            status_code=400,
            detail=f"You can't withdraw that much because you don't have enough money on your balance."
                   f" Balance: {user.balance}"
        )

    tasks.create_transaction.delay(user.id, transaction.amount, transaction.type.value)

    return {"detail": "The transaction is being created, wait."}
