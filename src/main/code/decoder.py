
"""
Map the numbers to the corresponding relative path of the elements
"""
path_to_images = "../motif/"
image_pattern_list = ["bajiaojing.png",
                      "fanggewen.png",
                      "fengchewen.png",
                      "gongziwen.png",
                      "haitangwen.png",
                      "huajiewen.png",
                      "huiwen.png",
                      "huiwen1.png",
                      "jingziwen.png",
                      "liujiaojing.png",
                      "meihuawen.png",
                      "taofangwen.png",
                      "wanbuduan.png",
                      "yaziwen.png",
                      "yuntouwen.png",
                      "yunwen.png",
                      "xiangyun.png",
                      "qianwen.png",
                      "tetris.png"]

image_pattern_list = [(path_to_images + name) for name in image_pattern_list]

path_to_frame = "../frame/"
frame_list = ["nothing.png",
              "circle.png",
              "hexagon.png",
              "square.png",
              "fan.png",
              "vase.png"]
frame_list = [(path_to_frame + f) for f in frame_list]

path_to_center = "../centre/"
center_list = ["nothing.png",
               "yuanshou.png",
               "shou.png",
               "circle.png",
               "hexagon.png",
               "square.png",
               "rhombus.png",
               "rhombus2.png",
               "flower.png",
               "fan.png"]
center_list = [(path_to_center + m) for m in center_list]

"""
Do NOT reference/ import from transformation.py as this raises circular import issue.
The variables are declared as placeholders, only the length of the list is used,
actual function is mapped in transformation.py. 
"""
rotation = 0
diagonal_translation = 1
horizontal_translation = 2
vertical_translation = 3
transformation_list = [rotation,
                       diagonal_translation,
                       horizontal_translation,
                       vertical_translation]


"""
line_transformation_list = [transformation_old.rotation,
                            transformation_old.horizontal_translation,
                            transformation_old.vertical_translation]

reflection_list = [transformation.reflection_along_x,
                   transformation.reflection_along_y,
                   transformation.reflection_line_pos,
                   transformation.reflection_line_neg]
"""