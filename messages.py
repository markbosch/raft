# messages.py

from dataclasses import dataclass

@dataclass
class AppendEntries:
    term: int
    leaderId: int
    prevLogIndex: int
    prevLogTerm: int
    entries: []
    leaderCommit: int

@dataclass
class AppendEntriesResult:
    term: int
    success: bool
