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
 # Slender medieval breastplate icon: light trim, narrow shoulders, small rune.
 im=Image.new("RGBA",(32,32));d=ImageDraw.Draw(im)
 metal=p["metal"];light=p["light"];shade=p["shade"]
 trim=p["edge"];gem=p["accent"];fabric=p["cloth"]
 poly(d,[(8,5),(13,4),(15,7),(17,7),(19,4),(24,5),
         (29,11),(27,17),(24,16),(23,26),(9,26),(8,16),
         (5,17),(3,11)],shade)
 poly(d,[(9,6),(12,6),(15,10),(17,10),(20,6),(23,6),
         (27,11),(26,15),(23,14),(22,24),(10,24),
         (9,14),(6,15),(5,11)],fabric)
 # Narrow silver/metal breastplate on top of the fitted tunic.
 poly(d,[(11,9),(15,12),(17,12),(21,9),(23,13),
         (21,18),(19,23),(13,23),(11,18),(9,13)],metal)
 d.line([(10,11),(13,14),(16,16),(19,14),(22,11)],fill=trim,width=1)
 d.line([(12,19),(15,21),(17,21),(20,19)],fill=light,width=1)
 poly(d,[(16,14),(18,17),(16,20),(14,17)],trim)
 poly(d,[(16,15),(17,17),(16,19),(15,17)],gem)
 d.line([(10,23),(13,25),(19,25),(22,23)],fill=trim,width=1)
 d.point((12,10),fill=light);d.point((20,10),fill=light)
 return im

def armor_texture(p):
 """Slim illustrated chest armor on the vanilla humanoid UV atlas (128x64).
 Transparent arms and side margins reduce the perceived size, while armor
 geometry and all gameplay mechanics remain unchanged.
 Body front: x40..55, back: x64..79, sides x32..39 / x56..63.
 Arms: x80..111. Chestplate only: leave all other UV areas transparent.
 """
 im=Image.new("RGBA",(128,64),(0,0,0,0));d=ImageDraw.Draw(im)
 metal=p["metal"];light=p["light"];shade=p["shade"]
 trim=p["edge"];gem=p["accent"];fabric=p["cloth"]

 # FRONT: fitted linen tunic underneath a tapered breastplate.
 # Transparent side margins keep the chest from reading as a solid box.
 poly(d,[(43,41),(46,40),(49,40),(52,41),(53,45),(53,53),
         (51,59),(50,62),(45,62),(44,59),(42,53),(42,45)],fabric)
 d.line([(44,42),(47,44),(50,42),(52,44)],fill=light,width=1)
 poly(d,[(43,45),(47,48),(48,51),(49,48),(52,45),
         (51,53),(50,56),(48,58),(45,56),(44,53)],metal)
 d.line([(43,46),(47,51),(48,53),(49,51),(52,46)],fill=trim,width=1)
 d.line([(44,54),(48,58),(51,54)],fill=shade,width=1)
 d.line([(45,59),(48,60),(50,59)],fill=trim,width=1)
 # Tiny gem instead of the previous huge central cross.
 poly(d,[(48,49),(50,52),(48,55),(46,52)],trim)
 poly(d,[(48,50),(49,52),(48,54),(47,52)],gem)
 d.point((48,50),fill=light)

 # BACK: narrow textile vest and two fine embroidered lines;
 # deliberately no broad glowing insignia covering the player's back.
 poly(d,[(67,41),(71,40),(74,40),(77,41),(77,52),
         (76,57),(75,62),(69,62),(68,57),(67,52)],fabric)
 poly(d,[(68,42),(71,41),(73,41),(76,42),(76,47),
         (73,48),(71,48),(68,47)],shade)
 d.line([(68,44),(71,46),(73,46),(76,44)],fill=trim,width=1)
 d.line([(69,48),(69,55),(71,60)],fill=trim,width=1)
 d.line([(75,48),(75,55),(73,60)],fill=trim,width=1)
 d.line([(71,58),(72,60),(73,58)],fill=light,width=1)
 poly(d,[(72,49),(74,51),(72,54),(70,51)],metal)
 poly(d,[(72,50),(73,51),(72,53),(71,51)],gem)

 # Side panels are mainly fabric. A thin metal clasp, not a solid slab.
 for sx in (32,56):
  poly(d,[(sx+2,42),(sx+5,42),(sx+6,46),(sx+6,54),
          (sx+5,59),(sx+3,61),(sx+2,57),(sx+1,51)],fabric)
  d.line([(sx+2,44),(sx+5,45)],fill=trim,width=1)
  d.line([(sx+2,52),(sx+5,52)],fill=shade,width=1)

 # SHORT shoulder guards only, the rest of each arm shows normal clothing.
 # Previous design covered entire upper arms, making a huge rectangular pauldron.
 for sx in (80,88,96,104):
  poly(d,[(sx+2,41),(sx+5,41),(sx+7,44),
          (sx+6,47),(sx+2,47),(sx+1,44)],metal)
  d.line([(sx+2,42),(sx+5,42)],fill=light,width=1)
  d.line([(sx+1,45),(sx+3,47),(sx+6,46)],fill=trim,width=1)
  d.point((sx+4,44),fill=shade)

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
 (root/"AIcraft_CHANGELOG_0_9_10_SERAPH_ELEGANT.txt").write_text(
  "AIcraft ResourcePack 0.9.10: Five elegant medieval Seraph chestplates (Variant B).\n"
  "Special PDC-marked plates only; vanilla armor and game rules preserved.\n"
  "Less bulky shoulder plates, narrow tapered armor, fine back embroidery.\n"
  "Equipped textures require AIcraft-SeraphVisuals plugin.\n",encoding="utf-8")

if __name__=="__main__":
 import sys
 if len(sys.argv)!=2:raise SystemExit("Usage: build_seraph_armor.py PACK_DIRECTORY")
 add_seraph_assets(sys.argv[1])
