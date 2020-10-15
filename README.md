
# Dianping Shops User Reviews and Stars Crawler

![Language Python](https://img.shields.io/badge/Language-Python-red)
[![License MIT](https://img.shields.io/github/license/imrdong/dazhongdianping.svg?label=License&color=blue)](https://github.com/imrdong/dazhongdianping/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/imrdong/dazhongdianping.svg?style=social&label=Star&maxAge=10)](https://github.com/imrdong/dazhongdianping/stargazers/)
[![GitHub forks](https://img.shields.io/github/forks/imrdong/dazhongdianping?style=social&label=Fork&maxAge=10)](https://github.com/imrdong/dazhongdianping/network/members/)

# Background

The encryption of dianping is divided into two categories, one is CSS encryption, the other is font library encryption, this paper only solved the CSS encryption, for the font library encryption has not yet been solved.

# Task
Grab user reviews and stars of dianping shops.

## CSS Encryption

### Process

*   Get the contents of the CSS file.  
*   Get a dictionary.  
*   Initiate the request, parse the SVG tag, and print the reviews.
 
### Categories

In CSS encryption, the source code of SVG files is divided into two categories, which is also a measure of dianping's anti-crawling, Dianping will automatically change the contents of SVG files according to time, which can be solved by calling two different functions in the code.

### Result

Save user reviews and stars as CSV files.

# Problem

*   If the crawler is too fast, the IP will be blocked (this article adds a pause mechanism).  
*   About 40 minutes for the crawler, the verification code will appear (temporarily solved by manually refreshing the web page and entering the verification code).  
*   Account is blocked, then the web page shows an error request, the only way is to switch to another account and get a new COOKIE.

# Instruction

This code captures the specified shop's user reviews and stars, only containing CSS encryption.  
As of 2020/04/09, this code can not guarantee normal operation.

# Statement

The code is for communication and learning only.