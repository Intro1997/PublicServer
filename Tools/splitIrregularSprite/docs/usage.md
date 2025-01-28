## Usage

### Get Sprite Boxes

You can get all sprite boxes coordinate:

```python
from tools.sprite_spliter import AlphaSpriteSpliter

img_path = "path/to/your/image"
spliter = AlphaSpriteSpliter(img_path)
# default use SpliterAlgorithm.SPRITE_SCAN
# you can use SpliterAlgorithm.EDGE_DETECT by
# spliter.get_sprite_boxes(SpliterAlgorithm.EDGE_DETECT)
boxes = spliter.get_sprite_boxes()
print(f"box 0 left corner: {boxes[0].left_top_corner}")
print(f"box 0 right corner: {boxes[0].right_bottom_corner}")
```

### Save Splitted Sprites

You can save all splitted sprites to folder(in PNG format):

```python
from tools.sprite_spliter import AlphaSpriteSpliter

img_path = "path/to/your/image"
spliter = AlphaSpriteSpliter(img_path)
spliter.save_sprites("./output")

# you also can specify the prefix of output sprite file
# and the algorithm
# "sprite_file_prefix" means "./output/sprite_file_prefix_0.png"
# spliter.save_sprites("./output", "sprite_file_prefix", SpliterAlgorithm.EDGE_DETECT)
```

You also can split sprite by given boxes:

```python
from tools.sprite_spliter import AlphaSpriteSpliter

img_path = "path/to/your/image"
spliter = AlphaSpriteSpliter(img_path)
boxes = spliter.get_sprite_boxes()
spliter.save_sprites_by_boxes("./output", boxes)

```

### Show Split Result

You can show split result and specify color(in integer, not float):

```python
from tools.sprite_spliter import AlphaSpriteSpliter

img_path = "test/assets/multiple_test0.png"
spliter = AlphaSpriteSpliter(img_path)
# you can use SpliterAlgorithm.EDGE_DETECT by
# spliter.show_split_result((255, 0, 0, 255), SpliterAlgorithm.EDGE_DETECT)
spliter.show_split_result((255, 0, 0, 255))
```

You also can specify boxes:

```python
from tools.sprite_spliter import AlphaSpriteSpliter


img_path = "test/assets/multiple_test0.png"
spliter = AlphaSpriteSpliter(img_path)
spliter.show_split_result_by_boxes(spliter.get_sprite_boxes(), (255, 0, 0, 255))
```
