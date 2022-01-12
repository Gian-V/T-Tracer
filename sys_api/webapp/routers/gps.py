import mariadb
from fastapi import APIRouter, Depends, Response, Query, status

from webapp.utilities.function import get_db, load_gps
from webapp.utilities import private_key

from typing import Dict, Optional

router = APIRouter(
    prefix="/gps",
    tags=["gps"]
)


@router.get('/', response_model=Dict[str, bool], status_code=status.HTTP_202_ACCEPTED)
def gps_request(
        response: Response,
        q: Optional[bytes] = Query(None),
        cursor: mariadb.connection.cursor = Depends(get_db)
):
    try:
        if q is None:
            raise ValueError("You must insert a value")
        load_gps(cursor, private_key.decrypt(q.replace(b" ", b"+")))
    except (ValueError, TypeError):
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {'success': False}
    return {'success': True}
