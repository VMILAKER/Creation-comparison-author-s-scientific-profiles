# Introduction
*!Please see attached data in ['master' branch](https://github.com/VMILAKER/Creation-comparison-author-s-scientific-profiles/tree/master/Data)!* <br/>

This repository regarding a drafting of scientific researchers profile by the evaluation of their publications in quartile journals. Journal's description and its rankings with quartile are allocated in site Scimagojr for 2023.
# Main part
## Theory
The visual appearance is considered to be matrix $A(m*n)$, where m-number of authors, n-number of rubrics <br/>
Next, certain author's contribution in rubric might be visualised through formula:
```math
$a_{ij} = l_{ij}+k_{ij}+r_{ij} 
```
where
* $l_{ij}$ - author's contribution in rubric if number of authors < 20 people;
* $k_{ij}$ - author's contribution in rubric if number of authors >= 20 people (collaborative publication);
* $r_{ij}$ - author's contribution in rubric if aritcles without rubrics;
The range of publication can be interpreted as well
```math
P_{ij}=L_{ij} \cup K_{ij} \cup R_{ij}
```
where
* $P_{ij} - publications of author i by rubric j;
* $L_{ij}$ - -//-, if number of authors in article < 20;
* $K_{ij}$ - -//-, if article is collaborative;
* $R_{ij}$ - articles of author i without rubric;
Main formula to calculate contribution certain author $(M_i)$ in certain rubric $(N_j)$
```math
a_{ij} =\sum_{p_l \in L_{ij}} f_1(p_l)*c(p_l)*Q_{5-n}(p_l) + \sum_{p_l \in K_{ij}} f_2(p_k)*c(p_k)*Q_{5-n}(p_k) + 0
```
where 
* $f_1(p_l)=\frac{1}{"author's sequence number "(p_l)};$
* $f_2(p_k)=\frac{1}{(number of authors (p_k))};$
* $c(p_{l,k}) = 1 - that equation exists by far;$
* $Q_{5-n}$ - quartile's number - is equal to (5 - number of quartile) e.g. $Q_1$=5-1=4
# Link on presentation
[Presenation JINR- 2025](https://disk.yandex.ru/i/rrI_7OZYy7PlCQ)
