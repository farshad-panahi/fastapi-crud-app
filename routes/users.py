from fastapi import APIRouter, HTTPException, status

from models.users import UserSignIn, NewUser


user_router = APIRouter(
	tags=['User'],
)

users = {}


@user_router.post('/signup')
async def sign_user_up(data: NewUser) -> dict:
	if data.email in users:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail='email already in use'
		)
	users[data.email] = data
	return {
		'message': 'user successfully registered'
	}


@user_router.post('/signin')
async def sign_user_in(user: UserSignIn) -> dict:
	if user.email not in users:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='user not found'
		)
	if users[user.email].password != user.password:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail='password mismatch'
		)
	return {
		'message': 'User signed in successfully'
	}




