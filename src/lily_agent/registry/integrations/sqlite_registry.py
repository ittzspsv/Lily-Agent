from typing import List, Optional
from ..agent_registry import AgentInfo, AgentRegistry

import sqlite3
import uuid


class SQLiteRegistry(AgentRegistry):
    def __init__(self, path: Optional[str] = None) -> None:

        self.path: Optional[str] = path or ".configs/agent_registry.db"

        super().__init__(self.path)

        """ Create a database connection """
        self.db: sqlite3.Connection = sqlite3.connect(self.path)

        """ Default Schema Initialization """
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS agent_registry (
                agent_key TEXT PRIMARY KEY,       
                agent_id TEXT UNIQUE NOT NULL,     
                name TEXT NOT NULL,                
                role TEXT NOT NULL,                
                prompt TEXT NOT NULL,              
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        
        self.db.commit()

    def register(self, agent_key: str, name: str, role: str, prompt: str) -> str:
        """ Check if role exists already """
        cursor = self.db.execute("""SELECT agent_id FROM agent_registry WHERE agent_key = ?""", (agent_key,))
        row = cursor.fetchone()

        if row:
            agent_id = row[0]

            """Update Existing Agent"""
            self.db.execute("""
                UPDATE agent_registry
                SET 
                    name = ?, role = ?, prompt = ?, updated_at = CURRENT_TIMESTAMP
                WHERE agent_key = ?
                """, 
        (
            name,
            role,
            prompt,
            agent_key
        ))
            
        else:
            agent_id = f"agent_{uuid.uuid4().hex}"

            self.db.execute("""
                INSERT INTO agent_registry 
                (
                    agent_key, agent_id, name, role, prompt
                ) 
                VALUES (?, ?, ?, ?, ?)
            """, 
            (
                agent_key,
                agent_id,
                name,
                role,
                prompt
            ))

        self.db.commit()
        return agent_id
    
    def get(self, agent_key: str) -> AgentInfo | None:
        row = self.db.execute("""
            SELECT agent_key, agent_id, name, role, prompt
            FROM agent_registry
            WHERE agent_key = ?
        """, (agent_key,)).fetchone()

        if not row:
            return None

        return AgentInfo(
            key=row[0],
            id=row[1],
            name=row[2],
            role=row[3],
            prompt=row[4]
        )
    
    def resolve(self, agent_id: str) -> str | None:
        row = self.db.execute("""
            SELECT agent_key
            FROM agent_registry
            WHERE agent_id = ?
        """, (agent_id,)).fetchone()

        return row[0] if row else None
    
    def list_agents(self) -> List[AgentInfo]:
        rows = self.db.execute("""
            SELECT agent_key, agent_id, name, role, prompt
            FROM agent_registry
        """).fetchall()

        return [
            AgentInfo(
                key=r[0],
                id=r[1],
                name=r[2],
                role=r[3],
                prompt=r[4]            
            )
            for r in rows
        ]