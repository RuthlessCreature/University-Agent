# 公开企鹅数据二次描述统计。默认在本文件所在目录运行。
# 桌面R：Rscript analysis.R；可选第一个参数为原始CSV路径。
args <- commandArgs(trailingOnly = TRUE)
input <- if (length(args) > 0) args[1] else "penguins.csv"
options(digits = 17)
d <- read.csv(input, na.strings = c("NA", ""), stringsAsFactors = FALSE)
stopifnot(nrow(d) == 344)
d$csv_line <- seq_len(nrow(d)) + 1L
keep <- !is.na(d$species) & d$species == "Adelie" &
        !is.na(d$sex) & d$sex %in% c("female", "male") &
        !is.na(d$flipper_length_mm)
selected <- d[keep, ]
selected$sex_code <- ifelse(selected$sex == "female", 0L, 1L)
stopifnot(nrow(selected) == 146)
summary_rows <- do.call(rbind, lapply(0:1, function(code) {
  x <- selected$flipper_length_mm[selected$sex_code == code]
  stopifnot(length(x) == 73)
  data.frame(sex_code = code, n = length(x), mean_mm = mean(x), sd_mm = sd(x))
}))
comparison <- data.frame(
  female_n = summary_rows$n[1], male_n = summary_rows$n[2],
  female_mean_mm = summary_rows$mean_mm[1], male_mean_mm = summary_rows$mean_mm[2],
  male_minus_female_mm = summary_rows$mean_mm[2] - summary_rows$mean_mm[1])
included_rows <- data.frame(csv_line = selected$csv_line,
                           sex_code = selected$sex_code,
                           flipper_mm = selected$flipper_length_mm)
dir.create("r-output", showWarnings = FALSE)
write.csv(summary_rows, "r-output/summary.csv", row.names = FALSE)
write.csv(comparison, "r-output/comparison.csv", row.names = FALSE)
write.csv(included_rows, "r-output/included_rows.csv", row.names = FALSE)
writeLines(capture.output(sessionInfo()), "r-output/session-info.txt")
print(summary_rows)
print(comparison)
# sd使用n-1分母。此脚本不计算P值，不作因果或总体外推判断。
