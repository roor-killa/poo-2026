"""
Router /admin — Modification directe des données (mots, définitions, corpus, expressions)

Tous les endpoints requièrent X-Api-Key.
Destiné à l'interface d'administration du frontend.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..dependencies import require_api_key
from ..models.models import Corpus, Definition, Expression, Mot
from ..schemas.schemas import (
    CorpusOut,
    CorpusUpdate,
    DefinitionUpdate,
    DefinitionWithId,
    ExpressionOut,
    ExpressionUpdate,
    MotDetail,
    MotUpdate,
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_api_key)],
)


# ===========================================================================
# Mots
# ===========================================================================

@router.put(
    "/mots/{mot_id}",
    response_model=MotDetail,
    summary="Modifier un mot 🔒",
)
def update_mot(mot_id: int, body: MotUpdate, db: Session = Depends(get_db)) -> MotDetail:
    mot = db.get(Mot, mot_id)
    if not mot:
        raise HTTPException(status_code=404, detail=f"Mot introuvable (id={mot_id})")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(mot, field, value)
    db.commit()
    db.refresh(mot)
    mot = (
        db.query(Mot)
        .options(joinedload(Mot.traductions), joinedload(Mot.definitions), joinedload(Mot.source))
        .filter(Mot.id == mot_id)
        .first()
    )
    return MotDetail.from_orm_mot(mot)


@router.delete(
    "/mots/{mot_id}",
    status_code=204,
    summary="Supprimer un mot 🔒",
)
def delete_mot(mot_id: int, db: Session = Depends(get_db)) -> None:
    mot = db.get(Mot, mot_id)
    if not mot:
        raise HTTPException(status_code=404, detail=f"Mot introuvable (id={mot_id})")
    db.delete(mot)
    db.commit()


# ===========================================================================
# Définitions
# ===========================================================================

@router.get(
    "/mots/{mot_id}/definitions",
    response_model=List[DefinitionWithId],
    summary="Liste des définitions d'un mot avec leurs IDs 🔒",
)
def list_definitions(mot_id: int, db: Session = Depends(get_db)) -> List[DefinitionWithId]:
    mot = db.get(Mot, mot_id)
    if not mot:
        raise HTTPException(status_code=404, detail=f"Mot introuvable (id={mot_id})")
    defs = db.query(Definition).filter(Definition.mot_id == mot_id).all()
    return [DefinitionWithId(id=d.id, definition=d.definition, exemple=d.exemple) for d in defs]


@router.put(
    "/mots/{mot_id}/definitions/{def_id}",
    response_model=DefinitionWithId,
    summary="Modifier une définition 🔒",
)
def update_definition(
    mot_id: int, def_id: int, body: DefinitionUpdate, db: Session = Depends(get_db)
) -> DefinitionWithId:
    d = (
        db.query(Definition)
        .filter(Definition.id == def_id, Definition.mot_id == mot_id)
        .first()
    )
    if not d:
        raise HTTPException(status_code=404, detail=f"Définition introuvable (id={def_id})")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(d, field, value)
    db.commit()
    db.refresh(d)
    return DefinitionWithId(id=d.id, definition=d.definition, exemple=d.exemple)


@router.delete(
    "/mots/{mot_id}/definitions/{def_id}",
    status_code=204,
    summary="Supprimer une définition 🔒",
)
def delete_definition(mot_id: int, def_id: int, db: Session = Depends(get_db)) -> None:
    d = (
        db.query(Definition)
        .filter(Definition.id == def_id, Definition.mot_id == mot_id)
        .first()
    )
    if not d:
        raise HTTPException(status_code=404, detail=f"Définition introuvable (id={def_id})")
    db.delete(d)
    db.commit()


# ===========================================================================
# Corpus
# ===========================================================================

@router.put(
    "/corpus/{corpus_id}",
    response_model=CorpusOut,
    summary="Modifier une entrée corpus 🔒",
)
def update_corpus(corpus_id: int, body: CorpusUpdate, db: Session = Depends(get_db)) -> CorpusOut:
    c = db.get(Corpus, corpus_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Entrée corpus introuvable (id={corpus_id})")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    db.commit()
    db.refresh(c)
    return CorpusOut.from_orm_corpus(c)


@router.delete(
    "/corpus/{corpus_id}",
    status_code=204,
    summary="Supprimer une entrée corpus 🔒",
)
def delete_corpus(corpus_id: int, db: Session = Depends(get_db)) -> None:
    c = db.get(Corpus, corpus_id)
    if not c:
        raise HTTPException(status_code=404, detail=f"Entrée corpus introuvable (id={corpus_id})")
    db.delete(c)
    db.commit()


# ===========================================================================
# Expressions
# ===========================================================================

@router.put(
    "/expressions/{expr_id}",
    response_model=ExpressionOut,
    summary="Modifier une expression 🔒",
)
def update_expression(
    expr_id: int, body: ExpressionUpdate, db: Session = Depends(get_db)
) -> ExpressionOut:
    e = db.get(Expression, expr_id)
    if not e:
        raise HTTPException(status_code=404, detail=f"Expression introuvable (id={expr_id})")
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(e, field, value)
    db.commit()
    db.refresh(e)
    return ExpressionOut.from_orm_expr(e)


@router.delete(
    "/expressions/{expr_id}",
    status_code=204,
    summary="Supprimer une expression 🔒",
)
def delete_expression(expr_id: int, db: Session = Depends(get_db)) -> None:
    e = db.get(Expression, expr_id)
    if not e:
        raise HTTPException(status_code=404, detail=f"Expression introuvable (id={expr_id})")
    db.delete(e)
    db.commit()
