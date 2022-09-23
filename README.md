# NCU calculus BookRoll (111)

This repository contains scripts to download and process BookRoll slides
in the NCU calculus course of year 111.

Fixed PDF files are also included.

## Processed Files

The table below contains links to processed PDF files for easy access.

| Chapter                                              | PDF          |
|------------------------------------------------------|--------------|
| Chapter 1 - Functions                                    | [PDF][Ch1PDF]  |
| Chapter 2 - Limits and Continuity                        | [PDF][Ch2PDF]  |
| Chapter 3 - Derivatives                                  | [PDF][Ch3PDF]  |
| Chapter 4 - Applications of Derivatives                  | [PDF][Ch4PDF]  |
| Chapter 5 - Integrals                                    | [PDF][Ch5PDF]  |
| Chapter 6 - Applications of Definite Integrals           | [PDF][Ch6PDF]  |
| Chapter 7 - Transcendental Functions                     | [PDF][Ch7PDF]  |
| Chapter 8 - Techniques of Integration                    | [PDF][Ch8PDF]  |
| Chapter 9 - First-Order Differential Equations           | [PDF][Ch9PDF]  |
| Chapter 10 - Infinite Sequences and Series               | [PDF][Ch10PDF] |
| Chapter 11 - Parametric Equations and Polar Coordinates  | [PDF][Ch11PDF] |
| Chapter 12 - Vectors and the Geometry of Space           | [PDF][Ch12PDF] |
| Chapter 13 - Vector-Valued Functions and Motion in Space | [PDF][Ch13PDF] |
| Chapter 14 - Partial Derivatives                         | [PDF][Ch14PDF] |
| Chapter 15 - Multiple Integrals                          | [PDF][Ch15PDF] |

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

## Running the scripts

### Requirements

- Python 3
- For packages, see [requirements.txt](requirements.txt)

### Usage

#### Downloading

To download PDF files of slides from BookRoll, run:

```shell
python download.py
```

Enter your username and password as prompted. Downloaded PDF files should
appear under the `pdf/` folder by default.

#### Fix border issues in downloaded PDF files

To fix weird border issues found in downloaded PDF files, run:

```shell
python fix_pdf.py
```

The fixed PDF files should appear under the `pdf/` folder by default, with the
filename "Chapter x - Title of Chapter.pdf".
