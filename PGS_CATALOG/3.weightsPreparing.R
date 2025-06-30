library(data.table)
library(readr)

folders <- list.dirs('PGS_CATALOG_WEIGHTS/', recursive = FALSE)

for (f in folders) {
  file <- file.path(f, list.files(f)[1])
  print(file)
  weights_path <- file.path(f, 'weights.txt')
  weights_clean_path <- file.path(f, 'weights_clean.txt')

  system(paste('zcat', shQuote(file), '>', shQuote(weights_path)))
  system(paste('sed "/^#/d" ', shQuote(weights_path), '>', shQuote(weights_clean_path)))
}
