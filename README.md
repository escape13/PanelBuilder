# PanelBuilder Blender add-on

This add-on allows you to make Paneled surfaces in one click! Instead of applying array modificators, putting up the walls and guessing to make the padding right you can just type in all desired modifications when creating one of this add-on's two meshes.

## Installation

1. Clone panelbuilder.py to your computer.
2. Open Blender.
3. Go to Edit -> Preferences -> Add-ons.
4. Click 'Install' and navigate to the directory where you have saved panelbuilder.py.
5. Click 'Install add-on'.
6. Check the box 'Add Mesh: PanelBuilder'.

## Functionality 

A new type of mesh will appear in the menu when you'll try to create a mesh (Shift + A): **Panels**

![new mesh type](https://github.com/escape13/PanelBuilder/blob/master/images/addMesh.png?raw=true)

### Let's start with **PaneledWall**
**PaneledWall** automatically adjusts to the user's input and retains its consistensy no matter the value given.
![Paneled wall](https://github.com/escape13/PanelBuilder/blob/master/images/PaneledWall.png?raw=true)
As you can see from the settings window, **PaneledWall** has 7 properties:

1. **Panel X Axis** is the total number of panels along the X axis
2. **Panel Z Axis** is the total number of panels along the Z axis
3. **Horizontal Padding** controls the spaces between horizontally placed panels
4. **Vertical Padding** controls the spaces between vertically placed panels
5. **Width** controls the width of a panel element
6. **Thickness** controls the thickness of a panel element
7. **Height** controls the height of a panel element

### Now, PaneledBlock
**PaneledBlock** is a combination of **PannelledWall** objects and it also automatically adjusts to the user's input and retains its consistensy no matter the value given.
![Paneled block](https://github.com/escape13/PanelBuilder/blob/master/images/PaneledBlock.png?raw=true)

**PaneledBlock** has 8 properties:

1. **Panel X Axis** is the total number of panels along the X axis
2. **Panel Y Axis** is the total number of panels along the Y axis
3. **Panel Z Axis** is the total number of panels along the Z axis
4. **Horizontal Padding** controls the spaces between horizontally placed panels
5. **Vertical Padding** controls the spaces between vertically placed panels
6. **Width** controls the width of a panel element
7. **Thickness** controls the thickness of a panel element
8. **Height** controls the height of a panel element
