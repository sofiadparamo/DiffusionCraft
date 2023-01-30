![DiffusionCraft](https://user-images.githubusercontent.com/7455707/215052100-0e752612-9ede-401c-b61e-d62fbe5f6c19.png)

This runs stable diffusion v1.5, grabs images from an active Minecraft Window and runs an Image2Image pipeline using a text description to generate real-time art from the game.

# Requirements:
- Windows 11 or 10
- Python 3.9 installed (From the Microsoft store)
- Minecraft Java Edition
- Bandwidth internet connection to download the models
- NVIDIA GPU with CUDA 11.4 and 8gb of vram
<details><summary>Don't meet the requirements?</summary>There are ways to run stable diffuson on <a href="https://huggingface.co/CompVis/stable-diffusion-v1-4/discussions/29#630e49a583f64e3516785431">AMD Video Cards</a> and even in <a href="https://www.assemblyai.com/blog/how-to-run-stable-diffusion-locally-to-generate-images/#how-to-install-stable-diffusion-cpu">CPUs without a graphics card</a>, however, I don't plan to support AMD Video Cards nor CPU generations. If you want to try for yourself, just be aware that this script only runs on Windows, and AMD support is mainly focused on Linux. Also, if you try running it on CPU with no graphics card you may have a really bad time waiting for 5 to 10 minutes just to get a frame, so it would be better if you tried another way, like a <a href="https://colab.research.google.com/drive/1hs5dYbPHVDv3AhkpZTGhck7H2E_4NBwZ?usp=sharing">Google Collab with stable diffusion</a> where you upload your own screenshots. This is mostly intended for advanced users in an effort to point you towards the right direction.</details>

# Installation and running:

1. Install Python 3.9 from https://www.python.org/downloads/
2. Install the latest NVIDIA drivers from https://www.nvidia.com/Download/index.aspx?lang=en-us
3. Install CUDA from https://developer.nvidia.com/cuda-downloads
4. Create virtual environment
    - `python -m venv venv`
5. Activate the virual environment
    - If you're on CMD, use ``.\venv\Scripts\activate.bat``
    - If you're on PowerShell, use ``.\venv\Scripts\Activate.ps1``
      - Keep in mind you should have enabled scripts in Windows PS
6. Install the requirements
    - `pip install -r requirements.txt`
5. Open Minecraft and set the resolution to 768x768
6. Run the script
    - `python diffusioncraft.py`

# Tips

You may play with the strenght and the camera distance from the objects.

You will find all the images you generated inside the `tmp` folder with the name of the seed you used.

Some good prompts are:
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

Original Idea by: [ThoseSixFaces](https://github.com/TSFSean)

Funding: [BobicraftMC](https://www.youtube.com/@BobicraftMC)
