from sqlalchemy import CTE, Select, Subquery, case, func, select
from sqlalchemy.dialects import postgresql

from src.core.enum.score.operation import ScoreOperationEnum
from src.data.models.group.group import GroupModel, GroupScoreModel
from src.data.models.user.user import UserModel, UserScoreModel

id_attr = "id"
attr_map = {"user_score": ("user_id", UserModel), "group_score": ("group_id", GroupModel)}


def showq(stmt):
    print(stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))


def build_score_table_subq(model: type[UserScoreModel] | type[GroupScoreModel]) -> Subquery:
    attr, entity_model = attr_map[model.__tablename__]
    score_model_id_field = getattr(model, attr).label(attr)
    entity_model_id_field = getattr(entity_model, id_attr).label(attr)
    subquery = (
        select(
            score_model_id_field,
            func.sum(
                case(
                    (
                        model.operation == ScoreOperationEnum.MINUS,
                        model.value * -1,
                    ),
                    else_=model.value,
                ),
            ).label("score"),
        )
        .group_by(score_model_id_field)
        .subquery("score_raw_table")
    )
    stmt = (
        select(
            entity_model_id_field,
            func.coalesce(subquery.c.score, 0).label("score"),
        )
        .outerjoin(
            subquery,
            entity_model_id_field == getattr(subquery.c, attr),
        )
        .order_by(subquery.c.score.desc())
        .subquery("score_table")
    )
    return stmt


def build_score_table_stmt(model: type[UserScoreModel] | type[GroupScoreModel], target_id: str | int) -> Select:
    attr, _ = attr_map[model.__tablename__]
    label_id = attr
    subq = build_score_table_subq(model=model)
    subq_id_attr = getattr(subq.c, attr)
    stmt = (
        select(
            subq_id_attr.label(label_id),
            subq.c.score.label("score"),
        )
        .select_from(subq)
        .where(subq_id_attr == target_id)
    )
    return stmt


def build_rating_table_cte(model: type[UserScoreModel] | type[GroupScoreModel]) -> CTE:
    attr, _ = attr_map[model.__tablename__]
    label_id = attr
    subq = build_score_table_subq(model=model)
    subq_id_attr = getattr(subq.c, attr)
    stmt = select(
        subq_id_attr.label(label_id),
        subq.c.score.label("score"),
        func.row_number().over(order_by=subq.c.score.desc()).label("position"),
    ).cte("rating_table_cte")
    return stmt


def build_rating_table_stmt(
    model: type[UserScoreModel] | type[GroupScoreModel],
    target_id: str | int | None = None,
    with_max_bound: bool = False,
    lbound: int | None = None,
    ubound: int | None = None,
    limit: int | None = None,
) -> Select:
    attr, _ = attr_map[model.__tablename__]
    rating_cte = build_rating_table_cte(model=model)
    cte_id_attr = getattr(rating_cte.c, attr)
    cte_position_attr = rating_cte.c.position
    columns = [
        cte_id_attr.label(attr),
        rating_cte.c.score.label("score"),
        cte_position_attr.label("position"),
    ]
    if with_max_bound:
        columns.append(select(func.max(cte_position_attr)).label("max_position"))
    conditions = []
    if target_id is not None:
        conditions.append(cte_id_attr == target_id)
    if lbound is not None:
        conditions.append(cte_position_attr >= lbound)
    if ubound is not None:
        conditions.append(cte_position_attr <= ubound)
    stmt = select(*columns).select_from(rating_cte).where(*conditions)
    if limit is not None:
        stmt = stmt.limit(limit)
    return stmt
