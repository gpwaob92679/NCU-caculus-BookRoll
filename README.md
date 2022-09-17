# NCU calculus BookRoll (111)

This repository contains scripts to download and process BookRoll slides
in the NCU calculus course of year 111.

Downloaded JPG files and merged PDF files are also included.

## Processed Files

The table below contains links to processed files for easy access.

| Chapter                                              | PDF          | JPG Folder      |
|------------------------------------------------------|--------------|-----------------|
| Chapter 1 - Functions                                    | [PDF][Ch1PDF]  | [第一章][Ch1JPG]   |
| Chapter 2 - Limits and Continuity                        | [PDF][Ch2PDF]  | [第二章][Ch2JPG]   |
| Chapter 3 - Derivatives                                  | [PDF][Ch3PDF]  | [第三章][Ch3JPG]   |
| Chapter 4 - Applications of Derivatives                  | [PDF][Ch4PDF]  | [第四章][Ch4JPG]   |
| Chapter 5 - Integrals                                    | [PDF][Ch5PDF]  | [第五章][Ch5JPG]   |
| Chapter 6 - Applications of Definite Integrals           | [PDF][Ch6PDF]  | [第六章][Ch6JPG]   |
| Chapter 7 - Transcendental Functions                     | [PDF][Ch7PDF]  | [第七章][Ch7JPG]   |
| Chapter 8 - Techniques of Integration                    | [PDF][Ch8PDF]  | [第八章][Ch8JPG]   |
| Chapter 9 - First-Order Differential Equations           | [PDF][Ch9PDF]  | [第九章][Ch9JPG]   |
| Chapter 10 - Infinite Sequences and Series               | [PDF][Ch10PDF] | [第十章][Ch10JPG]  |
| Chapter 11 - Parametric Equations and Polar Coordinates  | [PDF][Ch11PDF] | [第十一章][Ch11JPG] |
| Chapter 12 - Vectors and the Geometry of Space           | [PDF][Ch12PDF] | [第十二章][Ch12JPG] |
| Chapter 13 - Vector-Valued Functions and Motion in Space | [PDF][Ch13PDF] | [第十三章][Ch13JPG] |
| Chapter 14 - Partial Derivatives                         | [PDF][Ch14PDF] | [第十四章][Ch14JPG] |
| Chapter 15 - Multiple Integrals                          | [PDF][Ch15PDF] | [第十五章][Ch15JPG] |

[Ch1PDF]: pdf/Chapter%201%20-%20Functions.pdf
[Ch2PDF]: pdf/Chapter%202%20-%20Limits%20and%20Continuity.pdf
[Ch3PDF]: pdf/Chapter%203%20-%20Derivatives.pdf
[Ch4PDF]: pdf/Chapter%204%20-%20Applications%20of%20Derivatives.pdf
[Ch5PDF]: pdf/Chapter%205%20-%20Integrals.pdf
[Ch6PDF]: pdf/Chapter%206%20-%20Applications%20of%20Definite%20Integrals.pdf
[Ch7PDF]: pdf/Chapter%207%20-%20Transcendental%20Functions.pdf
[Ch8PDF]: pdf/Chapter%208%20-%20Techniques%20of%20Integration.pdf
[Ch9PDF]: pdf/Chapter%209%20-%20First-Order%20Differential%20Equations.pdf
[Ch10PDF]: pdf/Chapter%2010%20-%20Infinite%20Sequences%20and%20Series.pdf
[Ch11PDF]: pdf/Chapter%2011%20-%20Parametric%20Equations%20and%20Polar%20Coordinates.pdf
[Ch12PDF]: pdf/Chapter%2012%20-%20Vectors%20and%20the%20Geometry%20of%20Space.pdf
[Ch13PDF]: pdf/Chapter%2013%20-%20Vector-Valued%20Functions%20and%20Motion%20in%20Space.pdf
[Ch14PDF]: pdf/Chapter%2014%20-%20Partial%20Derivatives.pdf
[Ch15PDF]: pdf/Chapter%2015%20-%20Multiple%20Integrals.pdf
[Ch1JPG]: jpg/第一章/
[Ch2JPG]: jpg/第二章/
[Ch3JPG]: jpg/第三章/
[Ch4JPG]: jpg/第四章/
[Ch5JPG]: jpg/第五章/
[Ch6JPG]: jpg/第六章/
[Ch7JPG]: jpg/第七章/
[Ch8JPG]: jpg/第八章/
[Ch9JPG]: jpg/第九章/
[Ch10JPG]: jpg/第十章/
[Ch11JPG]: jpg/第十一章/
[Ch12JPG]: jpg/第十二章/
[Ch13JPG]: jpg/第十三章/
[Ch14JPG]: jpg/第十四章/
[Ch15JPG]: jpg/第十五章/

## Running the scripts

### Requirements

- Python 3
- For packages, see [requirements.txt](requirements.txt)

### Usage

#### Downloading

To download the JPG files of slides from BookRoll, run:

```shell
python download.py
```

Enter your username and password as prompted. Downloaded image files should
appear under the `jpg/` folder by default.

#### Merging JPGs into PDF

To merge the downloaded JPG files into PDF files per chapter, run:

```shell
python jpg_to_pdf.py
```

The resulting PDF files should appear under the `pdf/` folder by default.
