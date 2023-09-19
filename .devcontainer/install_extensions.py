import os

# VSIX dosyalarının bulunduğu dizin
vsix_dir = "/tmp/"

# VSIX dosyalarını al
vsix_files = [f for f in os.listdir(vsix_dir) if f.endswith(".vsix")]

# Her VSIX dosyasını yükle
for vsix_file in vsix_files:
    os.system(f"code --install-extension {os.path.join(vsix_dir, vsix_file)}")