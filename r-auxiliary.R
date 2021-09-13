# 

url <- './PycharmProjects/corona_map/data/owid_all.csv'

df <- read.csv(url)

colnames(df)

cols <- colnames(df)[grep('cases', colnames(df))]
cols

dfx <- df[, cols]

rowSums(is.na(dfx))

dfx[2,]



cols <- c(2, 6, 12, 48)

dfx <- df[100, cols]

dfx

dfx$total_cases / dfx$population * 1e+6
