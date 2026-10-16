import re,json,unicodedata
from pathlib import Path
from html.parser import HTMLParser
class Details(HTMLParser):
 def __init__(self,s):
  super().__init__();self.fields=[];self.current=None;self.images=[];self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t in ['h3','h4','p','span']:self.current=[t,''];self.fields.append(self.current)
  if t=='img':self.images.append(a.get('src',''))
 def handle_endtag(self,t):
  if self.current and self.current[0]==t:self.current=None
 def handle_data(self,s):
  if self.current:self.current[1]+=s

def norm(s):return re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower())
def source_rows(path):
 out=[]
 for block in re.split(r'(?=<div class="producto")',Path(path).read_text())[1:]:
  d=Details(block);name=re.search(r'data-name="([^"]+)"',block)[1]
  skus=re.findall(r'SKU\s*:\s*(?:<span[^>]*>)?\s*(\d{7,8})',block)
  skus+=re.findall(r'\.innerHTML\s*=\s*"(\d{7,8})"',block)
  pairs=re.findall(r'(?:if|else if)\s*\(select.value === "([^"]+)"\)\s*\{\s*\w+\.innerHTML = "(\d+)"',block)
  ps=[v.strip() for t,v in d.fields if t=='p' and v.strip() and not v.strip().startswith('SKU')]
  out.append(dict(name=name,skus=list(dict.fromkeys(skus)),sizes=dict(pairs),labels=ps,image=d.images[0] if d.images else ''))
 return out

def build(path):
 rows=source_rows(path)
 categories={
 'LIMPIEZA':'Limpieza', 'EPP':'EPP', 'PAPELERIA':'Papelería',
 'SOLVENTES':'Solventes', 'LUBRICANTES':'Lubricantes', 'QUIMICOS':'Químicos',
 'UNIFORMES':'Uniformes', 'REFACCIONES':'Refacciones', 'GASES':'Gases',
 'ADHESIVOS':'Adhesivos y selladores', 'PINTURAS':'Pinturas y recubrimientos',
 'HERRAMIENTAS':'Herramientas y consumibles', 'INSUMOS':'Insumos generales'}
 images={norm(p.stem):p.as_posix() for p in Path('Images').iterdir() if p.is_file()}
 products=[]
 for row in rows:
  name=row['name']; n=norm(name);labels=row['labels']; label=labels[0] if labels else ''
  category={'Lubricantes':'LUBRICANTES','Solventes':'SOLVENTES','Quimicos':'QUIMICOS','Uniforme':'UNIFORMES','Papeleria':'PAPELERIA','EPP':'EPP','Gases':'GASES'}.get(label,'LIMPIEZA' if 'Limpieza' in label else 'INSUMOS')
  subcategory=labels[1] if len(labels)>1 and not labels[1].startswith('©') else ''
  if name.startswith(('Aceite','Grasa','Aflojatodo','Antiderrapante','Lubricador','Lubricante')):category='LUBRICANTES'
  if name.startswith(('Adhesivo','Fijador','Formajuntas','Loctite','Pegamento','Resina','Silicon','Silicona','Empaquetadura')):category='ADHESIVOS'
  if name.startswith(('Barniz','Esmalte','Pintura','Polymar')):category='PINTURAS'
  if name.startswith(('Antiespumante','Bicarbonato','Glicerina')):category='QUIMICOS'
  if name.startswith(('Limpiador de Superficie','Cloro Cloralex')):category='LIMPIEZA'
  if name.startswith(('Cinta Metrica','Brocha','Pasta de Diamante','Pasta de Soldadura')):category='HERRAMIENTAS'
  if name.startswith('Philips'):category='REFACCIONES'
  if name.startswith('Placa Acrilica'):category='INSUMOS'
  if category=='EPP':
   if name.startswith(('Bloqueo','Base de Bloqueo','Broche para Bloqueo','Candado')):subcategory='Bloqueo y etiquetado (LOTOTO)'
   elif name.startswith(('Cartucho','Mascarilla','Respirador','Prefiltro')):subcategory='Protección respiratoria'
   elif name.startswith(('Casco','Barbiquejo','Gorra','Suspension')):subcategory='Protección de cabeza'
   elif name.startswith(('Guante','Guantes','Manga Anticorte','Antebrazo')):subcategory='Protección de manos y brazos'
   elif name.startswith(('Bota','Botas','Plantilla','Cubre Bota')):subcategory='Calzado de seguridad'
   elif name.startswith(('Lente','Cristal','Mica','Protector Facial')):subcategory='Protección ocular y facial'
   elif name.startswith(('Orejera','Tapon')):subcategory='Protección auditiva'
   elif name.startswith(('Chaleco','Impermeable','Overol','Cofia')):subcategory='Ropa y protección corporal'
   elif name.startswith(('Cinta','Rollo de Señalamiento','Bengala','Cadena','Manga Indicadora')):subcategory='Señalización y seguridad'
   else:subcategory='Soporte y protección corporal'
  image=images.get(n,'Images/placeholder.svg')
  if name == 'Botas Procliff':image='Images/Proximamente Botas Procliff.PNG'
  if name.startswith('Aceite (39433735'):image='Images/aceite-39433735-ingersoll-rand-litro.png'
  products.append(dict(id='dispatch-'+str(len(products)+1),name=name,category=category,subcategory=subcategory,sku=row['skus'][0],sizes=row['sizes'],image=image,source='dispatch',source_name=name))
 # Keep the existing local SKU when it conflicts with the linked catalog.
 products.append(dict(id='local-5537478',name='Limpiador de Superficie Tipo Espuma 400 g',category='LIMPIEZA',subcategory='',sku='5537478',sizes={},image=images[norm('Limpiador de Superficie Tipo Espuma 400 g')],source='local',note='El catálogo enlazado usa SKU 4056842 para esta descripción. Confirmar con inventario antes de unificar.'))
 Path('data/source-dispatch.json').write_text(json.dumps({'url':'https://almacengeneral.github.io/Productos-Despacho/index.html','checked_on':'2026-10-16','products':rows},ensure_ascii=False,indent=2)+'\n')
 Path('data/catalog.json').write_text(json.dumps({'categories':categories,'products':products},ensure_ascii=False,indent=2)+'\n')
 print('Products',len(products),'source SKUs',len({s for p in rows for s in p['skus']}))
 for p in products:
  if p['image'].endswith('placeholder.svg'):print('Missing image:',p['name'])

if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description='Importar una copia HTML del catálogo de despacho.')
 parser.add_argument('html_path')
 build(parser.parse_args().html_path)
