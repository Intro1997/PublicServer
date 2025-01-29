## Usage

### Get Sprite Boxes

You can get all sprite boxes coordinate:

```python
from tools.sprite_splitter import AlphaSpriteSplitter

img_path = "path/to/your/image"
splitter = AlphaSpriteSplitter(img_path)
# default use SplitterAlgorithm.SPRITE_SCAN
# you can use SplitterAlgorithm.EDGE_DETECT by
# splitter.get_sprite_boxes(SplitterAlgorithm.EDGE_DETECT)
boxes = splitter.get_sprite_boxes()
print(f"box 0 left corner: {boxes[0].left_top_corner}")
print(f"box 0 right corner: {boxes[0].right_bottom_corner}")
```

### Save Splitted Sprites

You can save all splitted sprites to folder(in PNG format):

```python
from tools.sprite_splitter import AlphaSpriteSplitter

img_path = "path/to/your/image"
splitter = AlphaSpriteSplitter(img_path)
splitter.save_sprites("./output")

# you also can specify the prefix of output sprite file
# and the algorithm
# "sprite_file_prefix" means "./output/sprite_file_prefix_0.png"
# splitter.save_sprites("./output", "sprite_file_prefix", SplitterAlgorithm.EDGE_DETECT)
```

You also can split sprite by given boxes:

```python
from tools.sprite_splitter import AlphaSpriteSplitter

img_path = "path/to/your/image"
splitter = AlphaSpriteSplitter(img_path)
boxes = splitter.get_sprite_boxes()
splitter.save_sprites_by_boxes("./output", boxes)

```

### Show Split Result

You can show split result and specify color(in integer, not float):

```python
from tools.sprite_splitter import AlphaSpriteSplitter

img_path = "test/assets/multiple_test0.png"
splitter = AlphaSpriteSplitter(img_path)
# you can use SplitterAlgorithm.EDGE_DETECT by
# splitter.show_split_result((255, 0, 0, 255), SplitterAlgorithm.EDGE_DETECT)
splitter.show_split_result((255, 0, 0, 255))
```

You also can specify boxes:

```python
from tools.sprite_splitter import AlphaSpriteSplitter


img_path = "test/assets/multiple_test0.png"
splitter = AlphaSpriteSplitter(img_path)
splitter.show_split_result_by_boxes(splitter.get_sprite_boxes(), (255, 0, 0, 255))
```
