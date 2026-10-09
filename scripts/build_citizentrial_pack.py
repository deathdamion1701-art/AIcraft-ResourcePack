#!/usr/bin/env python3
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw
from build_seraph_armor import add_seraph_assets

BASE_ZIP = Path("AIcraft-ResourcePack-0.9.6-Lodestone-Fallback-Fix.zip")
NEW_ZIP = Path("AIcraft-ResourcePack-0.9.9-Seraph-Chestplates.zip")
SERVER_ZIP = Path("server-pack.zip")
SERVER_SHA1 = Path("server-pack.sha1")

STAGES = {
    "wood":      {"base":(126,88,48,255), "light":(181,132,76,255), "dark":(61,39,24,255)},
    "stone":     {"base":(118,123,126,255), "light":(178,183,184,255), "dark":(56,61,64,255)},
    "iron":      {"base":(188,199,204,255), "light":(242,247,247,255), "dark":(83,93,98,255)},
    "gold":      {"base":(228,177,42,255), "light":(255,226,93,255), "dark":(125,79,20,255)},
    "diamond":   {"base":(55,204,196,255), "light":(155,255,241,255), "dark":(20,98,103,255)},
    "netherite": {"base":(76,65,77,255), "light":(130,111,133,255), "dark":(31,25,32,255)},
}
OUTLINE=(28,23,28,255)
HANDLE=(87,54,31,255)
HANDLE_HI=(148,94,48,255)

CMDS={"pickaxe":260101,"axe":260102,"sword":260103,"shovel":260104}
MATERIALS={"wood":"wooden","stone":"stone","iron":"iron","gold":"golden","diamond":"diamond","netherite":"netherite"}

def draw_pickaxe(stage):
    p=STAGES[stage]; im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    # Robust wooden haft, viewed at the familiar vanilla 45-degree angle.
    d.line((6,29,18,12),fill=OUTLINE,width=6)
    d.line((6,29,18,12),fill=HANDLE,width=4)
    d.line((8,27,18,13),fill=HANDLE_HI,width=1)
    # Forged, clearly hooked pick head; never a thin horizontal bar.
    d.polygon([(3,9),(6,5),(11,4),(17,6),(22,5),(27,4),(31,7),
               (30,11),(27,12),(25,9),(20,9),(18,14),(15,12),(13,10),
               (8,9),(5,12),(3,11)],fill=OUTLINE)
    d.polygon([(6,8),(9,6),(16,8),(22,7),(27,6),(29,8),
               (28,10),(25,8),(19,8),(17,11),(15,9),(9,8),(6,10)],fill=p['base'])
    d.line((9,6,16,8,22,7,27,6),fill=p['light'],width=2)
    d.line((9,9,14,10,17,12),fill=p['dark'],width=1)
    d.rectangle((16,7,19,10),fill=p['dark']); d.point((17,8),fill=(138,220,226,255))
    return im

def draw_axe(stage):
    p=STAGES[stage]; b=p["base"]; l=p["light"]; dk=p["dark"]
    im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    # Slim wooden handle; forged medieval blade with a distinct cutting edge.
    d.line((6,29,19,11),fill=OUTLINE,width=5)
    d.line((6,29,19,11),fill=HANDLE,width=3)
    d.line((7,28,18,12),fill=HANDLE_HI,width=1)
    # Compact head instead of the previous broad blocky axe silhouette.
    d.polygon([(10,5),(13,4),(16,6),(19,9),(22,10),(23,13),(20,15),
               (17,13),(15,13),(11,17),(8,18),(6,16),(9,12),(9,9),(8,7)],fill=OUTLINE)
    d.polygon([(11,7),(13,6),(16,8),(19,11),(21,11),(21,13),
               (19,13),(16,11),(13,12),(10,15),(8,16),(9,13),(11,10)],fill=b)
    d.line((10,7,10,10,8,15),fill=l,width=2)
    d.line((13,6,16,8,19,11),fill=l,width=1)
    d.line((13,13,15,12,19,13),fill=dk,width=1)
    d.point((18,11),fill=(181,218,184,255))
    return im

def draw_shovel(stage):
    p=STAGES[stage]; b=p["base"]; l=p["light"]; dk=p["dark"]
    im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    # Traditional wood T-grip and slender shaft: reads as a digging spade.
    d.line((6,28,19,15),fill=OUTLINE,width=5)
    d.line((6,28,19,15),fill=HANDLE,width=3)
    d.line((8,27,17,17),fill=HANDLE_HI,width=1)
    d.line((3,25,9,31),fill=OUTLINE,width=4)
    d.line((3,25,9,31),fill=HANDLE,width=2)
    d.line((3,25,7,29),fill=HANDLE_HI,width=1)
    # Metal ferrule, squared plate and straight bevel instead of spoon-shaped head.
    d.line((16,19,20,15),fill=dk,width=5)
    d.line((17,18,20,15),fill=(118,117,109,255),width=2)
    d.polygon([(14,10),(22,2),(25,2),(31,8),(31,11),(23,19),(20,19),(14,13)],fill=OUTLINE)
    d.polygon([(17,10),(23,4),(25,4),(29,8),(29,10),(23,16),(20,16),(17,13)],fill=b)
    d.line((17,10,23,4,25,4),fill=l,width=2)
    d.line((29,8,29,10,23,16),fill=dk,width=1)
    d.line((17,13,21,16,23,16),fill=dk,width=1)
    d.line((21,8,25,7),fill=l,width=1)
    d.line((24,3,30,9),fill=l,width=1)
    return im

def draw_sword(stage):
    p=STAGES[stage]; im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    # Broad, straight medieval blade with a proper crossguard and short grip.
    d.polygon([(9,21),(13,25),(28,9),(31,1),(23,5)],fill=OUTLINE)
    d.polygon([(11,21),(13,23),(26,9),(29,4),(24,7)],fill=p['base'])
    d.line((12,21,27,7),fill=p['light'],width=2)
    d.line((14,23,25,11),fill=p['dark'],width=1)
    d.line((17,16,22,11),fill=(231,131,49,255),width=1)
    d.polygon([(5,18),(8,17),(17,26),(16,29),(13,29),(5,21)],fill=OUTLINE)
    d.line((7,19,15,27),fill=p['dark'],width=2)
    d.line((5,30,11,24),fill=OUTLINE,width=5)
    d.line((5,30,11,24),fill=HANDLE,width=3)
    d.line((7,28,10,25),fill=HANDLE_HI,width=1)
    d.rectangle((2,29,5,31),fill=OUTLINE)
    d.point((3,30),fill=p['light'])
    return im

def draw_ancient_hoe():
    im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.line((6,30,18,13), fill=OUTLINE, width=5); d.line((6,30,18,13), fill=HANDLE, width=3); d.line((8,28,17,14), fill=HANDLE_HI, width=1)
    d.polygon([(12,7),(28,5),(30,7),(29,11),(19,12),(16,15),(13,14),(15,10),(12,10)], fill=OUTLINE)
    d.polygon([(14,8),(27,7),(28,8),(27,9),(18,10),(16,12),(15,12),(17,9),(14,9)], fill=(176,132,48,255))
    d.line((15,8,27,7), fill=(240,205,102,255), width=1)
    for x,y in [(20,10),(23,9),(26,9),(28,8)]:
        d.line((x,y,x+1,y+5), fill=OUTLINE, width=3)
        d.line((x,y+1,x+1,y+4), fill=(83,116,62,255), width=1)
    d.rectangle((16,10,18,12), fill=(91,182,76,255)); d.point((17,9), fill=(188,238,139,255))
    return im

DRAWERS={"pickaxe":draw_pickaxe,"axe":draw_axe,"sword":draw_sword,"shovel":draw_shovel}

def ensure_mapping(items, item_name, cmd, model_name):
    path=items/f"{item_name}.json"
    if path.exists():
        data=json.loads(path.read_text(encoding="utf-8"))
    else:
        data={"model":{"type":"minecraft:range_dispatch","property":"minecraft:custom_model_data","index":0,
                       "fallback":{"type":"minecraft:model","model":f"minecraft:item/{item_name}"},"entries":[]}}
    model=data.get("model",{})
    if model.get("type")!="minecraft:range_dispatch" or model.get("property")!="minecraft:custom_model_data":
        data={"model":{"type":"minecraft:range_dispatch","property":"minecraft:custom_model_data","index":0,
                       "fallback":model or {"type":"minecraft:model","model":f"minecraft:item/{item_name}"},"entries":[]}}
    entries=[e for e in data["model"].setdefault("entries",[]) if e.get("threshold")!=cmd]
    entries.append({"threshold":cmd,"model":{"type":"minecraft:model","model":model_name}})
    entries.sort(key=lambda e:e.get("threshold",0))
    data["model"]["entries"]=entries
    path.write_text(json.dumps(data,indent=2),encoding="utf-8")

def main():
    if not BASE_ZIP.exists():
        raise SystemExit(f"Missing base pack: {BASE_ZIP}")

    with tempfile.TemporaryDirectory() as td:
        root=Path(td)/"pack"; root.mkdir()
        with zipfile.ZipFile(BASE_ZIP,"r") as z:
            z.extractall(root)

        textures=root/"assets/aicraft/textures/item"
        models=root/"assets/aicraft/models/item"
        items=root/"assets/minecraft/items"
        textures.mkdir(parents=True,exist_ok=True); models.mkdir(parents=True,exist_ok=True); items.mkdir(parents=True,exist_ok=True)

        for tool,drawer in DRAWERS.items():
            for stage in STAGES:
                drawer(stage).save(textures/f"citizentrial_{tool}_{stage}.png")
                (models/f"citizentrial_{tool}_{stage}.json").write_text(json.dumps({
                    "parent":"minecraft:item/handheld",
                    "textures":{"layer0":f"aicraft:item/citizentrial_{tool}_{stage}"}
                },indent=2),encoding="utf-8")
                ensure_mapping(items,f"{MATERIALS[stage]}_{tool}",CMDS[tool],f"aicraft:item/citizentrial_{tool}_{stage}")

        draw_ancient_hoe().save(textures/"citizentrial_ancient_hoe.png")
        (models/"citizentrial_ancient_hoe.json").write_text(json.dumps({
            "parent":"minecraft:item/handheld",
            "textures":{"layer0":"aicraft:item/citizentrial_ancient_hoe"}
        },indent=2),encoding="utf-8")
        for prefix in MATERIALS.values():
            ensure_mapping(items,f"{prefix}_hoe",260105,"aicraft:item/citizentrial_ancient_hoe")

        (root/"AIcraft_CHANGELOG_0_9_8b_CITIZENTRIAL_SPADE_AXE.txt").write_text(
            "AIcraft ResourcePack 0.9.9 – CitizenTrial + Seraph Chestplates\\n"
            "- CitizenTrial axe slimmer, with forged edge: 6 stages.\\n"
            "- CitizenTrial shovel shaped as squared spade with a wooden T-grip: 6 stages.\\n"
            "- Existing CitizenTrial sword, pickaxe, relics, Stargate and other assets unchanged.\\n"
            "- CustomModelData, JSON mappings and vanilla fallback preserved.\\n",
            encoding="utf-8"
        )

        add_seraph_assets(root)

        mcmeta=root/"pack.mcmeta"
        meta=json.loads(mcmeta.read_text(encoding="utf-8"))
        meta["pack"]["description"]="AIcraft ResourcePack 0.9.8b – CitizenTrial Spade & Slim Axe"
        mcmeta.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")

        for path in root.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

        temp_out=Path(td)/NEW_ZIP.name
        with zipfile.ZipFile(temp_out,"w",zipfile.ZIP_DEFLATED) as z:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    z.write(path,path.relative_to(root))

        shutil.copy2(temp_out,NEW_ZIP)
        shutil.copy2(temp_out,SERVER_ZIP)

        sha1=hashlib.sha1(temp_out.read_bytes()).hexdigest()
        SERVER_SHA1.write_text(sha1+"\n",encoding="utf-8")
        print(f"Built {NEW_ZIP}")
        print(f"Refreshed {SERVER_ZIP}")
        print(f"SHA1: {sha1}")

if __name__=="__main__":
    main()
