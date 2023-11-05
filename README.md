# Shikaku (詩客)

Toolbox for Japanese text.

## Example

```python
from shikaku import load_aozorabunko, TextModel, WordCloud
import matplotlib.pyplot as plt

# Aozora Bunko, author_id = 35, work_id = 1567 ==> Run, Melos!
text = load_aozorabunko(35, 1567)

# Text generator using Markov chains.
model = TextModel()
model.fit(text)
result = model.generate()
print(result)

# Word cloud.
wc = WordCloud()
wc.fit(text)
result = wc.generate()
result.to_file("wc.png")

# Visualize Markov chains (preliminary).
model = TextModel(state_size=1)
model.fit("吾輩は猫である。名前はまだない。")
model.plot()
plt.savefig("model.png")
```
