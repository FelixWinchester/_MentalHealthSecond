from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, delete
from sqlalchemy.orm import contains_eager, joinedload
from typing import List
from database import get_db
from auth import get_current_user # Замени на свой импорт
from models import (
    ThreadDB, CommentDB, ThreadVote, CommentVote, 
    UserDB, ThreadCreate, ThreadOut, CommentCreate, 
    CommentOut, VoteCreate, thread_access
)

router = APIRouter(prefix="/forum", tags=["Forum"])

@router.post("/threads", response_model=ThreadOut)
async def create_thread(data: ThreadCreate, db: AsyncSession = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    new_thread = ThreadDB(
        title=data.title,
        content=data.content,
        is_public=data.is_public,
        is_anonymous=data.is_anonymous,
        author_id=current_user.id
    )
    
    if not data.is_public and data.allowed_user_ids:
        # Добавляем доступ конкретным пользователям
        result = await db.execute(select(UserDB).where(UserDB.id.in_(data.allowed_user_ids)))
        users = result.scalars().all()
        new_thread.allowed_users.extend(users)

    db.add(new_thread)
    await db.commit()
    await db.refresh(new_thread)
    return new_thread

@router.get("/threads", response_model=List[ThreadOut])
async def get_threads(db: AsyncSession = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    # 1. Подзапрос для рейтинга
    rating_subquery = (
        select(func.coalesce(func.sum(ThreadVote.value), 0))
        .where(ThreadVote.thread_id == ThreadDB.id)
        .scalar_subquery()
    )

    # 2. Подзапрос для количества ответов (комментариев)
    comments_count_subquery = (
        select(func.count(CommentDB.id))
        .where(CommentDB.thread_id == ThreadDB.id)
        .scalar_subquery()
    )

    # 3. Подзапрос для голоса текущего пользователя
    user_vote_sub = (
        select(ThreadVote.value)
        .where(ThreadVote.thread_id == ThreadDB.id, ThreadVote.user_id == current_user.id)
        .scalar_subquery()
    )

    query = (
        select(
            ThreadDB,
            rating_subquery.label("rating_sum"),
            comments_count_subquery.label("comments_count"),
            user_vote_sub.label("user_vote")
        )
        .outerjoin(ThreadDB.author)
        .options(contains_eager(ThreadDB.author))
        .order_by(ThreadDB.created_at.desc())
    )

    result = await db.execute(query)
    rows = result.all()

    output = []
    for thread, rating_sum, comments_count, user_vote in rows:
        t_out = ThreadOut.from_orm(thread)
        t_out.rating = int(rating_sum or 0)
        t_out.comments_count = int(comments_count or 0) # <--- Передаем количество
        t_out.user_vote = user_vote or 0
        
        # Логика анонимности
        if thread.is_anonymous and thread.author_id != current_user.id:
            t_out.author_name = "Аноним"
        else:
            t_out.author_name = thread.author.username if thread.author else "Пользователь"
            
        output.append(t_out)
    return output

@router.post("/threads/{thread_id}/vote")
async def vote_thread(
    thread_id: int, 
    vote_data: VoteCreate, # Принимает JSON {"value": 1}
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    if vote_data.value not in [1, -1]:
        raise HTTPException(status_code=400, detail="Значение должно быть 1 или -1")

    # Ищем существующий голос
    query = select(ThreadVote).where(
        ThreadVote.thread_id == thread_id, 
        ThreadVote.user_id == current_user.id
    )
    result = await db.execute(query)
    existing_vote = result.scalars().first()

    if existing_vote:
        if existing_vote.value == vote_data.value:
            # Отмена голоса (повторное нажатие на ту же кнопку)
            await db.delete(existing_vote)
            user_current_vote = 0
        else:
            # Смена голоса с +1 на -1 или наоборот
            existing_vote.value = vote_data.value
            user_current_vote = vote_data.value
    else:
        # Новый голос
        new_vote = ThreadVote(thread_id=thread_id, user_id=current_user.id, value=vote_data.value)
        db.add(new_vote)
        user_current_vote = vote_data.value

    await db.commit()

    # Считаем актуальный СУММАРНЫЙ рейтинг
    rating_query = select(func.coalesce(func.sum(ThreadVote.value), 0)).where(ThreadVote.thread_id == thread_id)
    rating_res = await db.execute(rating_query)
    total_rating = rating_res.scalar()

    return {"total_rating": total_rating, "user_vote": user_current_vote}

@router.post("/threads/{thread_id}/comments", response_model=CommentOut)
async def create_comment(thread_id: int, data: CommentCreate, db: AsyncSession = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    comment = CommentDB(
        thread_id=thread_id,
        author_id=current_user.id,
        content=data.content,
        is_anonymous=data.is_anonymous
    )
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


@router.get("/threads/{thread_id}", response_model=ThreadOut)
async def get_thread(thread_id: int, db: AsyncSession = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    # Подзапрос для получения голоса именно текущего пользователя
    user_vote_sub = (
        select(ThreadVote.value)
        .where(ThreadVote.thread_id == ThreadDB.id, ThreadVote.user_id == current_user.id)
        .correlate(ThreadDB)
        .as_scalar()
        .label("user_vote")
    )

    query = (
        select(
            ThreadDB,
            func.coalesce(func.sum(ThreadVote.value), 0).label("rating_sum"),
            user_vote_sub
        )
        .outerjoin(ThreadVote)
        .outerjoin(ThreadDB.author) 
        .options(contains_eager(ThreadDB.author))
        .where(ThreadDB.id == thread_id)
        .group_by(
            ThreadDB.id, 
            UserDB.id  
        )
    )

    result = await db.execute(query)
    row = result.first()

    if not row:
        raise HTTPException(404, "Thread not found")

    thread, rating_sum, user_vote = row
    
    # Формируем ответ с добавлением вычисленных полей
    t_out = ThreadOut.from_orm(thread)
    t_out.rating = int(rating_sum) 
    t_out.user_vote = user_vote or 0 
    
    # Логика анонимности
    if thread.is_anonymous and thread.author_id != current_user.id:
        t_out.author_name = "Аноним"
    else:
        t_out.author_name = thread.author.username if thread.author else "Пользователь"

    return t_out

@router.get("/threads/{thread_id}/comments", response_model=List[CommentOut])
async def get_comments(
    thread_id: int, 
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    query = (
        select(CommentDB)
        .options(joinedload(CommentDB.author)) 
        .where(CommentDB.thread_id == thread_id)
        .order_by(CommentDB.created_at.asc())
    )
    
    result = await db.execute(query)
    comments = result.scalars().all()

    output = []
    for comment in comments:
        c_out = CommentOut.from_orm(comment)
        
        # ЛОГИКА АНОНИМНОСТИ
        if comment.is_anonymous:

            
            if comment.author_id != current_user.id:
                c_out.author_name = "Аноним"
            else:
                c_out.author_name = f"{comment.author.username} (Вы)"
        else:
            c_out.author_name = comment.author.username if comment.author else "Пользователь"
            
        output.append(c_out)
        
    return output