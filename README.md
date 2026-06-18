# Mini Petri

<img alt="render of mini petri with case" src="https://cdn.hackclub.com/019ebd9e-28c0-7a16-b5fd-40f4e45ab089/render.png" />

Mini Petri is a simulator that runs Conway's game of life. I got this idea during a particularly boring class when I wanted something satisfying to look at.

### Highlights

- runs on a Xiao RP2040 and 3 AA batteries
- 8x8 led dot matrix to give enough space for your life to grow
- 9 buttons to easily edit and play simulations 
- portable and pocket sized (8x13x5 cm)

Here is a banana for scale.

<img alt="banana scale" src="https://cdn.hackclub.com/019ebd9e-2131-7403-8f3b-dd07944d9c85/banana_scale_top.png" />


## Build your own

<img alt="render of mini petri pcb" src="https://cdn.hackclub.com/019ebd9e-238c-7ad9-8462-db0403a8e648/pcb_render.png" />

Want a Mini Petri? Download the files in the "build" folder. Order the board with gerbers.zip. The case has 3d models in 2 different formats, STL and STEP. Use screws to attach the lid to the case. Load main.py onto the Xiao. That's it :)

I will add a more detailed assembly guide once I build it myself. 

## How to use

First, insert batteries and turn it on with the switch.

There are 9 buttons in a 3x3 arrangement for editing the starting positions and playing the simulation.

<img alt="diagram of how it's used" src="https://cdn.hackclub.com/019ebd9e-269b-7182-b7a7-4ae003a810a8/ux_layout.png" />


## Conway's game of life

Conway's game of life is a simulation that uses a simple set of rules to create interesting patterns.

The rules:

each cell has 9 neighbors. A filled in or lit up cell is alive (depending on what you are using to simulate it).

each generation, cells are born and die based on their neighbors. 

A living cell with less than 2 living neighbors dies the next generation. If it has 2-3 living neighbors, it survives. If it has more than 3 living neighbors, it dies, as if by overpopulation.

A dead cell can be born if it has exactly 3 living neighbors, as if by reproduction.

With time, you can create really interesting structures such as "spaceships" that glide on indefinetly, "still life" structures where cells are never born and die, and "wires" that can transfer signals in the form of cells.

<img width="156" height="126" alt="image" src="https://github.com/user-attachments/assets/d1a3b115-fcda-4b54-b62c-3f818eecaa61" />
<img width="162" height="163" alt="image" src="https://github.com/user-attachments/assets/01b6abea-c71a-4bc5-aa15-bf2e63a4a877" />
<img width="156" height="155" alt="image" src="https://github.com/user-attachments/assets/889a8f63-9751-417f-aef5-d04aec274d68" />

## Wiring
<img alt="banana scale" src="https://cdn.hackclub.com/019ebd9e-2ac2-7a7e-a371-bc477feb3332/schematic.png" />

## Other

Fallout reviewers: I made 2 versions of the zine, one for the left page and one for the right page! Hope that doesn't mess up something :')

find the onshape file here: https://cad.onshape.com/documents/10df214650d10753392c4f94/w/a985103637e720fab81ebfaa/e/7306bce063d86ed0c220e238

Zine:
<img alt="fallout zine" src="https://cdn.hackclub.com/019eccb8-3240-7ec4-8610-0f833d99b25c/zine.png" />

Left page:
<img alt="fallout zine" src="https://cdn.hackclub.com/019eccba-d997-7439-a8dc-3594c55dce50/left_page.png" />

Right page:
<img alt="fallout zine" src="https://cdn.hackclub.com/019eccba-dc19-7d5d-ae9a-f11daacda3b1/right_page.png" />

