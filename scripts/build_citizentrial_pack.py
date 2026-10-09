#!/usr/bin/env python3
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw

BASE_ZIP = Path("AIcraft-ResourcePack-0.9.6-Lodestone-Fallback-Fix.zip")
OLD_097 = Path("AIcraft-ResourcePack-0.9.7-CitizenTrial-Relic-Tools.zip")
NEW_ZIP = Path("AIcraft-ResourcePack-0.9.8-CitizenTrial-Tool-Polish.zip")
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
    d.line((6,30,18,14), fill=OUTLINE, width=5); d.line((6,30,18,14), fill=HANDLE, width=3); d.line((8,28,17,15), fill=HANDLE_HI, width=1)
    d.polygon([(5,8),(9,5),(17,6),(20,5),(27,6),(30,9),(27,11),(21,10),(18,13),(15,11),(9,10),(5,11)], fill=OUTLINE)
    d.polygon([(7,8),(10,7),(17,8),(20,7),(26,8),(28,9),(26,9),(20,9),(18,11),(16,9),(10,9),(7,10)], fill=p["base"])
    d.line((10,7,26,8), fill=p["light"], width=1); d.line((9,10,25,9), fill=p["dark"], width=1)
    d.rectangle((16,7,19,10), fill=(78,218,255,255)); d.point((17,6), fill=(192,250,255,255))
    return im

def draw_axe(stage):
    p=STAGES[stage]; im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.line((6,30,18,13), fill=OUTLINE, width=5); d.line((6,30,18,13), fill=HANDLE, width=3); d.line((8,28,17,14), fill=HANDLE_HI, width=1)
    d.polygon([(15,8),(19,5),(27,6),(30,10),(29,15),(25,19),(19,18),(16,15),(13,15),(12,11)], fill=OUTLINE)
    d.polygon([(17,9),(20,7),(26,8),(28,10),(27,14),(24,17),(20,16),(18,14),(15,14),(14,11)], fill=p["base"])
    d.line((20,7,26,8), fill=p["light"], width=1); d.line((24,17,20,16), fill=p["dark"], width=1)
    d.line((18,11,24,15), fill=(76,205,100,255), width=1); d.point((25,14), fill=(177,246,157,255))
    return im

def draw_shovel(stage):
    p=STAGES[stage]; im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.line((6,30,18,14), fill=OUTLINE, width=5); d.line((6,30,18,14), fill=HANDLE, width=3); d.line((8,28,17,15), fill=HANDLE_HI, width=1)
    d.polygon([(15,13),(16,8),(20,4),(25,4),(29,8),(28,14),(24,19),(19,18),(15,15)], fill=OUTLINE)
    d.polygon([(18,13),(18,9),(21,6),(24,6),(27,9),(26,13),(23,17),(20,16),(17,14)], fill=p["base"])
    d.line((21,6,24,6), fill=p["light"], width=1); d.line((20,16,23,17), fill=p["dark"], width=1)
    d.polygon([(21,10),(23,8),(25,10),(23,13)], fill=(224,160,57,255))
    return im

def draw_sword(stage):
    p=STAGES[stage]; im=Image.new("RGBA",(32,32),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.polygon([(8,25),(11,28),(26,9),(28,3),(23,6),(9,22)], fill=OUTLINE)
    d.polygon([(10,24),(11,26),(24,9),(26,5),(23,8),(11,23)], fill=p["base"])
    d.line((12,23,25,7), fill=p["light"], width=1); d.line((10,24,22,10), fill=p["dark"], width=1)
    d.line((13,22,23,10), fill=(239,82,42,255), width=2); d.point((24,8), fill=(255,198,90,255))
    d.line((5,21,15,29), fill=OUTLINE, width=5); d.line((6,22,14,28), fill=p["dark"], width=2)
    d.line((4,31,10,25), fill=OUTLINE, width=5); d.line((5,30,9,26), fill=HANDLE, width=3)
    d.rectangle((2,28,6,31), fill=OUTLINE); d.rectangle((3,29,5,30), fill=(239,82,42,255))
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

        (root/"AIcraft_CHANGELOG_0_9_8_CITIZENTRIAL_TOOL_POLISH.txt").write_text(
            "AIcraft ResourcePack 0.9.8 – CitizenTrial Tool Polish\n"
            "- Sword larger and closer to vanilla size.\n"
            "- Pickaxe, axe and shovel have clearer silhouettes.\n"
            "- Ancient Hoe/Rake uses CustomModelData 260105.\n"
            "- Vanilla fallback remains intact.\n",
            encoding="utf-8"
        )

        mcmeta=root/"pack.mcmeta"
        meta=json.loads(mcmeta.read_text(encoding="utf-8"))
        meta["pack"]["description"]="AIcraft ResourcePack 0.9.8 – CitizenTrial Tool Polish"
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
        # Keep the previous fixed links usable too.
        shutil.copy2(temp_out,OLD_097)
        shutil.copy2(temp_out,BASE_ZIP)

        sha1=hashlib.sha1(temp_out.read_bytes()).hexdigest()
        SERVER_SHA1.write_text(sha1+"\n",encoding="utf-8")
        print(f"Built {NEW_ZIP}")
        print(f"Refreshed {SERVER_ZIP}")
        print(f"SHA1: {sha1}")

if __name__=="__main__":
    main()
