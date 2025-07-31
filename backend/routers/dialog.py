import random
from urllib import request
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, update, select  # Import select here
# from achievements import AchievementService
from database import AsyncSessionLocal, get_db, create_tables
from models import DAILY_QUESTIONS, Achievement, AchievementDB, DialogAnswer, DialogMessage, MoodType, MoodViewHistoryOut, UserAchievementDB, UserAchievementOut, UserCreate, User, Token, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory
from database import get_db, create_tables
from models import MoodViewHistoryOut, UserCreate, User, Token, UserDB, MoodEntry, MoodEntryCreate, MoodEntryOut, MoodViewHistory, MoodChartPoint, MoodMap
from auth import get_password_hash, create_access_token, verify_password, get_current_user
from datetime import datetime, timedelta
from typing import Optional, List
import logging
from fastapi.middleware.cors import CORSMiddleware

router = APIRouter(prefix="/dialog", tags=["dialog"])

@router.get("/today")
async def get_daily_question(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    today = datetime.utcnow().date()

    result = await db.execute(
        select(DialogMessage)
        .where(DialogMessage.user_id == current_user.id)
        .where(DialogMessage.sender == "system")
        .where(func.date(DialogMessage.timestamp) == today)
    )
    message = result.scalar()

    if message:
        return {"question": message.text}

    question = random.choice(DAILY_QUESTIONS)
    new_msg = DialogMessage(user_id=current_user.id, sender="system", text=question)
    db.add(new_msg)
    await db.commit()
    await db.refresh(new_msg)

    return {"question": new_msg.text}

@router.post("/answer")
async def post_or_update_answer(
    answer_data: DialogAnswer,
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    today = datetime.utcnow().date()

    result = await db.execute(
        select(DialogMessage)
        .where(DialogMessage.user_id == current_user.id)
        .where(DialogMessage.sender == "user")
        .where(func.date(DialogMessage.timestamp) == today)
    )
    existing_answer = result.scalar()

    if existing_answer:
        await db.execute(
            update(DialogMessage)
            .where(DialogMessage.id == existing_answer.id)
            .values(text=answer_data.answer, timestamp=datetime.utcnow())
        )
        await db.commit()
        return {"message": "Answer updated"}
    else:
        new_msg = DialogMessage(
            user_id=current_user.id,
            sender="user",
            text=answer_data.answer
        )
        db.add(new_msg)
        await db.commit()
        await db.refresh(new_msg)
        return {"message": "Answer saved"}

@router.get("/history")
async def get_dialog_history(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    result = await db.execute(
        select(DialogMessage)
        .where(DialogMessage.user_id == current_user.id)
        .order_by(DialogMessage.timestamp)
    )
    messages = result.scalars().all()

    return [
        {
            "sender": msg.sender,
            "text": msg.text,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]

@router.get("/today/answer")
async def get_today_answer(
    db: AsyncSession = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    today = datetime.utcnow().date()

    result = await db.execute(
        select(DialogMessage)
        .where(DialogMessage.user_id == current_user.id)
        .where(DialogMessage.sender == "user")
        .where(func.date(DialogMessage.timestamp) == today)
    )
    message = result.scalar()

    if message:
        return {"answer": message.text}
    else:
        return {"answer": None}


