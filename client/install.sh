python3 -m venv .venv
source .venv/bin/activate
pip install tk
sudo cp -r ./config.json ~/.config/FileSharing/
sudo cp -r ./Notepad.png ~/.config/FileSharing/
sudo cp -r ./icon.png ~/.config/FileSharing/
sudo mkdir ~/.file-sharing
sudo mkdir ~/.file-sharing/cache
chmod +x ./run.sh
sudo cp -r ./FileShare.desktop ~/.local/share/applications/