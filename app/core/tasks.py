from app.core.celery_app import app
from app.crud import user
from app.db.session import SessionLocal
from app.schemas.transaction import TransactionType


@app.task
def create_transaction(user_id: int, transaction_amount: int, transaction_type: str):
    with SessionLocal() as db:
        current_user = user.get(db, user_id)

        # In the time interval between the execution of the task,
        # the money can already be withdrawn, so here is this check
        if transaction_type == TransactionType.WITHDRAW.value and transaction_amount > current_user.balance:
            # TODO: Добавить оповещение о том, что недостаточно денег
            print("Мало денег на балансе")
            return

        user.create_transaction(db, current_user, transaction_amount, transaction_type)
        # TODO: Добавить оповещение о том, что транзакция выполнилась
        print("Транзакция успешно выполнилась")
