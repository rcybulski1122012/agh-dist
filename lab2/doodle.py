import uuid
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class VoteBase(BaseModel):
    answer: str


class Vote(VoteBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class PollBase(BaseModel):
    question: str
    answers: list[str]


class Poll(PollBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    votes: dict[str, Vote] = {}


polls = {
    "1": Poll(
        id="1",
        question="What is your favorite color?",
        answers=["red", "green", "blue"],
        votes={"1": Vote(answer="red", id="1")},
    )
}


def get_requested_poll(poll_id: str) -> Poll:
    if poll_id not in polls:
        raise HTTPException(status_code=404, detail="Item not found")
    return polls[poll_id]


def get_requested_vote(
    poll: Annotated[Poll, Depends(get_requested_poll)], vote_id: str
) -> Vote:
    if vote_id not in poll.votes:
        raise HTTPException(status_code=404, detail="Item not found")
    return poll.votes[vote_id]


@app.get("/polls/", response_model=list[PollBase])
async def get_polls() -> list[Poll]:
    return list(polls.values())


@app.post("/polls/", response_model=PollBase)
async def create_poll(poll: PollBase) -> Poll:
    new_poll = Poll(
        question=poll.question,
        answers=dict.fromkeys(poll.answers, 0),
    )
    polls[new_poll.id] = new_poll
    return new_poll


@app.get("/polls/{poll_id}", response_model=PollBase)
async def get_poll(poll: Annotated[Poll, Depends(get_requested_poll)]) -> Poll:
    return poll


@app.get("/polls/{poll_id}")
async def update_vote(
    updated_poll: PollBase, poll: Annotated[Poll, Depends(get_requested_poll)]
) -> Poll:
    poll.question = updated_poll.question
    poll.answers = updated_poll.answers
    return poll


@app.delete("/polls/{poll_id}", response_model=PollBase)
async def delete_poll(poll: Annotated[Poll, Depends(get_requested_poll)]) -> Poll:
    return polls.pop(poll.id)


@app.get("/polls/{poll_id}/vote")
async def get_votes(poll: Annotated[Poll, Depends(get_requested_poll)]) -> list[Vote]:
    return list(poll.votes.values())


@app.post("/polls/{poll_id}/vote")
async def create_vote(
    vote: VoteBase, poll: Annotated[Poll, Depends(get_requested_poll)]
) -> Vote:
    if vote.answer not in poll.answers:
        raise HTTPException(status_code=400, detail="Invalid answer")

    new_vote = Vote(answer=vote.answer)
    poll.votes[new_vote.id] = new_vote
    return new_vote


@app.get("/polls/{poll_id}/vote/{vote_id}")
async def get_vote(vote: Annotated[Vote, Depends(get_requested_vote)]) -> Vote:
    return vote


@app.put("/polls/{poll_id}/vote/{vote_id}")
async def update_vote(
    updated_vote: VoteBase,
    vote: Annotated[Vote, Depends(get_requested_vote)],
    poll: Annotated[Poll, Depends(get_requested_poll)],
) -> Vote:
    if updated_vote.answer not in poll.answers:
        raise HTTPException(status_code=400, detail="Invalid answer")

    vote.answer = updated_vote.answer
    return vote
