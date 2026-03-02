import json
import os

path = r'E:\Ip\autovideo\projects\day4\script.json'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

replacements = [
    ("assets/manual/05_discriminative.png", "assets/manual/05_discriminative_icon.png"),
    ("assets/manual/07_generative_role.png", "assets/manual/07_generative_role_icon.png"),
    ("assets/manual/10_examples_gpt_doubao.png", "assets/manual/10_examples_gpt_doubao_icon.png"),
    ("assets/manual/13_history_eliza.png", "assets/manual/13_history_eliza_icon.png"),
    ("assets/manual/14_history_eliza2.png", "assets/manual/14_history_eliza2_icon.png"),
    ("assets/manual/19_gan_roles.png", "assets/manual/19_gan_roles_icon.png"),
    ("assets/manual/22_transformer_impact.png", "assets/manual/22_transformer_impact_icon.png"),
    ("assets/manual/23_transformer_extensions.png", "assets/manual/23_transformer_extensions_icon.png"),
    ("assets/manual/27_ddpm_advantage.png", "assets/manual/27_ddpm_advantage_icon.png"),
    ("assets/manual/29_models_stable_midjourney.png", "assets/manual/29_models_stable_midjourney_icon.png"),
    ("assets/manual/33_sora_veo_keling.png", "assets/manual/33_sora_veo_keling_icon.png"),
    ("assets/manual/37_movie_generation.png", "assets/manual/37_movie_generation_icon.png")
]

for old, new in replacements:
    text = text.replace(old, new)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Replacement complete.")
