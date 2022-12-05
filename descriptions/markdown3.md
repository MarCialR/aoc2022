## --- Day 3: Rucksack Reorganization ---


One Elf has the important job of loading all of the [rucksacks](https://en.wikipedia.org/wiki/Rucksack) with supplies for thejunglejourney. Unfortunately, that Elf didn't quite follow the packing instructions, and so a few items now need to be rearranged.


Each rucksack has two large **compartments** . All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.


The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is,a``andA``refer to different types of items).


The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.


For example, suppose you have the following list of contents from six rucksacks:


```
 vJrwpWtwJgWrhcsFMMfFFhFp
 jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
 PmmdzqPrVvPwwTWBwg
 wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
 ttgJtRGJQctTZtZT
 CrZsJsPPZsGzwwsLwLmpwMDw

```


+ The first rucksack contains the itemsvJrwpWtwJgWrhcsFMMfFFhFp``, which means its first compartment contains the itemsvJrwpWtwJgWr``, while the second compartment contains the itemshcsFMMfFFhFp``. The only item type that appears in both compartments is lowercasep``.
+ The second rucksack's compartments containjqHRNqRjqzjGDLGL``andrsFMfFZSrLrFZsSL``. The only item type that appears in both compartments is uppercaseL``.
+ The third rucksack's compartments containPmmdzqPrV``andvPwwTWBwg``; the only common item type is uppercaseP``.
+ The fourth rucksack's compartments only share item typev``.
+ The fifth rucksack's compartments only share item typet``.
+ The sixth rucksack's compartments only share item types``.


To help prioritize item rearrangement, every item type can be converted to a **priority** :


+ Lowercase item typesa``throughz``have priorities 1 through 26.
+ Uppercase item typesA``throughZ``have priorities 27 through 52.


In the above example, the priority of the item type that appears in both compartments of each rucksack is 16 (p``), 38 (L``), 42 (P``), 22 (v``), 20 (t``), and 19 (s``); the sum of these is157``.


Find the item type that appears in both compartments of each rucksack. **What is the sum of the priorities of those item types?** 


