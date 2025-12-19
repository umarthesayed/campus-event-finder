from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, List
from pathlib import Path
import datetime
from fastapi.middleware.cors import CORSMiddleware


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = ""
    category: Optional[str] = "General"
    date: str  
    time: Optional[str] = ""
    location: Optional[str] = ""
    organizer: Optional[str] = ""
    created_at: Optional[str] = ""
    updated_at: Optional[str] = ""


app = FastAPI(title="Campus Event Finder API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = "events.db"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_sample_events() -> List[Event]:
    now = datetime.datetime.utcnow().isoformat()
    return [
        Event(
            title="AI & ML Workshop",
            description="Hands-on workshop: Intro to Python for ML, basics of TensorFlow and scikit-learn.",
            category="Tech",
            date="2025-12-10",
            time="14:00",
            location="Engineering Lab A",
            organizer="Computer Science Club",
            created_at=now,
            updated_at=now
        ),
        Event(
<<<<<<< HEAD
            title="Basketball Cup Finals",
=======
            title="Basketball",
>>>>>>> 9c41de3800a720969d29b00058feab05ca18e63f
            description="Basketball CUP to play, score and win good prizes",
            category="Sports",
            date="2025-12-12",
            time="14:00",
            location="Basketball court",
            organizer="NU CLUB",
            created_at=now,
            updated_at=now
        ),
        Event(
            title="Football Friendly",
            description="Inter-faculty friendly match. All students welcome to attend or play. scoring GOALS",
            category="Sports",
            date="2025-03-12",
            time="17:00",
            location="Main Stadium",
            organizer="Sports Committee",
            created_at=now,
            updated_at=now
        ),
        Event(
            title="Startup Pitch Night",
            description="Student startups present their ideas to a panel of judges. Food & networking.",
            category="Social",
            date="2025-03-15",
            time="19:00",
            location="Auditorium",
            organizer="Entrepreneurship Club",
            created_at=now,
            updated_at=now
        ),
        Event(
            title="Robotics Club Meeting",
            description="Weekly meeting: build time and demo of last week's project.",
            category="Tech",
            date="2025-03-09",
            time="16:00",
            location="Robotics Lab",
            organizer="Robotics Club",
            created_at=now,
            updated_at=now
        ),
    ]

@app.on_event("startup")
def on_startup():
    
    create_db_and_tables()
    with Session(engine) as session:
        statement = select(Event)
        results = session.exec(statement).all()
        if len(results) == 0:
            for ev in get_sample_events():
                session.add(ev)
            session.commit()


@app.get("/api/events", response_model=List[Event])
def list_events():
    with Session(engine) as session:
        statement = select(Event).order_by(Event.date, Event.time)
        events = session.exec(statement).all()
        return events

@app.get("/api/events/{event_id}", response_model=Event)
def get_event(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event


@app.post("/api/events", response_model=Event)
def create_event(
    title: str = Form(...),
    description: str = Form(""),
    category: str = Form("General"),
    date: str = Form(...),
    time: str = Form(""),
    location: str = Form(""),
    organizer: str = Form("")
):
    now = datetime.datetime.utcnow().isoformat()
    ev = Event(
        title=title,
        description=description,
        category=category,
        date=date,
        time=time,
        location=location,
        organizer=organizer,
        created_at=now,
        updated_at=now
    )
    with Session(engine) as session:
        session.add(ev)
        session.commit()
        session.refresh(ev)
        return ev


HERE = Path(__file__).parent
static_dir = HERE / "static"
if not static_dir.exists():
    static_dir.mkdir(exist_ok=True)

app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
