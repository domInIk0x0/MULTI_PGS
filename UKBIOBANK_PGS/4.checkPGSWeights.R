library(snpStats)
library(data.table)
library(dplyr)

flip_allele <- function(a) {
  comp <- c(A="T", T="A", C="G", G="C")
  a <- toupper(a)
  res <- comp[a]
  ifelse(is.na(res), NA, res)
}

bim <- fread('plink_format_vcf/merged.bim', header = FALSE)
setnames(bim, c("chr", "SNP", "cm_pos", "pos", "allele1", "allele2"))

folders <- list.dirs('UKBIOBANK_WEIGHTS/', recursive = FALSE)
cat("=======================================================================", "\n")
for (f in folders) {
  cat("Weights loading for: ", basename(f), "\n")
  tsv_files <- list.files(f, pattern = "\\.tsv$", recursive = TRUE, full.names = TRUE)

  if (length(tsv_files) == 0) {
    cat("!!! TSV file does not exist in the folder:", f, "\n")
    next
  }

  file <- tsv_files[1] 

  cat("Używany plik wag:", file, "\n")

  pgs <- fread(file)

  if (('CHROM' %in% colnames(pgs)) & ('POS' %in% colnames(pgs))) {
    cat("Matching by chromosome position...\n")
    pgs[, CHROM := as.character(CHROM)]
    bim[, chr := as.character(chr)]
    x <- c('CHROM', 'POS')
    y <- c('chr', 'pos')
  } else if ('ID' %in% colnames(pgs)) {
    cat("Matching by snp name...\n")
    x <- 'ID'
    y <- 'SNP'
  } else {
    stop("No columns for matching (CHROM/POS or ID) found in the weights file")
  }

  merged <- merge(pgs, bim, by.x = x, by.y = y, all.x = FALSE, all.y = FALSE)

  if ('ID' %in% colnames(merged)) {
    setnames(merged, 'ID', 'SNP')
  }

  cat("Total variants in BIM file: ", nrow(bim), "\n")
  cat("Weights count from UK Biobank file: ", nrow(pgs), "\n")

  merged[, effect_allele := ALT]
  merged[, effect_weight := BETA]

  merged[, allel_match := (effect_allele == allele1) | (effect_allele == allele2)]
  t <- table(merged$allel_match)
  
  cat('Number of SNPs with effect allele mismatch:', ifelse(!is.na(t["FALSE"]), t["FALSE"], 0), "\n")
  cat('Number of SNPs with effect allele match:', ifelse(!is.na(t["TRUE"]), t["TRUE"], 0), "\n")

  merged[, flip_needed := (!allel_match) & (
    (flip_allele(effect_allele) == allele1) | (flip_allele(effect_allele) == allele2)
  )]
  t <- table(merged$flip_needed)
  
  cat('Number of SNPs requiring flip:', ifelse(!is.na(t["TRUE"]), t["TRUE"], 0), "\n")
  cat('Number of SNPs not requiring flip:', ifelse(!is.na(t["FALSE"]), t["FALSE"], 0), "\n")

  merged[, A1 := ifelse(flip_needed, flip_allele(effect_allele), effect_allele)]
  merged[, SCORE := effect_weight]

  score_file <- merged[!is.na(A1), .(SNP, A1, SCORE)]
  score_file <- score_file[!duplicated(SNP)]

  dup_count <- nrow(score_file) - length(unique(score_file$SNP))
  
  cat('Number of duplicate SNPs:', dup_count, '\n')
  cat('Matched variants:', nrow(merged), "\n")
  cat('Percentage of variants used for PGS calculation (relative to BIM): ', nrow(score_file) / nrow(bim) * 100, "%\n")
  cat('Percentage of matched variants (relative to weights): ', nrow(score_file) / nrow(pgs) * 100, "%\n")
  cat("=======================================================================", "\n")
  cat("\n")

  fwrite(score_file, file.path(f, 'plink_weights.txt'), sep = "\t", col.names = FALSE)
}
