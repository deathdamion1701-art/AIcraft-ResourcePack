#!/usr/bin/env python3
import base64
import json
import hashlib
import shutil
import tempfile
import zipfile
from pathlib import Path

BASE_ZIP = Path("AIcraft-ResourcePack-0.9.6-Lodestone-Fallback-Fix.zip")
NEW_ZIP = Path("AIcraft-ResourcePack-0.9.7-CitizenTrial-Relic-Tools.zip")
SERVER_ZIP = Path("server-pack.zip")
SERVER_SHA1 = Path("server-pack.sha1")

TEXTURES = {"citizentrial_axe_diamond.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABbklEQVR4nO2WMU/CQBiGH8TgWsZC2jCS6GJCmNgcdGQgTiRG/oGzs7/AvQ7yA1gddNGJxUnDZgKhjLLahNRBj1zqceXa62DCu17vnuf77mta2GWXXSzHd73Y5PlS0eDpYqZl5BJQQa/DNwBuaofKPUmhzAIyvDYa/lm/bB8DcDd+BSDs9u0ICLAKqooQER2xJmAiIaLqwp6pQLICJwoIu/314abJNAO+68WyyNnzRbysDLR7Ns2AcQeSh/iuF7+fP+FEAU4UAHB1NFHCVbH6GtZGQ5woYFkZ8HF7D8DB44NSPLeA73pxu14GYDxfAfB1crpel8E6gf2sAiKdZhX4/BFRQHVwyDGE7XqZTrPKy+QXPl8xXcxKyQFNi/EQyq1XxQRuLCDDVdWbnJVJQMQW3EhAd+9Z4VsLFAXfSkAFtxmtwKaJt1V9qoBIEa1PFSjy3lMF5NYXce9ytNX0Wo31166I6rdKr9WITf/1/1W+AQhWxV4HUDL3AAAAAElFTkSuQmCC","citizentrial_axe_gold.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABa0lEQVR4nO2WP0/CQBiHH8TEFaamIS2MzA3WhTAa3YmLg2sH+TQsuJr4JRwc0IWaMBpXIYR0ktWB1IGUXOr12uufwaS/9Xr3PO97b9NCnTp1So5tWqHO842qwavtWskoJCCDfi0uAehePEv3xIVyC4jw+bT1Z73rugch3wdgNNlJBU7zgmVQMRE4EgF5R7Q7kFa5KrIunOgKxFvoGQ6jye54uG5yzYBtWqEocvV6F86CpXJP0gxodyB+iG1a4cfNC57h4BkOAIvreylcllJfw/m0hWc4zIIlD48BAE/vZ1LxwgK2aYVupwmAv9kDcHv+c1wXwSoB7dcwnmG/DXwnQlVwKDCEbqfJsN/m7fMA9zd7Vtt1Iz6gadEeQrH1sujAtQVEuKx6nbNyCUQpC64loLr3vPDMAlXBMwnI4GVGKZA08WVVnyoQpYrWpwpUee+pAmLrq7h3McpqxoPe8WtXRfWZMh70Qt1//X+VX+XZwknhfSeeAAAAAElFTkSuQmCC","citizentrial_axe_iron.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABbElEQVR4nO2WsWrCQBjHf9a8gHQKorgpFaSIdXIqCJ2De8HZMY/hKGTzATrkBRzbqQUpBaGuijiVvoCSDm3kiJdLLskNBf9rcvf7fd99RwKXXHJJwanbtUDn/ZJp8Ga/VTJyCcigy/UKgG6zLV0TFcosIMLnvn/2/LbdBOB9tQZg7DhSASsrWAYVE4JDkbhodyCpclVkXbjSFYi2cHqYMXac0+a6yTQDdbsWiCIPz4+Ba02Ua+JmIPc1DI/k5ukeANea8NVZcv3RPYMXLhC9hnPfZ3qY4VoTPM8D4G2xiIXnEqjbtaBfLQPwujsCcDccnp6LYJWA9jWMZtCqAN+/IhKoCg45hrBfLTNoVXj5/IPvjmz221J0QJOifQ3F1suiA9cWEOGy6nX2yiQQpii4loDq3LPCUwuYgqcSkMGLjFIgbuKLqj5RIIyJ1icKmDz3RAGx9SbOXYyymlGvcframag+VUa9RqD7r/+v8gNlbcHI6OJ7gQAAAABJRU5ErkJggg==","citizentrial_axe_netherite.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABaElEQVR4nO2WsU6DQBjHfxRfoGEiDaQjMWk62DD1AVxcTOOoLr5GB16ji0/g5OyiUxMHbFKZ25hOjU+AOCEnHncchcGkvxW4/+/77jsAjhw50jK+62Um91tdB292W2XGQQKy0NvLOwDuHxbSZ8pCjQXE8FEw/nP97DQE4HW9BGCVxFKBk6bBslCRPDgXyQXKGHdAV7kKWRd6pgLlFqaRwyqJKyvU0WgGfNfLRJHz55vMnu+Vz1TNgHEHyov4rpetr55II4c0cgC4fryQhsto9RiOgjFp5GDP98TvbwD0rOIW2TvhoGMYDmwAlh8pAF9ZsZwYrBIwPoZlpkEf+PwlIqPqjdh4CMOBzTTo85IU4Zvd1ioPqA7jIRRbL8Mk3FhADJdVb7JWI4GctsKNBFT73jS8tkBX4bUEZOFtohSomvi2qtcK5HTReq1Al/uuFRBb38W+iyirmU2GP1+ULqqvxWwyzEz/9f8V3xfRyIbPUQeXAAAAAElFTkSuQmCC","citizentrial_axe_stone.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABb0lEQVR4nO2WsU7CQBjHf4gvwNhgGxiMjJhgXVib+ACEgcUBSRzdfA1HE3X1JUgYqou4dCIahyYgYfQJSB20zQWPa6+9Dib812v7+33ffdcWdtllF8NxLDvSub5SNni+WigZhQRk0Jv7WwCuLi6l92wK5RYQ4YPR8M+6e3oCwPTlFYDHuwczAjFYBpUlFok7YkxARyKOrAv7ugLz1aIiSgReyKw/ySUEOWfAsexIrOLs6Txqj5vKe7bNwF4eAfEhjmVHs/6EwAsJvBCA42tLCpfF6DEcjIYEXkh73MT3fQA+3z+k4oUFHMuO3HoVgOlyDcDB0WGyLoJVAtpDuJluqwZ8/YhIoCo4FBhCt16l26rx/PYLX66TE5L2+hWjPYRi62XRgWsLiHBZ9TrPyiUQxxRcS0C173nhmQXKgmcSkMFNRimwbeJNVZ8qEKeM1qcKlLnvqQJi68vYdzHKanqdRvK1K6P6TOl1GpHuv/6/yjd3p8hVHKwWYAAAAABJRU5ErkJggg==","citizentrial_axe_wood.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABcklEQVR4nO2WsUrDQBjHf7XuUgpCCAmdpC6NYCkU+gA+QJFunR2z+QhufQZx6VO4VCg42QxVHFtKQSniA9S4ePWIl0suTQYhvzW5/H/fd98lgZKSkpxxLSc0ub9SdPBivdRm7CWgCr0ZngJwffusXBMVyiwghw+69T/Xz06OAXh6fQNgPN0oBQ6zBqtCZUSwEBECUYw7kFS5DlUXDkwFoi0MfI/xdBNbYRKZZsC1nFAWuZgMw9Zopl0TNwPGHYg+xLWccH55T+B7BL4HwPndlTJcRa7HcNCtE/gerdGMyfwdgNXnb42qd8Jex7BjVwF4XG0BsI++dtflYJ2A8TGM0mvWgI8fkfj74t6ImYewY1fpNWs8vIjwLYv1shId0CSMh1BuvQqTcGMBOVxVvcmzMgkI8go3EtDte9bw1AJFhacSUIXniVYgbuLzqj5RQFBE6xMFitz3RAG59UXsu4y2mn67sfvaFVF9KvrtRmj6r/+v+AYdB8epI2v0IQAAAABJRU5ErkJggg==","citizentrial_pickaxe_diamond.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABQklEQVR4nGNgGAWjYBSMdMBIimI5Sdn/5Fjy6PljnPYwUcvyaQ8fkaWXqBBANqD62VUM+eWPeOHsSLnPKHKtUtoofPTQIOgAmOVSG5bgVMMhYQdn/3hxCKe6ZwExGI4gOgooBdgsZ2AgIQQYGBgYfjq7Y1Wj2Tobzr5enYoip5gbi9Nykh0AA+jRAbOAEMDmABZyNEkxMJCcHXFlRZLKAQYG1BCR2rAE7nszaWYGBgYGhlNP/+LN91R1ADIwk2Ym2XIGBjJyAcwCM2lmhiJnEYosJ8sBcpKy/2HBDbOcEkCSA5Att9EQZDhy4z0DAwPp8U62A2CAWpaT5ACY76lpOdEOoJXlRDkAm+XUBHgdgJ7iYYBavifoABigRdATdAAt452gA5CDnhbxjgzw+ibERAFe7tPC90SBEBOF/+S2hocEAACD2ajPrBMoYAAAAABJRU5ErkJggg==","citizentrial_pickaxe_gold.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABQUlEQVR4nGNgGAWjYBSMdMBIimI5Sdn/5Fjy6PljnPYwUcvyaQ8fkaWXqBBANuDhSTcMecf/c+Ds/YwpKHLy5rtQ+OihQdABMMsPTRbAqSbB9BKcveC0Hk51drkfMBxBdBRQCrBZzsDAwMBCigHRpj+xS5oimDMXvUSRSo8Tx2k5AwMJUYAM0KMDZgEhgM0BBEMAexYSIDk74sqKJJUDDAyoIXJosgDc92bSzAwMDAwMp57+xZvvqeoAZGAmzUyy5QwMZOQCmAVm0swMRc4iFFlOlgPkJGX/w4IbZjklgCQHIFtuoyHIcOTGewYGBtLjnWwHwAC1LCfJATDfU9Nyoh1AK8uJcgA2y6kJ8DoAPcXDALV8T9ABMECLoCfoAFrGO0EHIAc9LeIdGeD1TYiJArzcp4XviQIhJgr/yW0NDwkAACaPqHJVa0SdAAAAAElFTkSuQmCC","citizentrial_pickaxe_iron.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABQklEQVR4nGNgGAWjYBSMdMBIimI5Sdn/5Fjy6PljnPYwUcvyaQ8fkaWXqBBANuDczasY8iHveeHsNYKfUeSM1LVR+OihQdABMMvnrVuHU02LlAmcXfPsDE51SUFBGI4gOgooBdgsZ2AgIQQYGBgYTF1dsap52zwXzhauTUaRy8zMxGk5yQ6AAfTogFlACGBzAAs5mhgYGEjOjriyIknlAAMDaojMW7cO7nszaWYGBgYGhlNP/+LN91R1ADIwk2Ym2XIGBjJyAcwCM2lmhiJnEYosJ8sBcpKy/2HBDbOcEkCSA5Att9EQZDhy4z0DAwPp8U62A2CAWpaT5ACY76lpOdEOoJXlRDkAm+XUBHgdgJ7iYYBavifoABigRdATdAAt452gA5CDnhbxjgzw+ibERAFe7tPC90SBEBOF/+S2hocEAABRJqcp6/sqegAAAABJRU5ErkJggg==","citizentrial_pickaxe_netherite.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABTElEQVR4nGNgGAWjYBSMdMBIimI5Sdn/5Fjy6PljnPYwUcvyaQ8fkaWXqBBANiAhKBVD/lBZLZxt19WMIrdg3WwUPnpoEHQAzHJdDX2car4u2Axncyf44lR3+cZFDEcQHQWUAmyWMzAwMLCQYsC//9gDTAWJffH6JRQ5fU09nJaT5AAGBgYGJkZIUkCPjssWckhqUPXALMcFCDoAm6t1NfRJzo64siJJ5QADA2qO0NXQh/vQTJqZgYGBgeHU07948z06oCgRogcvqZaT5QCYBWbSzAxFziIMMDY5lpPlADlJ2f+w4IZZTgkgyQHIlttoCDIcufGegYGBvKAnywEwQC3LSXIAzPfUtJxoB9DKcqIcgM1yagK8DkBP8TBALd8TdAAM0CLoCTqAlvFO0AHIQU+LeEcGeH0TYqIAr3ho4XuiQIiJwn9yW8NDAgAASZaq9B9ZMD4AAAAASUVORK5CYII=","citizentrial_pickaxe_stone.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABUElEQVR4nGNgGAWjYBSMdMBIimI5Sdn/5Fjy6PljnPYwUcvyaQ8fkaWXqBBANmDCnBkY8pN0vODsvCvbUOQKUjJQ+OihQdABMMujUpNxqjmRXA9nW8xtxKlu2ey5GI4gOgooBdgsZ2AgIQQYGBgYZNRVsaphW7gXzv4V74wiZ2dnh9NyBgYGBhZCDkAGT27eZmBgwIyOZRZyOPUsg+rBBQg6AEcWIjk74sqKJJUDDAyoURKVmgwPXjNpZgYGBgaGU0//4s33VHUAMjCTZibZcgYGMnIBzAIzaWaGImcRiiwnywFykrL/YcENs5wSQJIDkC230RBkOHLjPQMDA+nxTrYDYIBalpPkAJjvqWk50Q6gleVEOQCb5dQEeB2AnuJhgFq+J+gAGKBF0BN0AC3jnaADkIOeFvGODPD6JsREAV7u08L3RIEQE4X/5LaGhwQAANgcqBTYfwkmAAAAAElFTkSuQmCC","citizentrial_pickaxe_wood.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABQUlEQVR4nGNgGAWjYBSMdMBIimI5Sdn/5Fjy6PljnPYwUcvyaQ8fkaWXqBBANqAjXhNDflbmTjg7bbo7ilzFwusofPTQIOgAmOURlsI41ZzqPw9nmxUa4lS34vhbDEcQHQWUAmyWMzAwMLCQYoA0/z+scuxI7MPXXqPI2WqJ4rScgYGEKEAG6NEBs4AQwOYAgiGAPQsJk5wdcWVFksoBBgbUEImwFIb73kyamYGBgYHh1NO/ePM9OqAoEaIHPamWk+UAmAVm0swMRc4iDDA2OZaT5QA5Sdn/sOCGWU4JIMkByJbbaAgyHLnxnoGBgbygJ8sBMEAty0lyAMz31LScaAfQynKiHIDNcmoCvA5AT/EwQC3fE3QADNAi6Ak6gJbxTtAByEFPi3hHBnh9E2KiAK94aOF7okCIicJ/clvDQwIAAB2fqt8mpzqFAAAAAElFTkSuQmCC","citizentrial_shovel_diamond.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABRklEQVR4nO2WoW7CUBSGf2DJNLI0bZBDkpAqHgKBIjMzewaSvcDUzB4AQYPGIlCgalCEqTWBtJN7AtKp29xdLrf3wjmChF/2tvm+c/LfAHDPPUwJvaCwea/OCbeRIBUIvaAQ0NY8PnnGKiBDWvMYL1EXb/lWey6nRikgwAAwSTblWT54BgDsfw4nPJINyNNNkg1evz+svyUv4Ww3RrpaYLYbl8/kPpALqKVzDcs1VGPqwAM1bNR518LP5aoNuKxfNz1w5TVU7376Of13/rhcGOGkAkJCt3IWgdALishvoP/UxPrrF0l21L5nggMXllDA5UR+A0l2rASqcS6hDBfTA7gI7ixADXcWEKGCOwmopaOAWwvo4FSpFNA1HqCZvlKAo3ROAiJccKMAV+msBOTVU5dOjXGaYa9d/thwTG+VYa9t/F9/8/kD4gW3PjxaUtsAAAAASUVORK5CYII=","citizentrial_shovel_gold.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABPElEQVR4nO2WMY7CMBBFP7ASTQooI5RAyQFQKrTlnoBr7GmoaJE4BC3QYC5AhwJCaKvdIt0KQuXIOMaxYaZA4pexo/fG+lYCvPMOU+Iwyl321TnhLhKkAnEY5RK6GLdKz1gFVMhi3EI3SZCuv4zramqUAhIMAKkQxdrn9x8AYH86lHgkJ6BOlwoB/EfO75KX8JIF2C3nuGRB8UztA7mAXjrfsFxDPbYOfFDD6kFmhN/d/wzM5/hN0wNPXkP97k+mPzfrs03TCicVkBKmI2cRiMMoTzoNDPttrLa/EMezcZ8NDjxYQglXk3QaEMdzJVCPdwlVuJwewENwbwFquLeADBXcS0AvHQXcWcAEp0qlgKnxAM30lQIcpfMSkOGCWwW4SuckoB49den0WKcZDXrFx4ZjeqeMBj3rf/3L5wpQJ7YsH6YnEgAAAABJRU5ErkJggg==","citizentrial_shovel_iron.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABQ0lEQVR4nO2WMYrCQBSG/133AstWQRLExgUbi2DlKcQT7AFylC22SecR0i+WWilImoDTKChiYbEnkGw1YXacnczE9wrBv8wkfN97/IMCjzzClCgIS5f3njnhLhKkAlEQlhI6zbKrZ6wCKmSaZRj0e1iLwniu5olSQIIBIC9EdfYxHgMA9qfDFY9kA+p0eSHwdv50/pa8hF2RYDf/Rlck1TO1D+QCeul8w3IN9dg68EIN2/a+jPD/ctMGfNZvmh648Rrqdz9N0z/nq9nMCicVkBKmlbMIREFYDtstjN5fsdj8YHm8GN+zwYGGJZRwNcN2C8vjpRaox7uEKlxOD6AR3FuAGu4tIEMF9xLQS0cBdxYwwalSK2BqPEAzfa0AR+m8BGS44FYBrtI5Cairpy6dHus0k7hT/dhwTO+USdyx/q+/+/wCHWO5Vq+8UB4AAAAASUVORK5CYII=","citizentrial_shovel_netherite.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABVElEQVR4nO2XMU7DMBSGv7RcADFVVauOAalkoMrEKVD3sjCycAPO0BP0GMwwReoQKpVsSKCKqeIEJUyOjOWmdvI8IPWXssROvv89/3YUOOqoQBr2BqXLvE5IuIuJKAQYYBwnrIq8Gvv4+rSyxDpgwq8uUm5v7qzjuk6kDOhggOU6q+7pnTAl0gG9uuU64/Hhx/lZ8RDOZ1ven5+Yz7bVvXGcAPZlaG1AvVRBfBVkG5pSGbDtBNEQAtwvzqzwfWrVAZ/27zsHWh1E5t7P317/jHeishYOghlYFTnJ+SWdqKwuFzXuwLA3KNN+l+v4lJfim2yzs86rqx4ahlDBdaX9LtlmdxBoynsJdLiqHmgE9zYgDfc2oCQF9zJghk4C7mzABpfSQQO2xINM9QcNhAidlwGlUPBaA6FC52RAb7106EzVVjOdjKovSojqnTSdjErXv5x/qV8O2q8pW60+VwAAAABJRU5ErkJggg==","citizentrial_shovel_stone.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABPklEQVR4nO2WvYrCQBSFj6svYBkkQax8ADfb2FsLVraiz2Mp/rS+Q9q4jckL7CIo+IPlPoFkq9FxHCczem8heMrMwPfdyxkI8M47TAk8P7O598EJt5EgFQg8PxPQbr93841VQIZ0+z2EX58YTkfaczkFSgEBBoBkmZ7P5pMZAGB73N3wSDYgT5csU7Trqek6vYCcQS3CZhFhUIvO3+Q+kAuopXMNyzNUY+pAiRo2Xre08Ht5agMu69dNDzz5DNW3H8fx1fn+d2WEkwoICd3KWQQCz8/CShHNehnfP39IDiftPRMceLCEAi4nrBSRHE65QDXOJZThYnoAD8GdBajhzgIiVHAnAbV0FHBrAR2cKrkCusYDNNPnCnCUzklAhAtuFOAqnZWAvHrq0qkxTtNpVC//egzTW6XTqBr/618+/+3OtaauCIR5AAAAAElFTkSuQmCC","citizentrial_shovel_wood.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABWklEQVR4nO2XMUvDQBiGH1OXjlIUSmnpJOrkUAoV/QudOtTJqdCf4k/wJ3R2c65Q6NRJpIugBKFSpJNTidOF87gmd8l3g9AXsuQued7vu/cuBPbaK5Ba9WbiMi8KCXcxcRACDDDs1ZjM1unY++eHlSXWARN+eXrC/d25dVzXoZQBHQywWK7Se3onTIl0QK9usVxxO7pyflY8hON+lbfpE+N+Nb037NUA+zKUNqBeqiC+CrINTakM2HaCaAgBHh5/rPBdKtUBn/bvOgdKHUTm3p++fP0ZjzdRJhwEMzCZrbm5OCbeROnlosIdaNWbSbdR4frsiOfXb+bx1jovq3ooGEIF19VtVJjH21ygKe8l0OGqeqAQ3NuANNzbgJIU3MuAGToJuLMBG1xKuQZsiQeZ6nMNhAidlwGlUPBMA6FC52RAb7106ExlVjPotNOvXYjqnTTotBPXv5x/qV+TD7DBl6QdAQAAAABJRU5ErkJggg==","citizentrial_sword_diamond.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABjElEQVR4nO2TsU7CUBSGf8SEkbEppH0CZkJcGJrI6ghJR17AV/ABXIwDiQmDfQBWBoZOCgsLmxtEiaPdmmiOgznN9doL3PYYB/mn3rQ93/+fcy5w1FH/Qb7rkend6V+BWSe/BfZdjxqTaO+34gY4tQpfbzcVaY4R7rsedeYxjSghPu/6R6wDavKH9AbjxVKq9OEGOvOYnHBInXl8UHoAEJkNg9Kgh6f3R7TiNwCHzb70CHT4+eVt2ZJ2cN/1yAmHlPRbVq1nFe5A3nV7uQgB2F27QjugJiwyd1XWHciDl5m7lQETvEjrCxmQhltJ3fgRJZT0W9YbnydjB9TCOmQwOMvmXjZ5rgEGOuGQ9s29rHLd+65HadDLzrXZFGnQw9X9NcaLpejcfxTQEzO8NpuiMYnEl87YAX5uN6tYPH9kJiThRgNsot2sZmc2AQCv0Z2YAeMS6nBV+nKW0bckelFuvyp9OcWv4apbx6pbB/CVfL3dVFQI74EEPNeAKhWgGmETEto5AlNC3/VI6iZ8Al+y9CGGS2HOAAAAAElFTkSuQmCC","citizentrial_sword_gold.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABfUlEQVR4nO2Vv07CUBTGP8SExAWmJg1pGV1cWzd5Apzc+gyuJrwAPgAsria8gKObbJaVxbEQQ2QwGqcOpg7kNIdrb//cHuIg39I0vbe/73zn3BY46KD/INd2Et2z478Ck472BXZtJ5mNO4VrxQ1Q1Ry+XK8auvWiLeDwnu+jd/5YuEcsgR24dYooDEvtE23BbNzB3f0bos0LLq4/AOTHDwC5D8uKqg+8GMMTC2dPn6XggEACKvz9qlpNtQxkwctGX9tA1nGrCgcMZ4B/4Uz6zlU5gSx41b4bG9DBTaI3MiANr2SAT/xoMgBgNnSlDfC41d/q181z2vc6cK0BAg4vraSo73WlTSDw4l/X0WQg0vdcA1TxdN4CXQMvxnTeQhSGonBA8yHisfvdJsLX79SEJFxrgEz43WZ6TyYA4PZhI2ZAO4QqnEsdzjraqUR9KcXPRSkA2/kQP4aLfhuLfhvAtvLletXgED6cezkFXBzAjZAJCeW2QFehazuJ1En4ASpz0/xGvqW6AAAAAElFTkSuQmCC","citizentrial_sword_iron.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABhUlEQVR4nO1VoW4CQRQcSlOL3pDdL8AeogbR7A+AQSFO1PY76ipqaiCpLz9wmCoSziBAYCENBtOTbZpX0Tyy3dzSu9ulFWXM3ebu3sx7My8HnHDCf4ASklzPzv+KmHF2LGIlJA3H4x/fDS6AuzbJ19tNLTSPk1wJSZNpSrssIz4f+ibYBMzOr95vMV+uQpUuLmAyTak3iGkyTQt1DwBBvGGiSGuM3mZoPb8CKOa9twU2+exm5FuyHLkSknqDmLJ+q9ToGZUnkLducbcLoNzaVcqA2WEV302UnkAe+a/5zv76+u4t4M/Jd1lGWb8VhNyZAbOwTXJxfbn33fdHkyuACXuDmFyh45XzRa56JSRFWu/PaZIg0hoP93eYL1eV9r0w7KSb12OEzjkBvm8365i9fCDSGmmSAAjbubOQEpLazfr+zCIA4OlxGEyAM4Q2uQk7nD741oldlMdvwg5n8DVcdBpYdBoAvjpfbzc1k4RzEII8V4AJk8AUwiJC4KAFrg6VkBRqEz4BtDAAt8jBlZ8AAAAASUVORK5CYII=","citizentrial_sword_netherite.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABc0lEQVR4nO2WsU7DMBRFr1MGJroSlUSMESLKgJS1fABbJ9aqn8CO+jvM/ABrJIZCVZhbVRUDAxtLawZk83DiNLEfMNC7ZEicc999z06AnXb6D4rDSNru7f0VWCn4KXAcRjJNsq3PshtQVVP4fLUQv2KAws9Ocjw+T7auYTNA4bfjfdzPikbrWBNIkwyTpwdcXL/r6uviB4Dam02lqt9Igdn5AU7v3hrBAYYETPjly3Gr9V4GquBNo/c2ULXd2sIBxxmgJ5xL36laJ1AFb9t3ZwM2uEv0Tga44a0M0IkfDkYA3IausQEat/lZvXq90X33gQOW/wEFPDqMZSC+2FXR+8qawEaK0nU4GLH0nar0AnPSAyH1NU0yVnilAdNE3uugWK61CU44YGmBAuS9jjahklAt4ZI1AQUHgGK5BoBv8EBI/hkwt5uKn4rbRKkF034X034XwGfl89VCUIiaA64Eak9CCqBG6Nngq9oW2CqMw0hy7YQPPwfhIF2mh1EAAAAASUVORK5CYII=","citizentrial_sword_stone.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABgklEQVR4nO2Vv07CUBTGP8Sd1Ya2W+3Cak0YhBAewcGwEp5AjfEF9CGMk4mjG4mT0Q4mlLULYQMMiZvu5jqQ0xxLb//diw7yLU1p7/195zvnFmCrrf6DbMMSsme7fwUm7WwKbBuW6A36me9qN0BVc/hsOa/8igEO9w4PcH9zm7lGmwEOv+6GCEbjXOu0DmFv0Ifv+7jEUVR9WvwAkPowr6h603XwuPeOxstHLjigoQVx+NX+caH1SgaS4HmjVzaQdNyKwoGSM8C/cGX6zlU4gSR40b6XNiCDl4m+lAHd8EKiP5hmuyMehkPxedIQ9JvKvtIE+MZxSPfuIuq7auWJBgjYbHdEVt9VJU3AdJ2169n5qfa+rxmgiheTKehqug4WkymC0Vj70CVuwmP36lUEb1+RCZ1wqQEy4dWr0T2ZAIDX5ydtBqRDGIdzxYdTRT8qiW9K8XNRCsBqPrQfw7BVQ9iqAVhVPlvOKxzCh3Mjp4CLA7gRMqFDqS2QVWgbltB1Er4B+cnWwO7+xRYAAAAASUVORK5CYII=","citizentrial_sword_wood.png":"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAABfUlEQVR4nO2WsU7CUBSGf4p7Y4gmzU07GWPEgYmkg+EFHBh5CRIfwoU38RUcjYMJEwNxYDKQKwnGoasJrYM59VB6S3t70EH+hQHK95//v+cCcNBB/0GB5yem947+Ckxy9gUOPD8ZhK2dnxU3QFNz+Hy5aPyKAQ7vnJ/i/vlj5zNiBjh8dHuGyWxV6jljNDYGBmELTy/vuL48Sacvil/MAE2v3BgPnWNcPUal4IBABVn43We1za5lIA9eNvraBvLWrSocsDwD/Iaz6Z2rcgJ58Kq9WxswwW2itzIgDa9kgJ/4Yb8NwO7QlTbA487+rN68vqW914EDhv8DBAwvVKKjH4950deVMQHlxluvw35bpPdCAzQ9Ta4jB8qNoSMHk9lKFA4YLiLeeVc1Mdbr1IQkHDBUQICuaqYmKAmqRErGBAgOAGO9BoANuI4ckSQ2viC7bhQ/l7SJrQqmPRfTngvge/L5ctHgEH4497IFXBzAjfC7oa4KKzBNGHh+IrUJX8j2208loRtCAAAAAElFTkSuQmCC"}

CMDS = {"pickaxe":260101,"axe":260102,"sword":260103,"shovel":260104}
STAGES = {"wood":"wooden","stone":"stone","iron":"iron","gold":"golden","diamond":"diamond","netherite":"netherite"}

def main():
    if not BASE_ZIP.exists():
        raise SystemExit(f"Missing base pack: {BASE_ZIP}")

    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "pack"
        root.mkdir()
        with zipfile.ZipFile(BASE_ZIP, "r") as z:
            z.extractall(root)

        textures = root / "assets/aicraft/textures/item"
        models = root / "assets/aicraft/models/item"
        items = root / "assets/minecraft/items"
        textures.mkdir(parents=True, exist_ok=True)
        models.mkdir(parents=True, exist_ok=True)
        items.mkdir(parents=True, exist_ok=True)

        for name, encoded in TEXTURES.items():
            (textures / name).write_bytes(base64.b64decode(encoded))

        for tool in CMDS:
            for stage in STAGES:
                model = {
                    "parent": "minecraft:item/handheld",
                    "textures": {"layer0": f"aicraft:item/citizentrial_{tool}_{stage}"}
                }
                (models / f"citizentrial_{tool}_{stage}.json").write_text(
                    json.dumps(model, indent=2), encoding="utf-8"
                )

        for tool, cmd in CMDS.items():
            for stage, prefix in STAGES.items():
                item_name = f"{prefix}_{tool}"
                path = items / f"{item_name}.json"
                if path.exists():
                    data = json.loads(path.read_text(encoding="utf-8"))
                else:
                    data = {
                        "model": {
                            "type": "minecraft:range_dispatch",
                            "property": "minecraft:custom_model_data",
                            "index": 0,
                            "fallback": {"type": "minecraft:model", "model": f"minecraft:item/{item_name}"},
                            "entries": []
                        }
                    }

                model = data.get("model", {})
                if model.get("type") != "minecraft:range_dispatch" or model.get("property") != "minecraft:custom_model_data":
                    data = {
                        "model": {
                            "type": "minecraft:range_dispatch",
                            "property": "minecraft:custom_model_data",
                            "index": 0,
                            "fallback": model or {"type": "minecraft:model", "model": f"minecraft:item/{item_name}"},
                            "entries": []
                        }
                    }

                entries = [e for e in data["model"].setdefault("entries", []) if e.get("threshold") != cmd]
                entries.append({
                    "threshold": cmd,
                    "model": {"type": "minecraft:model", "model": f"aicraft:item/citizentrial_{tool}_{stage}"}
                })
                entries.sort(key=lambda e: e.get("threshold", 0))
                data["model"]["entries"] = entries
                path.write_text(json.dumps(data, indent=2), encoding="utf-8")

        (root / "AIcraft_CHANGELOG_0_9_7_CITIZENTRIAL_RELIC_TOOLS.txt").write_text(
            """AIcraft ResourcePack 0.9.7 – CitizenTrial Relic Tools
- Vier eigenständige CitizenTrial-Designs:
  260101 Hammer des vergessenen Steins (Pickaxe)
  260102 Axt der alten Wurzeln (Axe)
  260103 Klinge der ersten Glut (Sword)
  260104 Spaten der vergessenen Erde (Shovel)
- Jede Prüfung entwickelt die Optik passend zu WOOD, STONE, IRON, GOLD, DIAMOND und NETHERITE weiter.
- Vanilla-Fallback bleibt erhalten: Spieler ohne Pack sehen das normale Material-Werkzeug.
- Bestehende BirthdayRelics-, Elytra-, Stargate-, Medaillen- und Lodestone-Zuordnungen bleiben erhalten.
""", encoding="utf-8"
        )

        mcmeta = root / "pack.mcmeta"
        meta = json.loads(mcmeta.read_text(encoding="utf-8"))
        meta["pack"]["description"] = "AIcraft ResourcePack 0.9.7 – CitizenTrial Relic Tools"
        mcmeta.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        for path in root.rglob("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

        temp_out = Path(td) / NEW_ZIP.name
        with zipfile.ZipFile(temp_out, "w", zipfile.ZIP_DEFLATED) as z:
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    z.write(path, path.relative_to(root))

        shutil.copy2(temp_out, NEW_ZIP)
        shutil.copy2(temp_out, BASE_ZIP)
        shutil.copy2(temp_out, SERVER_ZIP)

        sha1 = hashlib.sha1(temp_out.read_bytes()).hexdigest()
        SERVER_SHA1.write_text(sha1 + "\n", encoding="utf-8")

        print(f"Built {NEW_ZIP}")
        print(f"Refreshed legacy URL file {BASE_ZIP}")
        print(f"Refreshed stable server pack {SERVER_ZIP}")
        print(f"SHA1: {sha1}")

if __name__ == "__main__":
    main()
