* 教学代码，本轮未在IBM SPSS Statistics中执行，不附伪造输出。
* 先将当前目录设为本文件所在目录，确保可写；原始CSV为UTF-8。
* 0=female，1=male；标准差取样本标准差，均值差为雄减雌。
NEW FILE.
WEIGHT OFF.
FILTER OFF.
SPLIT FILE OFF.
GET DATA /TYPE=TXT /FILE='penguins.csv'
 /ENCODING='UTF8' /ARRANGEMENT=DELIMITED /FIRSTCASE=2
 /DELIMITERS="," /QUALIFIER='"' /IMPORTCASE=ALL
 /VARIABLES=species A16 island A16 bill_length_text A16 bill_depth_text A16
 flipper_text A16 body_mass_text A16 sex A16 year_text A8.
COMPUTE csv_line=$CASENUM+1.
SELECT IF (species='Adelie' AND ANY(sex,'female','male')
 AND flipper_text<>'NA' AND RTRIM(flipper_text)<>'').
COMPUTE flipper_mm=NUMBER(flipper_text,F8.0).
SELECT IF NOT SYSMIS(flipper_mm).
COMPUTE sex_code=(sex='male').
FORMATS csv_line(F8.0) sex_code(F1.0) flipper_mm(F20.12).
EXECUTE.
SAVE TRANSLATE OUTFILE='spss-included_rows.csv' /TYPE=CSV /ENCODING='UTF8'
 /REPLACE /FIELDNAMES /CELLS=VALUES /KEEP=csv_line sex_code flipper_mm.
MEANS TABLES=flipper_mm BY sex_code /CELLS=COUNT MEAN STDDEV.
AGGREGATE /OUTFILE='spss-summary.sav' /BREAK=sex_code
 /n=N(flipper_mm) /mean_mm=MEAN(flipper_mm) /sd_mm=SD(flipper_mm).
COMPUTE female_mm=$SYSMIS.
COMPUTE male_mm=$SYSMIS.
IF (sex_code=0) female_mm=flipper_mm.
IF (sex_code=1) male_mm=flipper_mm.
AGGREGATE /OUTFILE=* /BREAK=
 /female_n=N(female_mm) /male_n=N(male_mm)
 /female_mean_mm=MEAN(female_mm) /male_mean_mm=MEAN(male_mm).
COMPUTE male_minus_female_mm=male_mean_mm-female_mean_mm.
FORMATS female_n male_n(F8.0)
 female_mean_mm male_mean_mm male_minus_female_mm(F20.12).
SAVE TRANSLATE OUTFILE='spss-comparison.csv' /TYPE=CSV /ENCODING='UTF8'
 /REPLACE /FIELDNAMES /CELLS=VALUES.
GET FILE='spss-summary.sav'.
FORMATS sex_code(F1.0) n(F8.0) mean_mm sd_mm(F20.12).
SAVE TRANSLATE OUTFILE='spss-summary.csv' /TYPE=CSV /ENCODING='UTF8'
 /REPLACE /FIELDNAMES /CELLS=VALUES.
* 运行后再核对行号、0/1分组、146条记录、均值和SD。
* 当前提供的是完整教学语法文件，不能称为已通过SPSS运行验证。
