import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlmodel import create_engine, Session, select
from .models import User, Message, init_db

app = FastAPI()

# inicializa o banco de dados
init_db()

# Dependência para obter a sessão do banco de dados
def get_session():
    engine = create_engine('sqlite:///.test.db')
    with Session(engine) as session:
        yield session
        

@app.post('/users/')
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get('/users/')
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users


@app.post("/auth/login")
def login(username: str, password: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == username)).first()
    if user and user.password == password:
        return {"user_id": user.id}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/users/{user_id}/conversations/")
def get_conversations(user_id: int, session: Session = Depends(get_session)):
    messages = session.exec(select(Message).where(Message.user_id == user_id)).all()
    return messages

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            new_message = Message(**message_data, user_id=user_id)
            with Session(create_engine("sqlite:///./test.db")) as session:
                session.add(new_message)
                session.commit()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        pass
    