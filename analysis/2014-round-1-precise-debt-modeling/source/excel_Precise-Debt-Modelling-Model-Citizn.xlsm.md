# Workbook: Precise-Debt-Modelling-Model-Citizn.xlsm

## Sheet: Cover
... (80+ rows truncated)
|  |  | ModelOff Comp 2014 - Precise Debt Modelling Solution |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Precise Debt Modelling (Loan 1 - live case) (Alert in Loan 2 solution) |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Go to Table of Contents |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Primary Developer:  Lance Rubin |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Cover Notes: |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | This model has been designed as an alternative approach/solution to the Modeloff 2014 Precise Debt Modelling Question. |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | The best way to navigate through the model is through the hyperlinks contained at the top left of each sheet and through the table of contents. |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Similar to how you would navigate a Word document or a PDF file. Follow the numbered arrows and use the hyperlinks for a quick demonstration to navigate your way around the model. |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | KEYS: |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Formats & Styles Key |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | Color Name |  |  |  | Color Description / Purpose |  |  |  |  | Example |  |
|  |  |  |  | Font Colors |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | Constant |  |  |  | Indicates ranges contain 100% constant (e.g. text/numbers). |  |  |  |  | Constant |  |
|  |  |  |  | Formula |  |  |  | Indicates ranges contain pure formulas / output calculations. |  |  |  |  | Formula |  |
|  |  |  |  | Mixed |  |  |  | Indicates ranges contain a mixture of formulas and constants (e.g. formulas that contain embedded text or numbers). |  |  |  |  | Mixed |  |
|  |  |  |  | Check |  |  |  | Indicates operative checks - normally used as a conditional format. |  |  |  |  | Check |  |
|  |  |  |  | Hyperlink |  |  |  | Indicates ranges contain hyperlinks to other ranges within the workbook or to other linked models. |  |  |  |  | Hyperlink |  |
|  |  |  |  | Fill Colors |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | Color A |  |  |  | Used to distinguish assumption sheets and/or cells. |  |  |  |  |  |  |
|  |  |  |  | Work In Progress |  |  |  | Indicates ranges contain data or formulas that remain uncertain or are subject to change. |  |  |  |  |  |  |
|  |  |  |  | Color B |  |  |  | Used to distinguish assumption sheets and/or cells. May also be used for a custom purpose. |  |  |  |  |  |  |
|  |  |  |  | Hyperlink Type |  |  |  | Hyperlink Description / Purpose |  |  |  |  | Example |  |
|  |  |  |  | Cover Hyperlink |  |  |  | Links Contents Sheet to Cover Sheet. |  |  |  |  | Go To Cover Sheet |  |
|  |  |  |  | Home Hyperlink |  |  |  | Links worksheets to Contents Sheet. |  |  |  |  | Go To Table of Contents |  |
|  |  |  |  | Custom Hyperlink |  |  |  | Links worksheet ranges to other worksheet ranges in the model. |  |  |  |  | Linked Cell Text |  |
|  |  |  |  | Sheet Top Hyperlink |  |  |  | Scrolls worksheet to the upper-most viewable section. |  |  |  |  | é |  |
|  |  |  |  | Sheet Left Hyperlink |  |  |  | Links active worksheet to the previous visible worksheet. |  |  |  |  | ç |  |
|  |  |  |  | Sheet Right Hyperlink |  |  |  | Links active worksheet to the next visible worksheet. |  |  |  |  | è |  |
|  |  | Sheet Naming Key |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  | Base Sheet Type |  |  |  | Sheet Description / Purpose |  |  |  |  | Suffix |  |
|  |  |  |  | Cover* |  |  |  | Indicates the start of a workbook. |  |  |  |  | Cover |  |
|  |  |  |  | Contents* |  |  |  | Contains the workbook Table of Contents. |  |  |  |  | Contents |  |
|  |  |  |  | Section Cover |  |  |  | Indicates the start of a workbook section. |  |  |  |  | SC |  |

## Sheet: Contents
|  | Table of Contents |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Precise Debt Modelling (Loan 1 - live case) (Alert in Loan 2 solution) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Go to Cover Sheet |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| é | Section & Sheet Titles |  |  |  |  |  |  |  |  |  |  |  |  |  |  | Page |
|  | 1 |  | Assumptions |  |  |  |  |  |  |  |  |  |  |  |  | 3 |
|  |  |  |  |  | a. |  | Key Assumptions |  |  |  |  |  |  |  |  | 4 |
|  |  |  |  |  | b. |  | Time Series Assumptions & Calculations |  |  |  |  |  |  |  |  | 5 |
|  | 2 |  | Outputs |  |  |  |  |  |  |  |  |  |  |  |  | 6 |
|  |  |  |  |  | a. |  | Model Outputs |  |  |  |  |  |  |  |  | 7 |
|  |  |  |  |  | b. |  | Loan Dashboards |  |  |  |  |  |  |  |  | 8 |
|  |  |  |  |  | c. |  | Model Questions & Solutions |  |  |  |  |  |  |  |  | 10 |
|  | 3 |  | Appendices |  |  |  |  |  |  |  |  |  |  |  |  | 12 |
|  |  |  |  |  | a. |  | Time Series Lookup Tables |  |  |  |  |  |  |  |  | 13 |
|  |  |  |  |  | b. |  | Checks |  |  |  |  |  |  |  |  | 16 |
|  |  |  |  |  |  |  | - | Error Checks |  |  |  |  |  |  |  | - |
|  |  |  |  |  |  |  | - | Alert Checks |  |  |  |  |  |  |  | - |
|  | Total Pages: |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 17 |

## Sheet: Assumptions_SC
|  |  | Assumptions |  |  |  |  |
|  |  | Section 1. |  |  |  |  |
|  |  | Precise Debt Modelling (Loan 1 - live case) (Alert in Loan 2 solution) |  |  |  |  |
|  |  | Go to Table of Contents |  |  |  |  |
|  |  | ç | è |  |  |  |
|  |  | Section Cover Notes: |  |  |  |  |
|  |  | The subequent sheets under the Assumptions section contain the relevant assumptions used to capture the variables contained within the ModelOff question. |  |  |  |  |

## Sheet: Key_Assumptions_BA
... (80+ rows truncated)
|  | Key Assumptions |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Precise Debt Modelling (Loan 1 - live case) (Alert in Loan 2 solution) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Go to Table of Contents |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| é | ç | è | x | O |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Assumptions |  |  |  |  |  |  | Additional Assumptions |  |  |  |  |  |  |  |  |  |
|  |  | Holidays |  |  |  |  |  | Days in year |  |  | 365 | days_in_yr |  |  |  |  |  |
|  |  |  |  |  | 2015-04-03 00:00:00 |  |  | Months in a year |  |  | 12 | mths_in_year |  |  |  |  |  |
|  |  |  |  |  | 2015-04-06 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2015-10-25 00:00:00 |  |  | Loan Assumption selection |  |  | 1 |  |  |  |  |  |  |
|  |  |  |  |  | 2016-03-25 00:00:00 |  |  |  |  |  |  |  | NB: Click goal seek button following a change in the drop down selection. |  |  |  |  |
|  |  |  |  |  | 2016-03-28 00:00:00 |  |  | Goal seek check |  |  | 0 |  |  |  |  |  |  |
|  |  |  |  |  | 2016-10-24 00:00:00 |  |  | Error check |  |  | 0 |  |  |  |  |  |  |
|  |  |  |  |  | 2017-04-14 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2017-04-17 00:00:00 |  |  | Chosen loan assumptions (based on drop down box selection) |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2017-10-30 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2018-03-30 00:00:00 |  |  | Loan Amount |  |  | 250000 |  |  |  |  |  |  |
|  |  |  |  |  | 2018-04-02 00:00:00 |  |  | Term |  |  | 72 | term | months |  |  |  |  |
|  |  |  |  |  | 2018-10-19 00:00:00 |  |  | Drawdown Date |  |  | 2015-01-19 00:00:00 |  |  |  |  |  |  |
|  |  |  |  |  | 2019-04-19 00:00:00 |  |  | Interest Rate |  |  | 0.052 | int |  |  |  |  |  |
|  |  |  |  |  | 2019-04-22 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2019-10-14 00:00:00 |  |  | Loan payment |  |  | -4049.47 | pmt |  |  |  |  |  |
|  |  |  |  |  | 2020-04-10 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2020-04-13 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | 2020-10-19 00:00:00 | CA_holidays |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Loan 1 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Loan Amount |  | 250000 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Term |  | 72 | months |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Drawdown Date |  | 2015-01-19 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Interest Rate |  | 0.052 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Loan 2 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Loan Amount |  | 100000 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Term |  | 48 | months |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Drawdown Date |  | 2015-06-30 00:00:00 |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Interest Rate |  | 0.07 |  |  |  |  |  |  |  |  |  |  |  |  |

## Sheet: Calcs_TA
|  | Time Series Assumptions & Calculations |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Precise Debt Modelling (Loan 1 - live case) (Alert in Loan 2 solution) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  | Go to Table of Contents |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| é | ç | è | x | O |  |  |  |  |  |  |  |  |  | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Model Timeseries & counters |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Period start date (loan draw down) |  |  |  |  |  | 2015-01-19 00:00:00 | 2015-02-20 00:00:00 | 2015-03-20 00:00:00 | 2015-04-20 00:00:00 | 2015-05-20 00:00:00 | 2015-06-20 00:00:00 | 2015-07-20 00:00:00 | 2015-08-20 00:00:00 | 2015-09-20 00:00:00 | 2015-10-20 00:00:00 | 2015-11-20 00:00:00 | 2015-12-20 00:00:00 | 2016-01-20 00:00:00 | 2016-02-20 00:00:00 | 2016-03-20 00:00:00 | 2016-04-20 00:00:00 | 2016-05-20 00:00:00 | 2016-06-20 00:00:00 | 2016-07-20 00:00:00 | 2016-08-20 00:00:00 | 2016-09-20 00:00:00 |
|  |  |  | Period end date (PED) |  |  |  |  |  | 2015-02-19 00:00:00 | 2015-03-19 00:00:00 | 2015-04-19 00:00:00 | 2015-05-19 00:00:00 | 2015-06-19 00:00:00 | 2015-07-19 00:00:00 | 2015-08-19 00:00:00 | 2015-09-19 00:00:00 | 2015-10-19 00:00:00 | 2015-11-19 00:00:00 | 2015-12-19 00:00:00 | 2016-01-19 00:00:00 | 2016-02-19 00:00:00 | 2016-03-19 00:00:00 | 2016-04-19 00:00:00 | 2016-05-19 00:00:00 | 2016-06-19 00:00:00 | 2016-07-19 00:00:00 | 2016-08-19 00:00:00 | 2016-09-19 00:00:00 | 2016-10-19 00:00:00 |
|  |  |  | Period counter |  |  |  |  |  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 |
|  |  |  | Next workday following period end date (incl PED) |  |  |  |  |  | 2015-02-19 00:00:00 | 2015-03-19 00:00:00 | 2015-04-20 00:00:00 | 2015-05-19 00:00:00 | 2015-06-19 00:00:00 | 2015-07-20 00:00:00 | 2015-08-19 00:00:00 | 2015-09-21 00:00:00 | 2015-10-19 00:00:00 | 2015-11-19 00:00:00 | 2015-12-21 00:00:00 | 2016-01-19 00:00:00 | 2016-02-19 00:00:00 | 2016-03-21 00:00:00 | 2016-04-19 00:00:00 | 2016-05-19 00:00:00 | 2016-06-20 00:00:00 | 2016-07-19 00:00:00 | 2016-08-19 00:00:00 | 2016-09-19 00:00:00 | 2016-10-19 00:00:00 |
|  |  |  | Previous workday prior to PED (excl PED) |  |  |  |  |  | 2015-02-18 00:00:00 | 2015-03-18 00:00:00 | 2015-04-17 00:00:00 | 2015-05-18 00:00:00 | 2015-06-18 00:00:00 | 2015-07-17 00:00:00 | 2015-08-18 00:00:00 | 2015-09-18 00:00:00 | 2015-10-16 00:00:00 | 2015-11-18 00:00:00 | 2015-12-18 00:00:00 | 2016-01-18 00:00:00 | 2016-02-18 00:00:00 | 2016-03-18 00:00:00 | 2016-04-18 00:00:00 | 2016-05-18 00:00:00 | 2016-06-17 00:00:00 | 2016-07-18 00:00:00 | 2016-08-18 00:00:00 | 2016-09-16 00:00:00 | 2016-10-18 00:00:00 |
|  |  |  | Payment date (interest period between dates) |  |  |  |  |  | 2015-02-19 00:00:00 | 2015-03-19 00:00:00 | 2015-04-20 00:00:00 | 2015-05-19 00:00:00 | 2015-06-19 00:00:00 | 2015-07-20 00:00:00 | 2015-08-19 00:00:00 | 2015-09-21 00:00:00 | 2015-10-19 00:00:00 | 2015-11-19 00:00:00 | 2015-12-21 00:00:00 | 2016-01-19 00:00:00 | 2016-02-19 00:00:00 | 2016-03-21 00:00:00 | 2016-04-19 00:00:00 | 2016-05-19 00:00:00 | 2016-06-20 00:00:00 | 2016-07-19 00:00:00 | 2016-08-19 00:00:00 | 2016-09-19 00:00:00 | 2016-10-19 00:00:00 |
|  |  |  | Days in month |  |  |  |  |  | 31 | 28 | 32 | 29 | 31 | 31 | 30 | 33 | 28 | 31 | 32 | 29 | 31 | 31 | 29 | 30 | 32 | 29 | 31 | 31 | 30 |
|  |  | Day of the week (logic check) |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Period end date (PED) |  |  |  |  |  | 2015-02-19 00:00:00 | 2015-03-19 00:00:00 | 2015-04-19 00:00:00 | 2015-05-19 00:00:00 | 2015-06-19 00:00:00 | 2015-07-19 00:00:00 | 2015-08-19 00:00:00 | 2015-09-19 00:00:00 | 2015-10-19 00:00:00 | 2015-11-19 00:00:00 | 2015-12-19 00:00:00 | 2016-01-19 00:00:00 | 2016-02-19 00:00:00 | 2016-03-19 00:00:00 | 2016-04-19 00:00:00 | 2016-05-19 00:00:00 | 2016-06-19 00:00:00 | 2016-07-19 00:00:00 | 2016-08-19 00:00:00 | 2016-09-19 00:00:00 | 2016-10-19 00:00:00 |
|  |  |  | Next workday following period end date (incl PED) |  |  |  |  |  | 2015-02-19 00:00:00 | 2015-03-19 00:00:00 | 2015-04-20 00:00:00 | 2015-05-19 00:00:00 | 2015-06-19 00:00:00 | 2015-07-20 00:00:00 | 2015-08-19 00:00:00 | 2015-09-21 00:00:00 | 2015-10-19 00:00:00 | 2015-11-19 00:00:00 | 2015-12-21 00:00:00 | 2016-01-19 00:00:00 | 2016-02-19 00:00:00 | 2016-03-21 00:00:00 | 2016-04-19 00:00:00 | 2016-05-19 00:00:00 | 2016-06-20 00:00:00 | 2016-07-19 00:00:00 | 2016-08-19 00:00:00 | 2016-09-19 00:00:00 | 2016-10-19 00:00:00 |
|  |  |  | Previous workday prior to PED (excl PED) |  |  |  |  |  | 2015-02-18 00:00:00 | 2015-03-18 00:00:00 | 2015-04-17 00:00:00 | 2015-05-18 00:00:00 | 2015-06-18 00:00:00 | 2015-07-17 00:00:00 | 2015-08-18 00:00:00 | 2015-09-18 00:00:00 | 2015-10-16 00:00:00 | 2015-11-18 00:00:00 | 2015-12-18 00:00:00 | 2016-01-18 00:00:00 | 2016-02-18 00:00:00 | 2016-03-18 00:00:00 | 2016-04-18 00:00:00 | 2016-05-18 00:00:00 | 2016-06-17 00:00:00 | 2016-07-18 00:00:00 | 2016-08-18 00:00:00 | 2016-09-16 00:00:00 | 2016-10-18 00:00:00 |
|  |  |  | Payment date (interest period between dates) |  |  |  |  |  | 2015-02-19 00:00:00 | 2015-03-19 00:00:00 | 2015-04-20 00:00:00 | 2015-05-19 00:00:00 | 2015-06-19 00:00:00 | 2015-07-20 00:00:00 | 2015-08-19 00:00:00 | 2015-09-21 00:00:00 | 2015-10-19 00:00:00 | 2015-11-19 00:00:00 | 2015-12-21 00:00:00 | 2016-01-19 00:00:00 | 2016-02-19 00:00:00 | 2016-03-21 00:00:00 | 2016-04-19 00:00:00 | 2016-05-19 00:00:00 | 2016-06-20 00:00:00 | 2016-07-19 00:00:00 | 2016-08-19 00:00:00 | 2016-09-19 00:00:00 | 2016-10-19 00:00:00 |
|  |  |  | Non business days |  |  |  | 24 |  | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
|  |  | Using the excel payment function |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Opening loan balance |  |  |  |  |  | 250000 | 247055 | 243991 | 241054 | 238000 | 235002 | 231990 | 228932 | 225959 | 222811 | 219745 | 216698 | 213544 | 210437 | 207317 | 204124 | 200947 | 197814 | 194582 | 191391 | 188187 |
|  |  |  | Repayments |  |  |  |  |  | -2945.36 | -3063.96 | -2937.14 | -3053.55 | -2998.35 | -3011.6 | -3057.95 | -2973.17 | -3148.11 | -3065.44 | -3047.67 | -3154.18 | -3106.37 | -3120.08 | -3192.94 | -3177.05 | -3133.37 | -3232.2 | -3190.11 | -3204.2 | -3245.16 |
|  |  |  | Closing loan balance |  |  |  |  |  | 247055 | 243991 | 241054 | 238000 | 235002 | 231990 | 228932 | 225959 | 222811 | 219745 | 216698 | 213544 | 210437 | 207317 | 204124 | 200947 | 197814 | 194582 | 191391 | 188187 | 184942 |
|  |  |  |  |  | Ending balance |  | 32.0864 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Interest charged |  |  |  | 41593.7 |  | 1104.11 | 985.511 | 1112.33 | 995.914 | 1051.11 | 1037.87 | 991.519 | 1076.29 | 901.359 | 984.03 | 1001.8 | 895.288 | 943.102 | 929.383 | 856.532 | 872.421 | 916.099 | 817.269 | 859.357 | 845.268 | 804.307 |
|  |  |  | Less payment (using pmt calculation) |  |  |  | -4049.47 |  | 2945.36 | 3063.96 | 2937.14 | 3053.55 | 2998.35 | 3011.6 | 3057.95 | 2973.17 | 3148.11 | 3065.44 | 3047.67 | 3154.18 | 3106.37 | 3120.08 | 3192.94 | 3177.05 | 3133.37 | 3232.2 | 3190.11 | 3204.2 | 3245.16 |
|  |  | Using goal seek |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Months |  |  |  | 72 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Opening loan balance |  |  |  |  |  | 250000 | 247054 | 243990 | 241052 | 237998 | 235000 | 231988 | 228929 | 225956 | 222807 | 219741 | 216693 | 213539 | 210432 | 207312 | 204118 | 200941 | 197807 | 194574 | 191384 | 188179 |
|  |  |  | Repayments |  |  |  |  |  | -2945.74 | -3064.34 | -2937.52 | -3053.94 | -2998.74 | -3011.99 | -3058.34 | -2973.57 | -3148.5 | -3065.83 | -3048.07 | -3154.58 | -3106.77 | -3120.49 | -3193.34 | -3177.45 | -3133.78 | -3232.61 | -3190.52 | -3204.61 | -3245.57 |
|  |  |  | Closing loan balance |  |  |  |  |  | 247054 | 243990 | 241052 | 237998 | 235000 | 231988 | 228929 | 225956 | 222807 | 219741 | 216693 | 213539 | 210432 | 207312 | 204118 | 200941 | 197807 | 194574 | 191384 | 188179 | 184934 |
|  |  |  | Goal Seek Error check |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  | Diff | Target | Current |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Closing balance |  | 2.31012e-10 | 0 | 2.31012e-10 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Payment |  |  |  | 4049.85 |  | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 | 4049.85 |
|  |  |  | Interest charged |  |  |  | 41589 |  | 1104.11 | 985.51 | 1112.33 | 995.91 | 1051.11 | 1037.86 | 991.509 | 1076.28 | 901.347 | 984.015 | 1001.78 | 895.27 | 943.081 | 929.36 | 856.509 | 872.396 | 916.07 | 817.241 | 859.326 | 845.235 | 804.273 |
|  |  |  | Less payment - using goal seek |  |  |  | 250000 |  | 2945.74 | 3064.34 | 2937.52 | 3053.94 | 2998.74 | 3011.99 | 3058.34 | 2973.57 | 3148.5 | 3065.83 | 3048.07 | 3154.58 | 3106.77 | 3120.49 | 3193.34 | 3177.45 | 3133.78 | 3232.61 | 3190.52 | 3204.61 | 3245.57 |
|  |  |  | % Balance of opening drawn amount |  |  |  | 0.4 |  | 1 | 0.988219 | 0.975963 | 0.964214 | 0.952 | 0.940007 | 0.92796 | 0.915728 | 0.903836 | 0.891243 | 0.878982 | 0.866791 | 0.854174 | 0.841749 | 0.829268 | 0.816497 | 0.803788 | 0.791255 | 0.778326 | 0.765566 | 0.752749 |
|  |  |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|  |  |  | Payments made prior to 40% of drawn balance |  |  |  | 46 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
|  |  |  | Count payment period days |  |  |  | 31 |  | 31 | 28 | 32 | 29 | 31 | 31 | 30 | 33 | 28 | 31 | 32 | 29 | 31 | 31 | 29 | 30 | 32 | 29 | 31 | 31 | 30 |
|  |  |  |  |  |  |  | 17 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Loan balance after payment number |  |  |  | 12 |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 213539 | 210432 | 207312 | 204118 | 200941 | 197807 | 194574 | 191384 | 188179 |
|  |  |  |  |  |  |  | 213539 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Total payments |  |  |  | 291589 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Total interest payment |  |  |  | 41589 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  | Ratio of interest to total |  |  |  | 0.142629 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  | Go to Model Outputs |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

## Sheet: Outputs_SC
|  |  | Outputs |  |  |  |  |
|  |  | Section 2. |  |  |  |  |
|  |  | Precise Debt Modelling (Loan 1 - live case) (Alert in Loan 2 solution) |  |  |  |  |
|  |  | Go to Table of Contents |  |  |  |  |
|  |  | ç | è |  |  |  |
|  |  | Section Cover Notes: |  |  |  |  |
|  |  | This section contain all the outputs as a result of the assumptions and calcutions prior to this section. |  |  |  |  |
