# Shipping Classifier

A simple text classifier using BERT - for dates, locations, company names and vessel names.


## Evaluation Results

```
eval_accuracy = 0.9444444
eval_loss = 0.18641633
global_step = 190
loss = 0.18245141
```


## Test Results
```
                                                 text    label prediction
0                                            bandirma     port       port
1                                          1905-04-15     date       date
2                                  seven seas voyager   vessel     vessel
3                 digicel (singapore) private limited  company    company
4                                       motor yacht a   vessel     vessel
5                                         1883-May-17     date       date
6                         hasse bank johansen consult  company    company
7                                                aden     port       port
8                                      msc meraviglia   vessel     vessel
9                                                 air   vessel    company
10                    ministry of hunting affairs aps  company    company
11                                         bob barker   vessel     vessel
12                                       msc preziosa   vessel     vessel
13                                             balogo     port       port
14           john bean technologies hong kong limited  company    company
15                         aleksandrovsk-sakhalinskiy     port       port
16                                         1858/12/09     date       date
17                                        22 Nov 2032     date       date
18                                14th February, 2081     date       date
19                             mogens haahr lauridsen  company    company
20                        shiji (singapore) pte. ltd.  company    company
21                          bxt international limited  company    company
22                                        1857-Sep-17     date       date
23                                  17-September-1863     date       date
24                                 anthem of the seas   vessel     vessel
25  hongkong and shanghai banking corporation limi...  company    company
26                  galleri bo bjerggaard holding aps  company    company
27                                              ambon     port       port
28                                             balogo     port       port
29                                      vividworks oy  company    company
30                                        aeropole oy  company    company
31                                    fryderyk chopin   vessel     vessel
32                                     Mar 05th, 1830     date       date
33                              long bridge pte. ltd.  company    company
34                                        viking star   vessel     vessel
35                                   29th August 1885     date       date
36                                        vera rambow   vessel     vessel
37                                            abidjan     port       port
38                             vitran cincinnati, llc  company    company
39                                voyager of the seas   vessel     vessel
40                               celebrity silhouette   vessel     vessel
41                              rlc investments, inc.  company    company
42                                      13th Jan 2014     date       date
43                                       oy verman ab  company    company
44                                        Jan 01 1931     date       date
45                                      20th Aug 1881     date       date
```