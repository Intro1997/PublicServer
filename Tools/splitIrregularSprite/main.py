from tools.sprite_spliter import AlphaSpriteSpliter


img_path = "test/assets/multiple_test0.png"
spliter = AlphaSpriteSpliter(img_path)
spliter.show_split_result((255, 0, 0, 255))
