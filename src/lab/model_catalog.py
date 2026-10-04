"""Public reference catalog, not account access or a latency benchmark."""
from copy import deepcopy

LEVELS = ['low','medium','high','xhigh','max']
MODELS = [
 {'provider':'openai','id':'gpt-6.1-sol','name':'GPT-6.1 Sol','profile':{'es':'Equilibrio entre capacidad y coste','en':'Balance of capability and cost'},'efforts':LEVELS,'source':'https://developers.openai.com/api/docs/models'},
 {'provider':'openai','id':'gpt-6-astra','name':'GPT-6 Astra','profile':{'es':'Trabajo complejo y razonamiento profundo','en':'Complex work and deep reasoning'},'efforts':LEVELS,'source':'https://developers.openai.com/api/docs/models'},
 {'provider':'openai','id':'gpt-6-luna','name':'GPT-6 Luna','profile':{'es':'Tareas acotadas y eficiencia','en':'Focused tasks and efficiency'},'efforts':['none']+LEVELS,'source':'https://developers.openai.com/api/docs/models'},
 {'provider':'anthropic','id':'claude-sonnet-5-5','name':'Claude Sonnet 5.5','profile':{'es':'Rápido · trabajo cotidiano','en':'Fast · everyday work'},'efforts':LEVELS,'source':'https://platform.claude.com/docs/en/models/sonnet-5-5/overview'},
 {'provider':'anthropic','id':'claude-opus-5-5','name':'Claude Opus 5.5','profile':{'es':'Velocidad moderada · trabajo complejo','en':'Moderate speed · complex work'},'efforts':LEVELS,'source':'https://platform.claude.com/docs/en/models/opus-5-5/overview'},
 {'provider':'anthropic','id':'claude-fable-5-1','name':'Claude Fable 5.1','profile':{'es':'Más pausado · razonamiento exigente','en':'Slower · demanding reasoning'},'efforts':LEVELS,'source':'https://platform.claude.com/docs/en/models/fable-5-1/overview'},
 {'provider':'anthropic','id':'claude-haiku-4-5-20251001','name':'Claude Haiku 4.5','profile':{'es':'Muy rápido · tareas sencillas','en':'Very fast · simple tasks'},'efforts':[],'source':'https://platform.claude.com/docs/en/models/haiku-4-5/overview'},
]

def catalog():
 return {'checked_on':'2026-10-03','kind':'documented_reference','models':deepcopy(MODELS)}

def supports(provider,model,effort):
 if effort=='default':return True
 row=next((x for x in MODELS if x['provider']==provider and x['id']==model),None)
 return isinstance(effort,str) and row is not None and effort in row['efforts']
