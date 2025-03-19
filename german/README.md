## B2 German Verbs Collection
This project contains a comprehensive Python list of B2-level German verbs with detailed information in PORTUGUESE to help learners improve their German skills. The list is structured as a dictionary, providing the following details for each verb. There is a Duden  dictionary entry for comparison, so the CLI must be installed before (pip install duden).

# Features
**verbo**: The infinitive form of the verb in German.
**tradução**: The Portuguese translation of the verb.
**frase**: A sample sentence demonstrating the verb in context.
**tradução_frase**: The Portuguese translation of the example sentence.
**sinônimo**: A list of common German synonyms.
**perfekt** Form: The perfect tense form of the verb.
**präteritum** Form: The simple past tense form of the verb.
**regência**: Information about the verb's case governance (Akkusativ, Dativ, etc.).
**outra_frase**: Another example sentence using a verb synonym.
**tradução_outra_frase**: Portuguese translation of the additional example.
**reflexivo**: Boolean value indicating whether the verb is reflexive.

# Usage
You can load the list of verbs into a Python script and create custom exercises, flashcards, or even integrate it into a language learning app.

# Example:

```python
from verbs import verbos

# Print all verbs and their meanings
for verbo in verbos:
    print(f"{verbo['verbo']} - {verbo['tradução']}")
```

# Requirements
Python 3.x

# Notes
The list includes verbs that cover more advanced sentence structures and common usage patterns in B2-level German.
The example sentences help to understand the context and proper case usage.

# Credits
Special thanks to Radomír Bosák for creating the CLI tool used in this project.

The CLI tool is licensed under the MIT License:

```
MIT License

Copyright (c) 2018 Radomír Bosák

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```