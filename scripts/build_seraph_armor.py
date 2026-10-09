"""Five medieval Seraph chestplate textures. Only PDC-marked Seraph items are assigned these assets."""
from pathlib import Path
import json
from PIL import Image, ImageDraw

VARIANTS = {
 "iron": {"material":"iron","cmd":261201,"metal":"#c9c9cf","light":"#f9f6e6","shade":"#62616b","edge":"#ba8b42","accent":"#4bb7d2","cloth":"#ede7d8"},
 "copper": {"material":"copper","cmd":261202,"metal":"#be704d","light":"#f6c594","shade":"#613b32","edge":"#e3a878","accent":"#3fbb9e","cloth":"#216854"},
 "gold": {"material":"golden","cmd":261203,"metal":"#c8912d","light":"#ffe399","shade":"#7b321e","edge":"#e6ab3f","accent":"#ff692b","cloth":"#971f20"},
 "diamond": {"material":"diamond","cmd":261204,"metal":"#75cbe5","light":"#f7f8f2","shade":"#2479b2","edge":"#e8c17d","accent":"#25c8fa","cloth":"#1765ae"},
 "netherite": {"material":"netherite","cmd":261205,"metal":"#48444f","light":"#9891a4","shade":"#231f30","edge":"#7e5b8b","accent":"#d263fc","cloth":"#39234e"}
}
def rect(d,box,c): d.rectangle(box,fill=c)
def poly(d,pts,c): d.polygon(pts,fill=c)

def chest_icon(p):
 im=Image.new("RGBA",(32,32));d=ImageDraw.Draw(im);dark="#28222c";edge=p["edge"];light=p["light"];metal=p["metal"]
 poly(d,[(7,4),(12,3),(14,6),(18,6),(20,3),(25,4),(31,12),(29,20),(25,19),(24,28),(8,28),(7,19),(3,20),(1,12)],dark)
 poly(d,[(8,6),(12,5),(15,9),(17,9),(20,5),(24,6),(29,12),(27,17),(23,15),(22,26),(10,26),(9,15),(5,17),(3,12)],metal)
 poly(d,[(8,6),(13,6),(15,10),(17,10),(20,6),(24,6),(23,11),(20,14),(12,14),(9,11)],light)
 poly(d,[(12,4),(15,4),(15,7),(17,7),(17,4),(20,4),(19,10),(13,10)],dark)
 d.line([(5,10),(9,7),(12,12),(16,15),(20,12),(23,7),(28,10)],fill=edge,width=2)
 d.line([(4,12),(7,17),(9,16)],fill=p["shade"],width=2)
 d.line([(28,12),(25,17),(23,16)],fill=p["shade"],width=2)
 poly(d,[(16,12),(19,16),(16,22),(13,16)],edge)
 poly(d,[(16,13),(18,16),(16,20),(14,16)],p["accent"])
 d.line([(10,18),(11,24),(15,26),(17,26),(21,24),(22,18)],fill=p["shade"],width=2)
 d.line([(10,24),(13,25),(19,25),(22,24)],fill=edge,width=2)
 rect(d,(15,21,17,22),light)
 return im

def armor_texture(p):
 # Full-size 128x64 humanoid-layer UV, i.e. standard 64x32 armor map x2.
 im=Image.new("RGBA",(128,64));d=ImageDraw.Draw(im)
 metal=p["metal"];edge=p["edge"];light=p["light"];shade=p["shade"];accent=p["accent"];cloth=p["cloth"]
 # Torso front x40..55; back x64..79; sides x32..39 and x56..63.
 for box in [(40,40,55,63),(64,40,79,63),(32,40,39,63),(56,40,63,63)]:rect(d,box,shade)
 rect(d,(41,41,54,60),metal);rect(d,(43,42,52,44),light)
 d.line([(41,45),(47,51),(48,57),(54,45)],fill=edge,width=2)
 d.line([(41,56),(47,61),(54,56)],fill=edge,width=2)
 d.line([(41,59),(54,59)],fill=shade,width=2)
 poly(d,[(48,48),(52,53),(48,59),(44,53)],edge)
 poly(d,[(48,50),(50,53),(48,57),(46,53)],accent)
 d.line([(41,46),(43,49)],fill=light,width=2)
 d.line([(54,46),(52,49)],fill=light,width=2)
 d.line([(41,61),(54,61)],fill=edge,width=2)
 rect(d,(45,60,50,62),cloth)
 rect(d,(65,41,78,61),metal);d.line([(65,43),(78,43)],fill=light,width=2)
 d.line([(65,54),(72,59),(78,54)],fill=edge,width=2)
 poly(d,[(72,46),(75,49),(72,54),(69,49)],accent)
 d.line([(65,61),(78,61)],fill=edge,width=2)
 for bx0 in (32,56):
  rect(d,(bx0+1,41,bx0+6,61),metal)
  d.line([(bx0+1,43),(bx0+6,47)],fill=edge,width=2)
  d.line([(bx0+1,59),(bx0+6,59)],fill=light,width=1)
 # Upper arms (one vanilla arm UV; Minecraft mirrors for the second arm).
 for bx0 in (80,88,96,104):
  rect(d,(bx0,40,bx0+7,63),shade)
  rect(d,(bx0+1,41,bx0+6,58),metal)
  d.line([(bx0+1,44),(bx0+6,46)],fill=light,width=2)
  d.line([(bx0+1,49),(bx0+6,51)],fill=edge,width=2)
  d.line([(bx0+1,57),(bx0+6,58)],fill=edge,width=2)
  rect(d,(bx0+2,60,bx0+5,62),cloth)
 # Do not fill helmet or leggings UV: chestplate only.
 return im

def insert_item_model(items,material,cmd,model_id):
 file=items/f"{material}_chestplate.json"
 old=(json.loads(file.read_text(encoding="utf-8")).get("model") if file.exists()
      else {"type":"minecraft:model","model":f"minecraft:item/{material}_chestplate"})
 if old.get("type")=="minecraft:range_dispatch" and old.get("property")=="minecraft:custom_model_data" and old.get("index",0)==0:
  model=old
 else:
  model={"type":"minecraft:range_dispatch","property":"minecraft:custom_model_data","index":0,"fallback":old,"entries":[]}
 entries=[e for e in model.get("entries",[]) if e.get("threshold")!=cmd]
 entries.append({"threshold":cmd,"model":{"type":"minecraft:model","model":model_id}})
 model["entries"]=sorted(entries,key=lambda e:e["threshold"])
 file.write_text(json.dumps({"model":model},indent=2),encoding="utf-8")

def add_seraph_assets(root):
 root=Path(root)
 eq=root/"assets/aicraft/equipment";tex=root/"assets/aicraft/textures/entity/equipment/humanoid"
 icons=root/"assets/aicraft/textures/item";models=root/"assets/aicraft/models/item";items=root/"assets/minecraft/items"
 for f in (eq,tex,icons,models,items):f.mkdir(parents=True,exist_ok=True)
 for variant,p in VARIANTS.items():
  name=f"seraph_{variant}"
  (eq/f"{name}.json").write_text(json.dumps({"layers":{"humanoid":[{"texture":f"aicraft:{name}"}]}},indent=2),encoding="utf-8")
  armor_texture(p).save(tex/f"{name}.png")
  chest_icon(p).save(icons/f"{name}.png")
  (models/f"{name}.json").write_text(json.dumps({"parent":"minecraft:item/generated","textures":{"layer0":f"aicraft:item/{name}"}},indent=2),encoding="utf-8")
  insert_item_model(items,p["material"],p["cmd"],f"aicraft:item/{name}")
 (root/"AIcraft_CHANGELOG_0_9_9_SERAPH_CHESTPLATES.txt").write_text(
  "AIcraft ResourcePack 0.9.9: Five medieval Seraph chestplates.\n"
  "Special PDC-marked plates only; vanilla armor and game rules preserved.\n"
  "Equipped textures require AIcraft-SeraphVisuals plugin.\n",encoding="utf-8")

if __name__=="__main__":
 import sys
 if len(sys.argv)!=2:raise SystemExit("Usage: build_seraph_armor.py PACK_DIRECTORY")
 add_seraph_assets(sys.argv[1])
