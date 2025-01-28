# SpriteSpliter

## Description

A sprite image spliter for rgba format image.

## Usage

```python
from tools.sprite_spliter import AlphaSpriteSpliter, SpliterAlgorithm

img_path = "test/assets/multiple_test0.png"
spliter = AlphaSpriteSpliter(img_path)
box_border_color = (255, 0, 0, 255)
# default is SpliterAlgorithm.SPRITE_SCAN
spliter.show_split_result(box_border_color, SpliterAlgorithm.EDGE_DETECT)
```

Please refer to [here](./docs/usage.md)

## Performance

Platform: Python 3.12.7
CPU: Mac M3 Max

### EDGE DETECT

| image                                  | split time                  |
| -------------------------------------- | --------------------------- |
| assets/multiple_test0.png(104 x 113)   | 0.25486283301142976 seconds |
| assets/multiple_test1.png(2048 x 2048) | 2.9249990829848684 seconds  |
| assets/multiple_test2.png(1024 x 512)  | 1.142435582994949 seconds   |
| assets/tmp.png(1024 x 1024)            | 2.3546547499718145 seconds  |

### SPRITE SCAN

| image                                  | split time                  |
| -------------------------------------- | --------------------------- |
| assets/multiple_test0.png(104 x 113)   | 0.19917637499747798 seconds |
| assets/multiple_test1.png(2048 x 2048) | 0.8949957919539884 seconds  |
| assets/multiple_test2.png(1024 x 512)  | 0.3498120000003837 seconds  |
| assets/tmp.png(1024 x 1024)            | 0.6984633749816567 seconds  |

# Execution Result

See [here](./docs/result.md)

# Disclaimer

All downloads and use of the software (SpriteSpliter) are considered to have been carefully read and fully agreed to the following terms:

The software (SpriteSpliter) is provided solely for personal learning and communication purposes. It is strictly prohibited to use it for commercial or malicious purposes.

If any commercial use or malicious behavior is discovered, the author of the software (SpriteSpliter) reserves the right to revoke the usage rights.

All risks associated with the use of this software shall be borne solely by the user. The author of the software (SpriteSpliter) shall not be held responsible for any consequences.

Except for the service terms specified in the software (SpriteSpliter), the author shall not be liable for any accidents, negligence, contract breaches, defamation, copyright or other intellectual property infringements, or any losses caused by improper use of the software.

The author of the software (SpriteSpliter) shall not be responsible for any service interruptions or defects caused by force majeure, hacker attacks, communication line interruptions, or other uncontrollable factors that prevent normal use. However, the author will make every effort to minimize the losses or impacts caused to users.

Any issues not covered in this disclaimer shall be governed by the relevant national laws and regulations. In the event of any conflict between this disclaimer and national laws and regulations, the latter shall prevail.

The copyright of this disclaimer, as well as the rights to modify, update, and ultimately interpret it, belong solely to the author of the software (SpriteSpliter).
