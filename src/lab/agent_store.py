"""Local role definitions. Storage is private to this checkout and never a tool grant."""
import hashlib
import json
import os
import re
import threading
import uuid
from pathlib import Path
from .cloud import CloudError
from .agents import ROLES

MODES = {'plan','research','implementation','review'}

class AgentStore:
    def __init__(self, path):
        self.path=Path(path);self.lock=threading.RLock()

    def _read(self):
        if not self.path.exists():return []
        try:
            if self.path.stat().st_size>400000:raise ValueError()
            rows=json.loads(self.path.read_text(encoding='utf-8'))
            if not isinstance(rows,list) or len(rows)>50:raise ValueError()
            for row in rows:
                if not isinstance(row,dict):raise ValueError()
                self.validate(row)
            return rows
        except (OSError,ValueError,TypeError,CloudError):
            raise CloudError('AGENT_STORE_UNREADABLE',500) from None

    @staticmethod
    def validate(body):
        if not isinstance(body,dict) or set(body)!={'id','name','role','prompt','work_mode'}:raise CloudError('AGENT_DEFINITION_INVALID')
        for key,low,high in [('name',2,80),('role',3,160),('prompt',20,4000)]:
            if not isinstance(body[key],str) or not low<=len(body[key].strip())<=high:raise CloudError('AGENT_DEFINITION_INVALID')
        if not isinstance(body['id'],str) or (body['id'] and not re.fullmatch(r'custom-[0-9a-f]{32}',body['id'])):raise CloudError('AGENT_DEFINITION_INVALID')
        if not isinstance(body['work_mode'],str) or body['work_mode'] not in MODES:raise CloudError('AGENT_DEFINITION_INVALID')
        if re.search(r'sk-[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----',json.dumps(body)):raise CloudError('AGENT_SENSITIVE_INPUT')

    def list(self):
        with self.lock:return self._read()

    def save(self,body):
        self.validate(body)
        with self.lock:
            rows=self._read();row={key:value.strip() for key,value in body.items()}
            if row['id']:
                index=next((i for i,x in enumerate(rows) if x['id']==row['id']),None)
                if index is None:raise CloudError('AGENT_NOT_FOUND',404)
                rows[index]=row
            else:
                if len(rows)>=50:raise CloudError('AGENT_STORE_FULL',409)
                row['id']='custom-'+uuid.uuid4().hex;rows.append(row)
            self.path.parent.mkdir(parents=True,exist_ok=True)
            tmp=self.path.with_suffix('.tmp')
            try:
                tmp.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                os.replace(tmp,self.path)
            except OSError:raise CloudError('AGENT_STORE_WRITE_FAILED',500) from None
            return row

    def resolve(self,ident):
        if not isinstance(ident,str):raise CloudError('AGENT_NOT_FOUND',404)
        if not ident:return None,'general'
        if ident in ROLES:
            prompt=ROLES[ident]['instructions']
        else:
            row=next((x for x in self.list() if x['id']==ident),None)
            if not row:raise CloudError('AGENT_NOT_FOUND',404)
            prompt=f"Role: {row['role']}\nWork mode: {row['work_mode']}\nInstructions: {row['prompt']}"
        prompt+='\nYou can only provide text proposals. You have no tools, filesystem access or authority to execute actions. Do not claim to have run tests or changed files.'
        return prompt,ident+':'+hashlib.sha256(prompt.encode()).hexdigest()
