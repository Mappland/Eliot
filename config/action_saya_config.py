import pkgutil
from pathlib import Path
from creart import create
from graia.saya import Saya

SAYA_CONFIGPATH=Path("/root/Eliot/config/saya.yaml")
saya = create(Saya)

def write_saya():
    with open(SAYA_CONFIGPATH,"w",encoding="utf-8") as f:
        f.write("Saya:\n")
        with saya.module_context():
            for module_info in pkgutil.iter_modules(["/root/Eliot/saya/"]):
                try:
                    f.write("  ")
                    f.write(module_info.name)
                    f.write(":\n    Disabled: false\n    Description:\n")
                    
                except KeyError:
                    pass

write_saya()
print("done")