#
# Description: Source code for the chat cache for Site Sense AI
# Author: Alexander Powell
# Version: v1.0
# Dependencies: N/A
#

from langchain_core.caches import BaseCache
import psycopg2
import json

class SiteSenseCache(BaseCache):
    def __init__(self, conn_url):
        self.conn = psycopg2.connect(conn_url)
        self.conn.autocommit = True  # Auto commits the commands so you dont need to use conn.commit()
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sitesense_cache (
                    prompt TEXT PRIMARY KEY,
                    llm_response TEXT
                );
            """)

    @staticmethod
    def serialize_prompt(prompt) -> str:
        if isinstance(prompt, str):
            return prompt
        try:
            return json.dumps(prompt, sort_keys=True)
        except Exception:
            return str(prompt)

    def lookup(self, prompt: str) -> str | None:
        prompt_str = self.serialize_prompt(prompt)
        print(f"[+] {prompt_str}")
        with self.conn.cursor() as cur:
            cur.execute("SELECT llm_response FROM sitesense_cache WHERE prompt = %s", (prompt_str,))
            row = cur.fetchone()
            return row[0] if row else None

    def update(self, prompt: str, llm_response: str) -> None:
        prompt_str = self.serialize_prompt(prompt)
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sitesense_cache (prompt, llm_response)
                VALUES (%s, %s)
                ON CONFLICT (prompt) DO UPDATE
                SET llm_response = EXCLUDED.llm_response;
            """, (prompt_str, llm_response))

    def clear(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM sitesense_cache")
