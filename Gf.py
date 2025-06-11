#!/bin/bash

echo "🔧 Starting Lenovo E41-25 Performance Setup..."

# 1. Install essential packages
sudo pacman -Syu --noconfirm
sudo pacman -S --noconfirm i3 rofi dmenu picom feh lxappearance papirus-icon-theme \
  bat btop fd ripgrep fzf neovim zoxide htop xarchiver networkmanager git

# 2. Enable NetworkManager
sudo systemctl enable NetworkManager
sudo systemctl start NetworkManager

# 3. Power saving (TLP)
sudo pacman -S --noconfirm tlp
sudo systemctl enable tlp
sudo systemctl start tlp

# 4. Set up zram
sudo pacman -S --noconfirm systemd-zram-generator

sudo bash -c 'cat > /etc/systemd/zram-generator.conf <<EOF
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
EOF'

sudo systemctl daemon-reexec

# 5. Boot cleanup
sudo systemctl disable bluetooth.service
sudo systemctl disable cups.service
sudo systemctl disable lvm2-monitor.service

# 6. Network tuning
sudo bash -c 'cat > /etc/sysctl.d/99-sysctl.conf <<EOF
net.ipv4.tcp_fastopen = 3
net.core.default_qdisc = fq
net.ipv4.tcp_congestion_control = bbr
EOF'

sudo sysctl --system

# 7. Shell aliases
echo "alias cat='bat'" >> ~/.bashrc
echo "alias top='btop'" >> ~/.bashrc
echo "alias vim='nvim'" >> ~/.bashrc

# 8. Optional: Dotfiles setup
echo "Setting up dotfiles Git alias..."
git init --bare $HOME/.dotfiles
echo "alias config='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'" >> ~/.bashrc
source ~/.bashrc
config config --local status.showUntrackedFiles no

echo "✅ All done! Reboot to apply zRAM + boot service tweaks."
echo "💡 On next login, run: startx or setup your i3/xinit."
