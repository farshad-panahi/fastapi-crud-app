from fastapi import APIRouter, Body, HTTPException, status, Depends
from typing import List
from sqlmodel import select

from db.connection import get_session
from models.events import Event, UpdateEvent


event_router = APIRouter(
	tags=['Events']
)

events = []


@event_router.post('/new')
async def create(data: Event, session=Depends(get_session)):
	session.add(data)
	session.commit()
	session.refresh(data)

	return {
		'message': 'Event created successfully'
	}


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)):
	_events = session.exec(select(Event)).all()
	return _events


@event_router.get('/{_id}', response_model=Event)
async def retrieve(_id: int, session=Depends(get_session)):
	event = session.get(Event, _id)
	if event:
		return event

	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail='Event not found'
	)


@event_router.put('edit/{_di}')
async def update(_id: int, new_data: UpdateEvent ,session=Depends(get_session)):
	event = session.get(Event, _id)
	if event:
		event_data = new_data.dict(exclude_unset=True)
		for k, v in event_data.items():
			setattr(event, k, v)

		session.add(event)
		session.commit()
		session.refresh(event)

		return event
	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail='item not found'
	)


@event_router.delete('/delete/{_id}')
async def delete_event(_id: int, session=Depends(get_session)) -> dict:
	event = session.get(Event, _id)
	if event:
		session.delete(event)
		session.commit()
		return {
			'message': 'This event removed'
		}
	raise HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail='item not found'
	)
