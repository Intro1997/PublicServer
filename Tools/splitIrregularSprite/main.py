from tools.sprite_splitter import AlphaSpriteSplitter


img_path = "test/assets/tmp.png"
splitter = AlphaSpriteSplitter(img_path)
splitter.show_split_result((255, 0, 0, 255))
