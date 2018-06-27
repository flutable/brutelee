library(gtools) # R general tools
#validChars <- chr(65:69) # vector of ascii symbols & letters, add 1 to upper limit in Python.
validChars <- chr(33:126)
maxpwlen <- 5
pw <- 0; ylen <- 0; pw <- 0
for (pwlen in 1: maxpwlen) {
  y    <- permutations(length(validChars), pwlen, validChars, repeats=T)
  ylen <- nrow(y)   #else we get both columns counted
  rm(y); gc()
  print(paste0("Password of length: ", toString(pwlen), ": ", toString(ylen)," passwords"))
  #print(y)
  pw = pw + ylen
}
print(paste0(validChars))
print(paste0("Total passwords: ", pw))
