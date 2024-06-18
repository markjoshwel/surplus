"""
script to copy shell scripts into the docs folder for publishing

src/surplus-on-wheels/s+ow               ->  docs/spow.sh
src/surplus-on-wheels/termux-s+ow-setup  ->  docs/termux.sh
src/spow-whatsapp-bridge/install.sh      ->  docs/whatsapp.sh
src/spow-telegram-bridge/install.sh      ->  docs/telegram.sh
"""
from pathlib import Path
from shutil import copyfile

repo_root: Path = Path(__file__).parent.parent.parent
docs_path: Path = repo_root.joinpath("docs")

copy_map: dict[Path, Path] = {
    repo_root.joinpath("src/surplus-on-wheels/s+ow"): docs_path.joinpath("spow.sh"),
    repo_root.joinpath("src/surplus-on-wheels/install.sh"): docs_path.joinpath("termux.sh"),
    repo_root.joinpath("src/spow-whatsapp-bridge/install.sh"): docs_path.joinpath("whatsapp.sh"),
    repo_root.joinpath("src/spow-telegram-bridge/install.sh"): docs_path.joinpath("telegram.sh"),
}

for target, destination in copy_map.items():
    copyfile(target, destination)
    print(f"{target}\t->\t{destination}")
