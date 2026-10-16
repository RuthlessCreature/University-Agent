# Public CC0 palmerpenguins, descriptive example. Not executed in this environment.
d <- read.csv('training/deck-zh/sources/penguins.csv', na.strings='NA')
out <- do.call(rbind, lapply(split(d$body_mass_g, d$species), function(x) {
  x <- x[!is.na(x)]
  c(n=length(x), mean=mean(x), sample_sd=sd(x))
}))
print(out)
