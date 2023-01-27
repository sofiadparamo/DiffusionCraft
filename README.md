# DiffusionCraft

This runs stable diffusion v1.5, grabs images from an active Minecraft Window and runs an Image2Image pipeline using a text description to generate real-time art from the game.

# Requirements:
- Windows 11 or 10
- Python 3.9 installed (From the Microsoft store)
- NVIDIA GPU with CUDA 11.4 and 8gb of vram
- Minecraft Java Edition
- Bandwidth internet connection to download the models

# Installation:

1. Install Python 3.9 from https://www.python.org/downloads/
2. Install the latest NVIDIA drivers from https://www.nvidia.com/Download/index.aspx?lang=en-us
3. Install CUDA from https://developer.nvidia.com/cuda-downloads
4. Create virtual environment and install requirements
    - `python -m venv env`
    - `venv\Scripts\activate`
    - `pip install -r requirements.txt`
5. Open Minecraft and set the resolution to 768x768
6. Run the script
    - `python diffusioncraft.py`

# Tips

Best prompts are:
- `An isometric drawing of a house, concept art, trending on artstation`
- `crochet bunny with a scarf`
- `cinematic mountainscape highly detailed, epic, with old town by greg rutkowski`
- `colourful watercolor of astronaut in space surrounded by planets and stars`
- `god prince face close-up portrait ram skull abstract 3d composition. jellyfish phoenix head, nautilus, orchid, skull, betta fish, bioluminiscent creatures, intricate artwork by Tooth Wu and wlop and beeple. octane render, trending on artstation, greg rutkowski very coherent symmetrical artwork. cinematic, hyper realism, high detail, octane render, 8k`
- `realistic photo of a human face, portrait, sketch`
- `detailed photo of a fan-palm plant in a junglescape`
- `panoramic photo of a neon cyberpunk city skyline, detailed, high resolution, infocus`
- `octane render of a cute retro robot`
- `a photorealistic hand`
- `a beautiful storybook painting of a vintage Schwinn bicycle with a basket of flowers on the front propped up against a wall, anime style by Grzegorz greg rutkowski and Studio Ghibli, nostalgic heart-warming, trending on artstation hq`
- `realistic skull with horns, portrait, powerful, intricate, elegant, volumetric lighting, scenery, digital painting, highly detailed, artstation, sharp focus, illustration, concept art, ruan jia, steve mccurry`
- `HD nature photography of ladybug`
- `isometric photo of a realistic sunlit cozy refreshing outdoor summer reflective indoors poolside lounge, 3d octane render, isometric angle`
- `photo of a sock puppet, muppet, highly detailed, 4k`
- `complex 3 d render hyper detail portrait of a mechanical cyborg robot, sci fi, full body, intricate, art by kazuhiko nakamura and hajime sorayama, 8 k octane detailed render, post processing, extremely hyperdetailed, intricate futuristic mechanic parts, maya, dark background, sharp focus, blender, cinematic lighting masterpiece, trending on artstation`
- `realistic full body, Portrait painting of Tom Hiddleston as Cyborg Power Ranger, made by Michaelangelo, physical painting, Sharp focus,digital art, bright colors,fine art, trending on Artstation, unreal engine`

Original Idea by: [ThoseSixFaces](github.com/TSFSean)
