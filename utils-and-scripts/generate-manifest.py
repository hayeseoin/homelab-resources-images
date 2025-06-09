#!/bin/python3
import yaml
import os

work_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(work_dir)

s3_bucket = 'hayeseoin-homelab-resources-images'

not_distros = [
    'base-images',
    'generate-manifest.py',
    'manifest.yml',
]
exclusions = [
    'build-meta.yml',
    ]
manifest = {}

distros = [entry for entry in os.listdir(work_dir) if entry not in not_distros]

for distro in distros:
    manifest[distro] = {}
    for platform in os.listdir(distro):
        filename = ''
        dir_path = os.path.join(work_dir, distro, platform)
        files = os.listdir(dir_path)
        for f in files:
            if f in exclusions:
                continue
            if f == '':
                continue
            filename = f
        if filename == '':
            continue
        s3_uri = f's3://{s3_bucket}/{distro}/{platform}/{filename}'
        manifest[distro].update({platform: {'s3_uri': s3_uri }})
        
    
with open('manifest.yml', "w") as f:
    yaml.dump(manifest, f, default_flow_style=False, sort_keys=True)
